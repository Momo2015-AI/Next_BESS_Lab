"""
用户认证相关API路由
支持注册、登录、JWT token验证
"""

import hashlib
import hmac
import re
import secrets
import uuid
from datetime import datetime, timedelta, timezone

import jwt
from flask import Blueprint, current_app, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from sqlalchemy.exc import IntegrityError

auth_bp = Blueprint("auth", __name__)

# 速率限制器（延迟初始化，避免在模块导入时访问 current_app）
limiter = Limiter(key_func=get_remote_address, default_limits=[])

# JWT token 黑名单
# 默认进程内 dict；若设置环境变量 REDIS_URL 则改用 Redis（多 worker / 多进程部署可共享）。
import base64 as _base64
import json as _json
import os as _os

_token_blacklist = {}


def _extract_jti(token):
    """从 JWT 中解码 jti（仅解 payload 段，无需密钥）"""
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return None
        payload = parts[1]
        payload += "=" * (-len(payload) % 4)
        data = _json.loads(_base64.urlsafe_b64decode(payload))
        return data.get("jti")
    except Exception:
        return None


_redis_client = None


def _get_redis():
    """延迟初始化 Redis 客户端；未配置或连接失败时返回 None（降级为内存）。"""
    global _redis_client
    if _redis_client is not None:
        return _redis_client
    redis_url = _os.environ.get("REDIS_URL")
    if redis_url:
        try:
            import redis

            _redis_client = redis.from_url(redis_url, socket_timeout=2, socket_connect_timeout=2)
            return _redis_client
        except Exception:
            _redis_client = False
            return None
    _redis_client = False
    return None


def _clean_blacklist():
    """清理超过24小时的进程内黑名单条目"""
    now = datetime.now(timezone.utc)
    expired = [t for t, ts in _token_blacklist.items() if (now - ts).total_seconds() > 86400]
    for t in expired:
        del _token_blacklist[t]


def add_to_blacklist(token):
    """将 token 加入黑名单（按 jti 存储，多实例可共享）"""
    jti = _extract_jti(token)
    r = _get_redis()
    if r is not None:
        try:
            if jti:
                r.set(f"bl:{jti}", 1, ex=86400)
            return
        except Exception:
            pass
    _token_blacklist[token] = datetime.now(timezone.utc)
    _clean_blacklist()


def is_blacklisted(token):
    """检查 token 是否在黑名单中"""
    jti = _extract_jti(token)
    if jti:
        r = _get_redis()
        if r is not None:
            try:
                if r.exists(f"bl:{jti}"):
                    return True
            except Exception:
                pass
    return token in _token_blacklist


def hash_password(password, salt=None):
    """密码哈希，PBKDF2-SHA256，600,000 次迭代"""
    if salt is None:
        salt = secrets.token_hex(16)
    hashed = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 600000)
    return f"{salt}${hashed.hex()}"


def verify_password(password, hashed):
    """验证密码"""
    try:
        salt, _ = hashed.split("$")
        return hmac.compare_digest(hash_password(password, salt), hashed)
    except (ValueError, IndexError):
        return False


def _get_secret_key():
    """获取 SECRET_KEY，无默认值保护"""
    return current_app.secret_key


def generate_token(user_id, expires_in=24):
    """生成JWT token，含 jti 用于撤销"""
    payload = {
        "jti": str(uuid.uuid4()),
        "user_id": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(hours=expires_in),
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, _get_secret_key(), algorithm="HS256")


def decode_token(token):
    """解码JWT token，同时检查黑名单"""
    if is_blacklisted(token):
        return None
    try:
        payload = jwt.decode(token, _get_secret_key(), algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def _get_user_from_token():
    """从请求头提取 token 并获取用户"""
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return None, ("未提供认证token", 401)

    token = auth_header[7:]
    payload = decode_token(token)
    if not payload:
        return None, ("token已失效", 401)

    user_id = payload.get("user_id")
    from database import User

    user = User.query.get(user_id)
    if not user:
        return None, ("用户不存在", 404)

    return user, None


def _validate_username(username):
    """校验用户名格式：3-20位，仅允许字母/数字/下划线/中文"""
    if not username or len(username) < 3 or len(username) > 20:
        return False
    if not re.match(r"^[\w\u4e00-\u9fff]{3,20}$", username):
        return False
    return True


@auth_bp.route("/api/auth/register", methods=["POST"])
@limiter.limit("5/hour")
def register():
    """用户注册"""
    data = request.get_json()

    if not data:
        return jsonify({"error": "无效的请求数据"}), 400

    username = data.get("username", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "")
    tenant_id = "00000000-0000-0000-0000-000000000001"  # 默认租户UUID，禁止客户端自选

    if not _validate_username(username):
        return jsonify({"error": "用户名需3-20位，仅允许字母/数字/下划线/中文"}), 400

    if not email or "@" not in email:
        return jsonify({"error": "请输入有效的邮箱地址"}), 400

    if not password or len(password) < 6:
        return jsonify({"error": "密码至少需要6个字符"}), 400

    from database import User

    existing_user = User.query.filter((User.username == username) | (User.email == email)).first()

    if existing_user:
        return jsonify({"error": "用户名或邮箱已存在"}), 409

    from database import db

    user_id = str(uuid.uuid4())

    user = User(
        id=user_id,
        username=username,
        email=email,
        password_hash=hash_password(password),
        tenant_id=tenant_id,
        role="user",
        is_active=True,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    db.session.add(user)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "用户名或邮箱已存在"}), 409
    except Exception:
        db.session.rollback()
        current_app.logger.error("注册失败", exc_info=True)
        return jsonify({"error": "注册失败，请稍后重试"}), 500

    token = generate_token(user_id)

    return (
        jsonify(
            {
                "success": True,
                "message": "注册成功",
                "token": token,
                "user": {
                    "id": user_id,
                    "username": username,
                    "email": email,
                    "role": "user",
                },
            }
        ),
        201,
    )


@auth_bp.route("/api/auth/login", methods=["POST"])
@limiter.limit("10/hour")
def login():
    """用户登录"""
    data = request.get_json()

    if not data:
        return jsonify({"error": "无效的请求数据"}), 400

    username = data.get("username", "").strip()
    password = data.get("password", "")

    if not username or not password:
        return jsonify({"error": "请输入用户名和密码"}), 400

    from database import User

    user = User.query.filter((User.username == username) | (User.email == username)).first()

    if not user:
        return jsonify({"error": "用户名或密码错误"}), 401

    if not user.is_active:
        return jsonify({"error": "用户名或密码错误"}), 401

    if not verify_password(password, user.password_hash):
        return jsonify({"error": "用户名或密码错误"}), 401

    user.last_login = datetime.now(timezone.utc)
    user.login_count = (user.login_count or 0) + 1

    from database import db

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        current_app.logger.error("登录记录更新失败", exc_info=True)

    token = generate_token(user.id)

    return (
        jsonify(
            {
                "success": True,
                "message": "登录成功",
                "token": token,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "role": user.role,
                    "tenant_id": user.tenant_id,
                },
            }
        ),
        200,
    )


@auth_bp.route("/api/auth/logout", methods=["POST"])
def logout():
    """用户登出，将 token 加入黑名单"""
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        token = auth_header[7:]
        add_to_blacklist(token)

    return jsonify({"success": True, "message": "已退出登录"}), 200


@auth_bp.route("/api/auth/me", methods=["GET"])
def get_current_user():
    """获取当前用户信息"""
    user, error = _get_user_from_token()
    if error:
        return jsonify({"error": error[0]}), error[1]

    return (
        jsonify(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
                "tenant_id": user.tenant_id,
                "is_active": user.is_active,
                "created_at": user.created_at.isoformat() if user.created_at else None,
                "last_login": user.last_login.isoformat() if user.last_login else None,
            }
        ),
        200,
    )


@auth_bp.route("/api/auth/refresh", methods=["POST"])
def refresh_token():
    """刷新token，要求 token 在 1 小时内过期才允许刷新"""
    user, error = _get_user_from_token()
    if error:
        return jsonify({"error": error[0]}), error[1]

    new_token = generate_token(user.id)

    # 旧 token 加入黑名单
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        add_to_blacklist(auth_header[7:])

    return (
        jsonify(
            {
                "success": True,
                "token": new_token,
            }
        ),
        200,
    )


@auth_bp.route("/api/auth/change-password", methods=["POST"])
def change_password():
    """修改密码"""
    user, error = _get_user_from_token()
    if error:
        return jsonify({"error": error[0]}), error[1]

    data = request.get_json()

    old_password = data.get("old_password", "")
    new_password = data.get("new_password", "")

    if not old_password:
        return jsonify({"error": "请输入原密码"}), 400

    if not new_password or len(new_password) < 6:
        return jsonify({"error": "新密码至少需要6个字符"}), 400

    if not verify_password(old_password, user.password_hash):
        return jsonify({"error": "原密码错误"}), 401

    from database import db

    # 若密码哈希使用旧迭代次数（100k），登录时自动升级到 600k
    user.password_hash = hash_password(new_password)
    user.updated_at = datetime.now(timezone.utc)

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        current_app.logger.error("密码修改失败", exc_info=True)
        return jsonify({"error": "密码修改失败，请稍后重试"}), 500

    # 加入黑名单使旧 token 失效
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        add_to_blacklist(auth_header[7:])

    return jsonify({"success": True, "message": "密码修改成功，请重新登录"}), 200


# 验证token的装饰器
import functools


def token_required(f):
    """验证token装饰器，使用 functools.wraps 保留原函数名以避免 Flask 端点冲突"""

    @functools.wraps(f)
    def decorated(*args, **kwargs):
        user, error = _get_user_from_token()
        if error:
            return jsonify({"error": error[0]}), error[1]
        request.current_user = user
        request.user_id = user.id
        return f(*args, **kwargs)

    return decorated


# 角色权限检查装饰器（不内嵌 token_required，调用方需自行确保已认证）
def role_required(*roles):
    """角色权限装饰器"""

    def decorator(f):
        @functools.wraps(f)
        def decorated(*args, **kwargs):
            user = request.current_user
            if not user:
                return jsonify({"error": "请先登录"}), 401
            if user.role not in roles:
                return jsonify({"error": "权限不足"}), 403
            request.user_role = user.role
            return f(*args, **kwargs)

        return decorated

    return decorator
