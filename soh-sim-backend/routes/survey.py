"""
调研表相关API路由
"""
import uuid
import json
from datetime import datetime
from flask import Blueprint, request, jsonify
from database import db, Survey, Project

survey_bp = Blueprint('survey', __name__)


@survey_bp.route('/api/survey/submit', methods=['POST'])
def submit_survey():
    """
    提交调研表
    无需登录，自动生成UUID，并创建关联项目
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': '无效的请求数据'}), 400
    
    # 生成UUID
    survey_id = str(uuid.uuid4())
    project_id = str(uuid.uuid4())
    project_code = f"PRJ-{datetime.now().strftime('%Y%m%d')}-{project_id[:8].upper()}"

    # 先创建项目（被调研表外键引用，需先存在）
    project = Project(
        id=project_id,
        name=data.get('project_name', '未命名项目'),
        code=project_code,
        status='draft',
        stage='survey',
        config=json.dumps({
            'survey_id': survey_id,
            'created_from': 'survey',
            'basic_params': {
                'total_mw': data.get('total_mw'),
                'total_mwh': data.get('total_mwh'),
                'duration': data.get('duration'),
                'location': data.get('location')
            }
        })
    )
    db.session.add(project)

    # 再创建调研表并直接绑定项目（project_id 始终有效）
    survey = Survey(
        id=survey_id,
        project_name=data.get('project_name'),
        contact_person=data.get('contact_person'),
        contact_phone=data.get('contact_phone'),
        contact_email=data.get('contact_email'),
        location=data.get('location'),
        altitude=data.get('altitude'),
        total_mw=data.get('total_mw'),
        total_mwh=data.get('total_mwh'),
        duration=data.get('duration'),
        cycles_per_day=data.get('cycles_per_day', 1.0),
        temp_max=data.get('temp_max'),
        temp_min=data.get('temp_min'),
        temp_avg=data.get('temp_avg'),
        humidity=data.get('humidity'),
        grid_voltage=data.get('grid_voltage'),
        grid_frequency=data.get('grid_frequency'),
        rte_target=data.get('rte_target'),
        soh_year1=data.get('soh_year1'),
        soh_year25=data.get('soh_year25'),
        calendar_life=data.get('calendar_life'),
        cycle_life=data.get('cycle_life'),
        availability_target=data.get('availability_target'),
        aux_consumption=data.get('aux_consumption'),
        response_time=data.get('response_time'),
        dc_voltage_range=data.get('dc_voltage_range'),
        ac_voltage=data.get('ac_voltage'),
        thdi=data.get('thdi'),
        remarks=data.get('remarks'),
        attachments=json.dumps(data.get('attachments', [])),
        status='pending',
        project_id=project_id
    )
    db.session.add(survey)

    try:
        db.session.commit()
        return jsonify({
            'success': True,
            'survey_id': survey_id,
            'project_id': project_id,
            'project_code': project_code,
            'message': '调研表提交成功，项目已自动创建'
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'提交失败: {str(e)}'}), 500


@survey_bp.route('/api/survey/<survey_id>', methods=['GET'])
def get_survey(survey_id):
    """获取调研表详情"""
    survey = Survey.query.get(survey_id)
    if not survey:
        return jsonify({'error': '调研表不存在'}), 404
    
    result = survey.to_dict()
    if survey.project:
        result['project'] = survey.project.to_dict()
    
    return jsonify(result), 200


@survey_bp.route('/api/survey/list', methods=['GET'])
def list_surveys():
    """获取调研表列表"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    status = request.args.get('status')
    keyword = request.args.get('keyword')
    
    query = Survey.query
    if status:
        query = query.filter(Survey.status == status)
    if keyword:
        query = query.filter(Survey.project_name.ilike(f'%{keyword}%'))
    
    pagination = query.order_by(Survey.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'surveys': [s.to_dict() for s in pagination.items],
        'total': pagination.total,
        'page': page,
        'per_page': per_page,
        'pages': pagination.pages
    }), 200


@survey_bp.route('/api/survey/search', methods=['GET'])
def search_survey():
    """通过项目名称搜索调研表"""
    keyword = request.args.get('keyword', '')
    
    if not keyword:
        return jsonify({'error': '请输入搜索关键词'}), 400
    
    surveys = Survey.query.filter(Survey.project_name.ilike(f'%{keyword}%')).limit(10).all()
    
    return jsonify({
        'success': True,
        'surveys': [s.to_dict() for s in surveys]
    }), 200


@survey_bp.route('/api/survey/<survey_id>', methods=['PUT'])
def update_survey(survey_id):
    """更新调研表"""
    survey = Survey.query.get(survey_id)
    if not survey:
        return jsonify({'error': '调研表不存在'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': '无效的请求数据'}), 400
    
    # 更新字段
    updatable_fields = [
        'project_name', 'contact_person', 'contact_phone', 'contact_email',
        'location', 'altitude', 'total_mw', 'total_mwh', 'duration',
        'cycles_per_day', 'temp_max', 'temp_min', 'temp_avg', 'humidity',
        'grid_voltage', 'grid_frequency', 'rte_target', 'soh_year1', 'soh_year25',
        'calendar_life', 'cycle_life', 'availability_target', 'aux_consumption',
        'response_time', 'dc_voltage_range', 'ac_voltage', 'thdi', 'remarks', 'status'
    ]
    
    for field in updatable_fields:
        if field in data:
            setattr(survey, field, data[field])
    
    if 'attachments' in data:
        survey.attachments = json.dumps(data['attachments'])
    
    survey.updated_at = datetime.utcnow()
    
    try:
        db.session.commit()
        return jsonify({
            'success': True,
            'survey': survey.to_dict(),
            'message': '调研表更新成功'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'更新失败: {str(e)}'}), 500


@survey_bp.route('/api/survey/<survey_id>', methods=['DELETE'])
def delete_survey(survey_id):
    """删除调研表"""
    survey = Survey.query.get(survey_id)
    if not survey:
        return jsonify({'error': '调研表不存在'}), 404
    
    try:
        db.session.delete(survey)
        db.session.commit()
        return jsonify({'success': True, 'message': '调研表已删除'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'删除失败: {str(e)}'}), 500


@survey_bp.route('/api/project/<project_id>', methods=['GET'])
def get_project(project_id):
    """获取项目详情"""
    project = Project.query.get(project_id)
    if not project:
        return jsonify({'error': '项目不存在'}), 404
    
    result = project.to_dict()
    result['surveys'] = [s.to_dict() for s in project.surveys]
    
    return jsonify(result), 200


@survey_bp.route('/api/project/list', methods=['GET'])
def list_projects():
    """获取项目列表"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    status = request.args.get('status')
    stage = request.args.get('stage')
    
    query = Project.query
    if status:
        query = query.filter(Project.status == status)
    if stage:
        query = query.filter(Project.stage == stage)
    
    pagination = query.order_by(Project.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'projects': [p.to_dict() for p in pagination.items],
        'total': pagination.total,
        'page': page,
        'per_page': per_page,
        'pages': pagination.pages
    }), 200


@survey_bp.route('/api/project/<project_id>', methods=['PUT'])
def update_project(project_id):
    """更新项目"""
    project = Project.query.get(project_id)
    if not project:
        return jsonify({'error': '项目不存在'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': '无效的请求数据'}), 400

    if 'name' in data:
        project.name = data['name']
    if 'status' in data:
        project.status = data['status']
    if 'stage' in data:
        project.stage = data['stage']
    if 'config' in data:
        project.config = json.dumps(data['config'])

    project.updated_at = datetime.utcnow()

    try:
        db.session.commit()
        return jsonify({
            'success': True,
            'project': project.to_dict(),
            'message': '项目更新成功'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'更新失败: {str(e)}'}), 500


@survey_bp.route('/api/project/<project_id>', methods=['DELETE'])
def delete_project(project_id):
    """删除项目（级联删除关联调研表）

    仅级联 Survey，其他关联实体（Simulation/FinancialData 等）暂不级联，
    避免误删大量历史数据。如需清理，单独调用各自删除接口。
    """
    project = Project.query.get(project_id)
    if not project:
        return jsonify({'error': '项目不存在'}), 404

    try:
        # 级联删除关联调研表
        Survey.query.filter_by(project_id=project_id).delete()
        db.session.delete(project)
        db.session.commit()
        return jsonify({
            'success': True,
            'message': '项目及关联调研表已删除'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'删除失败: {str(e)}'}), 500