"""用户业务逻辑服务层

提供注册、登录、密码修改等核心用户操作，供 routes/auth.py 调用。
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy.exc import IntegrityError

from database import Tenant, User, db
from routes.auth import generate_token, hash_password, verify_password


def register_user(username, email, password):
    """注册新用户。

    Args:
        username: 用户名（已通过 _validate_username 校验）
        email: 邮箱（已校验格式）
        password: 明文密码（已校验长度 >=6）

    Returns:
        (user_dict_or_none, error_or_none, status_code)
    """
    # 检查用户是否已存在
    existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
    if existing_user:
        return None, "用户名或邮箱已存在", 409

    user_id = str(uuid.uuid4())

    user = User(
        id=user_id,
        username=username,
        email=email,
        password_hash=hash_password(password),
        tenant_id="00000000-0000-0000-0000-000000000001",
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
        return None, "用户名或邮箱已存在", 409
    except Exception:
        db.session.rollback()
        return None, "注册失败，请稍后重试", 500

    token = generate_token(user_id)

    return {
        "token": token,
        "user": {
            "id": user_id,
            "username": username,
            "email": email,
            "role": "user",
        },
    }, None, 201


def authenticate_user(username, password):
    """验证用户登录。

    Args:
        username: 用户名或邮箱
        password: 明文密码

    Returns:
        (user_dict_or_none, error_or_none, status_code)
    """
    user = User.query.filter((User.username == username) | (User.email == username)).first()

    if not user:
        return None, "用户名或密码错误", 401

    if not user.is_active:
        return None, "用户名或密码错误", 401

    if not verify_password(password, user.password_hash):
        return None, "用户名或密码错误", 401

    # 更新登录记录
    user.last_login = datetime.now(timezone.utc)
    user.login_count = (user.login_count or 0) + 1

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()

    token = generate_token(user.id)

    return {
        "token": token,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "tenant_id": user.tenant_id,
        },
    }, None, 200


def change_user_password(user, old_password, new_password):
    """修改用户密码。

    Args:
        user: User 模型实例
        old_password: 原密码
        new_password: 新密码

    Returns:
        (success_bool, error_or_none, status_code)
    """
    if not old_password:
        return False, "请输入原密码", 400

    if not new_password or len(new_password) < 6:
        return False, "新密码至少需要6个字符", 400

    if not verify_password(old_password, user.password_hash):
        return False, "原密码错误", 401

    user.password_hash = hash_password(new_password)
    user.updated_at = datetime.now(timezone.utc)

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return False, "密码修改失败，请稍后重试", 500

    return True, None, 200
