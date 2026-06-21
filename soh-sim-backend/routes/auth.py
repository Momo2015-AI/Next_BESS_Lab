"""
用户认证相关API路由
支持注册、登录、JWT token验证
"""
import uuid
import hashlib
import secrets
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify, current_app
import jwt

auth_bp = Blueprint('auth', __name__)


def hash_password(password, salt=None):
    """密码哈希"""
    if salt is None:
        salt = secrets.token_hex(16)
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
    return f"{salt}${hashed.hex()}"


def verify_password(password, hashed):
    """验证密码"""
    try:
        salt, _ = hashed.split('$')
        return hash_password(password, salt) == hashed
    except:
        return False


def generate_token(user_id, secret_key, expires_in=24):
    """生成JWT token"""
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=expires_in),
        'iat': datetime.utcnow(),
    }
    return jwt.encode(payload, secret_key, algorithm='HS256')


def decode_token(token, secret_key):
    """解码JWT token"""
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


@auth_bp.route('/api/auth/register', methods=['POST'])
def register():
    """
    用户注册
    支持角色: customer(客户) / engineer(工程师) / admin(管理员)
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'error': '无效的请求数据'}), 400
    
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')
    role = data.get('role', 'customer')  # 默认客户角色
    tenant_id = data.get('tenant_id')  # 可选，关联租户
    
    # 验证必填字段
    if not username or len(username) < 3:
        return jsonify({'error': '用户名至少需要3个字符'}), 400
    
    if not email or '@' not in email:
        return jsonify({'error': '请输入有效的邮箱地址'}), 400
    
    if not password or len(password) < 6:
        return jsonify({'error': '密码至少需要6个字符'}), 400
    
    # 验证角色
    valid_roles = ['customer', 'engineer', 'admin']
    if role not in valid_roles:
        return jsonify({'error': f'无效的角色，可选值: {", ".join(valid_roles)}'}), 400
    
    # 检查用户是否已存在
    from database import User
    existing_user = User.query.filter(
        (User.username == username) | (User.email == email)
    ).first()
    
    if existing_user:
        return jsonify({'error': '用户名或邮箱已存在'}), 409
    
    # 创建用户
    from database import db
    user_id = str(uuid.uuid4())
    
    user = User(
        id=user_id,
        username=username,
        email=email,
        password_hash=hash_password(password),
        tenant_id=tenant_id,
        role=role,  # 用户选择的角色
        is_active=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    
    db.session.add(user)
    
    try:
        db.session.commit()
        
        # 生成token
        secret_key = current_app.config.get('SECRET_KEY', 'your-secret-key-change-in-production')
        token = generate_token(user_id, secret_key)
        
        return jsonify({
            'success': True,
            'message': '注册成功',
            'token': token,
            'user': {
                'id': user_id,
                'username': username,
                'email': email,
                'role': role,
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'注册失败: {str(e)}'}), 500


@auth_bp.route('/api/auth/login', methods=['POST'])
def login():
    """
    用户登录
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'error': '无效的请求数据'}), 400
    
    username = data.get('username', '').strip()
    password = data.get('password', '')
    
    if not username or not password:
        return jsonify({'error': '请输入用户名和密码'}), 400
    
    # 查找用户
    from database import User
    user = User.query.filter(
        (User.username == username) | (User.email == username)
    ).first()
    
    if not user:
        return jsonify({'error': '用户名或密码错误'}), 401
    
    if not user.is_active:
        return jsonify({'error': '账号已被禁用'}), 403
    
    # 验证密码
    if not verify_password(password, user.password_hash):
        return jsonify({'error': '用户名或密码错误'}), 401
    
    # 更新最后登录时间
    user.last_login = datetime.utcnow()
    user.login_count = (user.login_count or 0) + 1
    
    try:
        from database import db
        db.session.commit()
    except:
        pass
    
    # 生成token
    secret_key = current_app.config.get('SECRET_KEY', 'your-secret-key-change-in-production')
    token = generate_token(user.id, secret_key)
    
    return jsonify({
        'success': True,
        'message': '登录成功',
        'token': token,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'tenant_id': user.tenant_id,
        }
    }), 200


@auth_bp.route('/api/auth/logout', methods=['POST'])
def logout():
    """
    用户登出（前端清除token即可）
    """
    return jsonify({
        'success': True,
        'message': '已退出登录'
    }), 200


@auth_bp.route('/api/auth/me', methods=['GET'])
def get_current_user():
    """
    获取当前用户信息
    """
    auth_header = request.headers.get('Authorization', '')
    
    if not auth_header.startswith('Bearer '):
        return jsonify({'error': '未提供认证token'}), 401
    
    token = auth_header[7:]
    secret_key = current_app.config.get('SECRET_KEY', 'your-secret-key-change-in-production')
    payload = decode_token(token, secret_key)
    
    if not payload:
        return jsonify({'error': 'token已失效'}), 401
    
    user_id = payload.get('user_id')
    
    from database import User
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': '用户不存在'}), 404
    
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role,
        'tenant_id': user.tenant_id,
        'is_active': user.is_active,
        'created_at': user.created_at.isoformat() if user.created_at else None,
        'last_login': user.last_login.isoformat() if user.last_login else None,
    }), 200


@auth_bp.route('/api/auth/refresh', methods=['POST'])
def refresh_token():
    """
    刷新token
    """
    auth_header = request.headers.get('Authorization', '')
    
    if not auth_header.startswith('Bearer '):
        return jsonify({'error': '未提供认证token'}), 401
    
    token = auth_header[7:]
    secret_key = current_app.config.get('SECRET_KEY', 'your-secret-key-change-in-production')
    payload = decode_token(token, secret_key)
    
    if not payload:
        return jsonify({'error': 'token已失效'}), 401
    
    user_id = payload.get('user_id')
    new_token = generate_token(user_id, secret_key)
    
    return jsonify({
        'success': True,
        'token': new_token,
    }), 200


@auth_bp.route('/api/auth/change-password', methods=['POST'])
def change_password():
    """
    修改密码
    """
    auth_header = request.headers.get('Authorization', '')
    
    if not auth_header.startswith('Bearer '):
        return jsonify({'error': '未提供认证token'}), 401
    
    token = auth_header[7:]
    secret_key = current_app.config.get('SECRET_KEY', 'your-secret-key-change-in-production')
    payload = decode_token(token, secret_key)
    
    if not payload:
        return jsonify({'error': 'token已失效'}), 401
    
    data = request.get_json()
    user_id = payload.get('user_id')
    
    old_password = data.get('old_password', '')
    new_password = data.get('new_password', '')
    
    if not new_password or len(new_password) < 6:
        return jsonify({'error': '新密码至少需要6个字符'}), 400
    
    from database import User, db
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': '用户不存在'}), 404
    
    # 验证旧密码（必须提供且正确）
    if not old_password:
        return jsonify({'error': '请输入原密码'}), 400
    
    if not verify_password(old_password, user.password_hash):
        return jsonify({'error': '原密码错误'}), 401
    
    # 更新密码
    user.password_hash = hash_password(new_password)
    user.updated_at = datetime.utcnow()
    
    try:
        db.session.commit()
        return jsonify({'success': True, 'message': '密码修改成功'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'密码修改失败: {str(e)}'}), 500


# 中间件：验证token的装饰器
def token_required(f):
    """验证token装饰器"""
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        
        if not auth_header.startswith('Bearer '):
            return jsonify({'error': '未提供认证token'}), 401
        
        token = auth_header[7:]
        secret_key = current_app.config.get('SECRET_KEY')
        
        if not secret_key:
            current_app.logger.error('SECRET_KEY not configured!')
            return jsonify({'error': '服务器配置错误'}), 500
        
        payload = decode_token(token, secret_key)
        
        if not payload:
            return jsonify({'error': 'token已失效'}), 401
        
        # 将user_id添加到请求中
        request.user_id = payload.get('user_id')
        return f(*args, **kwargs)
    
    decorated.__name__ = f.__name__
    return decorated


# 角色权限检查装饰器（复用token_required）
def role_required(*roles):
    """角色权限装饰器"""
    def decorator(f):
        @token_required
        def decorated(*args, **kwargs):
            user_id = request.user_id
            
            from database import User
            user = User.query.get(user_id)
            
            if not user:
                return jsonify({'error': '用户不存在'}), 404
            
            if user.role not in roles:
                return jsonify({'error': '权限不足'}), 403
            
            request.user_role = user.role
            return f(*args, **kwargs)
        
        decorated.__name__ = f.__name__
        return decorated
    return decorator