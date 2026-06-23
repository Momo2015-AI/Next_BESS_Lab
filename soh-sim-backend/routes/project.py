"""
项目与版本管理API路由
支持项目CRUD、版本管理（另存为）、方案配置
"""
import uuid
import json
from datetime import datetime
from flask import Blueprint, request, jsonify, current_app
from routes.auth import token_required, role_required

project_bp = Blueprint('project', __name__)


# ==================== 项目API ====================

@project_bp.route('/api/projects', methods=['GET'])
@token_required
def get_projects():
    """获取项目列表"""
    user_id = request.user_id
    
    from database import db, Project, User
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': '用户不存在'}), 404
    
    # 根据角色筛选项目
    query = Project.query
    
    # 客户只能看到自己的项目
    if user.role == 'customer':
        query = query.filter(Project.customer_id == user_id)
    
    # 按更新时间倒序
    projects = query.order_by(Project.updated_at.desc()).all()
    
    return jsonify({
        'success': True,
        'data': [{
            'id': p.id,
            'name': p.name,
            'code': p.code,
            'status': p.status,
            'stage': p.stage,
            'customer_id': p.customer_id,
            'created_at': p.created_at.isoformat() if p.created_at else None,
            'updated_at': p.updated_at.isoformat() if p.updated_at else None,
        } for p in projects]
    })


@project_bp.route('/api/projects', methods=['POST'])
@token_required
def create_project():
    """创建项目"""
    user_id = request.user_id
    data = request.get_json()
    
    if not data:
        return jsonify({'error': '无效的请求数据'}), 400
    
    name = data.get('name', '').strip()
    if not name:
        return jsonify({'error': '项目名称不能为空'}), 400
    
    from database import db, Project, User, ProjectVersion
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': '用户不存在'}), 404
    
    # 检查权限（客户不能创建项目）
    if user.role == 'customer':
        return jsonify({'error': '权限不足，客户不能创建项目'}), 403
    
    project_id = str(uuid.uuid4())
    project = Project(
        id=project_id,
        name=name,
        code=data.get('code'),
        tenant_id=user.tenant_id,
        customer_id=data.get('customer_id'),
        status='active',
        stage='survey',
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    
    db.session.add(project)
    
    try:
        db.session.commit()
        
        # 自动创建第一个版本
        version = ProjectVersion(
            id=str(uuid.uuid4()),
            project_id=project_id,
            version_num=1,
            name='方案v1',
            description='初始版本',
            is_active=True,
            created_by=user_id,
            status='draft',
            created_at=datetime.utcnow(),
        )
        db.session.add(version)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'id': project_id,
            'version_id': version.id,
            'message': '项目创建成功'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'创建失败: {str(e)}'}), 500


@project_bp.route('/api/projects/<project_id>', methods=['GET'])
@token_required
def get_project(project_id):
    """获取项目详情"""
    user_id = request.user_id
    
    from database import db, Project, User, ProjectVersion
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': '用户不存在'}), 404
    
    project = Project.query.get(project_id)
    if not project:
        return jsonify({'error': '项目不存在'}), 404
    
    # 检查权限
    if user.role == 'customer' and project.customer_id != user_id:
        return jsonify({'error': '权限不足'}), 403
    
    # 获取所有版本
    versions = ProjectVersion.query.filter_by(project_id=project_id)\
        .order_by(ProjectVersion.version_num.desc()).all()
    
    return jsonify({
        'success': True,
        'data': {
            'id': project.id,
            'name': project.name,
            'code': project.code,
            'status': project.status,
            'stage': project.stage,
            'customer_id': project.customer_id,
            'config': json.loads(project.config) if project.config else None,
            'created_at': project.created_at.isoformat() if project.created_at else None,
            'updated_at': project.updated_at.isoformat() if project.updated_at else None,
            'versions': [{
                'id': v.id,
                'version_num': v.version_num,
                'name': v.name,
                'description': v.description,
                'is_active': v.is_active,
                'status': v.status,
                'created_by': v.created_by,
                'created_at': v.created_at.isoformat() if v.created_at else None,
            } for v in versions]
        }
    })


@project_bp.route('/api/projects/<project_id>', methods=['PUT'])
@token_required
def update_project(project_id):
    """更新项目"""
    user_id = request.user_id
    data = request.get_json()
    
    from database import db, Project, User
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': '用户不存在'}), 404
    
    # 检查权限（客户不能更新项目）
    if user.role == 'customer':
        return jsonify({'error': '权限不足'}), 403
    
    project = Project.query.get(project_id)
    if not project:
        return jsonify({'error': '项目不存在'}), 404
    
    # 更新字段
    if 'name' in data:
        project.name = data['name']
    if 'code' in data:
        project.code = data['code']
    if 'status' in data:
        project.status = data['status']
    if 'stage' in data:
        project.stage = data['stage']
    if 'config' in data:
        project.config = json.dumps(data['config']) if isinstance(data['config'], dict) else data['config']
    
    project.updated_at = datetime.utcnow()
    
    try:
        db.session.commit()
        return jsonify({'success': True, 'message': '项目更新成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'更新失败: {str(e)}'}), 500


@project_bp.route('/api/projects/<project_id>', methods=['DELETE'])
@token_required
@role_required('admin')
def delete_project(project_id):
    """删除项目（仅管理员）"""
    from database import db, Project
    
    project = Project.query.get(project_id)
    if not project:
        return jsonify({'error': '项目不存在'}), 404
    
    try:
        db.session.delete(project)
        db.session.commit()
        return jsonify({'success': True, 'message': '项目删除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'删除失败: {str(e)}'}), 500


# ==================== 版本API ====================

@project_bp.route('/api/projects/<project_id>/versions', methods=['GET'])
@token_required
def get_versions(project_id):
    """获取项目版本列表"""
    user_id = request.user_id
    
    from database import db, Project, ProjectVersion, User
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': '用户不存在'}), 404
    
    project = Project.query.get(project_id)
    if not project:
        return jsonify({'error': '项目不存在'}), 404
    
    # 检查权限
    if user.role == 'customer' and project.customer_id != user_id:
        return jsonify({'error': '权限不足'}), 403
    
    versions = ProjectVersion.query.filter_by(project_id=project_id)\
        .order_by(ProjectVersion.version_num.desc()).all()
    
    return jsonify({
        'success': True,
        'data': [{
            'id': v.id,
            'version_num': v.version_num,
            'name': v.name,
            'description': v.description,
            'is_active': v.is_active,
            'status': v.status,
            'config_data': json.loads(v.config_data) if v.config_data else None,
            'created_by': v.created_by,
            'created_at': v.created_at.isoformat() if v.created_at else None,
        } for v in versions]
    })


@project_bp.route('/api/projects/<project_id>/versions', methods=['POST'])
@token_required
def create_version(project_id):
    """创建新版本（另存为）"""
    user_id = request.user_id
    data = request.get_json()
    
    from database import db, Project, ProjectVersion, User
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': '用户不存在'}), 404
    
    # 检查权限（客户不能创建版本）
    if user.role == 'customer':
        return jsonify({'error': '权限不足'}), 403
    
    project = Project.query.get(project_id)
    if not project:
        return jsonify({'error': '项目不存在'}), 404
    
    # 获取最新版本号
    latest_version = ProjectVersion.query.filter_by(project_id=project_id)\
        .order_by(ProjectVersion.version_num.desc()).first()
    new_version_num = (latest_version.version_num + 1) if latest_version else 1
    
    # 创建新版本
    version_id = str(uuid.uuid4())
    version = ProjectVersion(
        id=version_id,
        project_id=project_id,
        version_num=new_version_num,
        name=data.get('name', f'方案v{new_version_num}'),
        description=data.get('description', ''),
        config_data=data.get('config_data', latest_version.config_data if latest_version else None),
        is_active=True,
        created_by=user_id,
        status='draft',
        created_at=datetime.utcnow(),
    )
    
    # 将之前的活跃版本设为非活跃
    ProjectVersion.query.filter_by(project_id=project_id, is_active=True)\
        .update({'is_active': False})
    
    db.session.add(version)
    
    try:
        db.session.commit()
        return jsonify({
            'success': True,
            'id': version_id,
            'version_num': new_version_num,
            'message': '版本创建成功'
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'创建失败: {str(e)}'}), 500


@project_bp.route('/api/versions/<version_id>', methods=['GET'])
@token_required
def get_version(version_id):
    """获取版本详情"""
    user_id = request.user_id
    
    from database import db, ProjectVersion, User
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': '用户不存在'}), 404
    
    version = ProjectVersion.query.get(version_id)
    if not version:
        return jsonify({'error': '版本不存在'}), 404
    
    return jsonify({
        'success': True,
        'data': {
            'id': version.id,
            'project_id': version.project_id,
            'version_num': version.version_num,
            'name': version.name,
            'description': version.description,
            'is_active': version.is_active,
            'status': version.status,
            'config_data': json.loads(version.config_data) if version.config_data else None,
            'created_by': version.created_by,
            'created_at': version.created_at.isoformat() if version.created_at else None,
            'updated_at': version.updated_at.isoformat() if version.updated_at else None,
        }
    })


@project_bp.route('/api/versions/<version_id>', methods=['PUT'])
@token_required
def update_version(version_id):
    """更新版本配置"""
    user_id = request.user_id
    data = request.get_json()
    
    from database import db, ProjectVersion, User
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': '用户不存在'}), 404
    
    # 检查权限（客户不能更新版本）
    if user.role == 'customer':
        return jsonify({'error': '权限不足'}), 403
    
    version = ProjectVersion.query.get(version_id)
    if not version:
        return jsonify({'error': '版本不存在'}), 404
    
    # 更新字段
    if 'name' in data:
        version.name = data['name']
    if 'description' in data:
        version.description = data['description']
    if 'config_data' in data:
        version.config_data = json.dumps(data['config_data']) if isinstance(data['config_data'], dict) else data['config_data']
    if 'status' in data:
        version.status = data['status']
    if 'is_active' in data:
        if data['is_active']:
            # 将其他版本设为非活跃
            ProjectVersion.query.filter_by(project_id=version.project_id)\
                .filter(ProjectVersion.id != version_id)\
                .update({'is_active': False})
        version.is_active = data['is_active']
    
    version.updated_at = datetime.utcnow()
    
    try:
        db.session.commit()
        return jsonify({'success': True, 'message': '版本更新成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'更新失败: {str(e)}'}), 500


@project_bp.route('/api/versions/<version_id>/activate', methods=['POST'])
@token_required
def activate_version(version_id):
    """激活版本"""
    user_id = request.user_id
    
    from database import db, ProjectVersion, User
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': '用户不存在'}), 404
    
    # 检查权限（客户不能激活版本）
    if user.role == 'customer':
        return jsonify({'error': '权限不足'}), 403
    
    version = ProjectVersion.query.get(version_id)
    if not version:
        return jsonify({'error': '版本不存在'}), 404
    
    # 将其他版本设为非活跃
    ProjectVersion.query.filter_by(project_id=version.project_id)\
        .update({'is_active': False})
    
    version.is_active = True
    version.updated_at = datetime.utcnow()
    
    try:
        db.session.commit()
        return jsonify({'success': True, 'message': '版本激活成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'激活失败: {str(e)}'}), 500


# ==================== 参数同步API ====================

@project_bp.route('/api/project/sync-params', methods=['POST'])
def sync_params():
    """同步参数到数据库"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': '无效的请求数据'}), 400
    
    project_id = data.get('project_id')
    params_data = data.get('params')
    soh_data = data.get('soh')
    rte_data = data.get('rte')
    dod_data = data.get('dod')
    aug_qty_data = data.get('augQty')
    
    from database import db, Project, ProjectVersion, SohRteData
    
    try:
        if project_id:
            project = Project.query.get(project_id)
            if project:
                config = json.loads(project.config) if project.config else {}
                config['params'] = params_data
                config['soh'] = soh_data
                config['rte'] = rte_data
                config['dod'] = dod_data
                config['augQty'] = aug_qty_data
                project.config = json.dumps(config)
                project.updated_at = datetime.utcnow()
                db.session.commit()
        
        soh_rte_record = SohRteData.query.first()
        if soh_rte_record:
            soh_rte_record.soh_values = json.dumps(soh_data) if soh_data else None
            soh_rte_record.rte_values = json.dumps(rte_data) if rte_data else None
            soh_rte_record.dod_values = json.dumps(dod_data) if dod_data else None
            soh_rte_record.aug_qty_values = json.dumps(aug_qty_data) if aug_qty_data else None
            soh_rte_record.updated_at = datetime.utcnow()
        else:
            soh_rte_record = SohRteData(
                id=str(uuid.uuid4()),
                soh_values=json.dumps(soh_data) if soh_data else None,
                rte_values=json.dumps(rte_data) if rte_data else None,
                dod_values=json.dumps(dod_data) if dod_data else None,
                aug_qty_values=json.dumps(aug_qty_data) if aug_qty_data else None,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            db.session.add(soh_rte_record)
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': '参数同步成功'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'同步失败: {str(e)}'}), 500
