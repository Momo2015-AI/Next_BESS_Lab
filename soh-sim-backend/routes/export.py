"""
导出功能相关API路由
支持CSV、PNG图表导出
"""
import csv
import io
import json
from datetime import datetime
from flask import Blueprint, request, jsonify, make_response
from database import db, Simulation, SohRteData, Project

export_bp = Blueprint('export', __name__)


@export_bp.route('/api/export/csv', methods=['POST'])
def export_csv():
    """
    导出计算结果为CSV格式
    支持导出25年矩阵数据、SOH数据、财务数据等
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'error': '无效的请求数据'}), 400
    
    export_type = data.get('type', 'matrix')  # matrix/soh/financial/all
    results = data.get('results', {})
    params = data.get('params', {})
    soh = data.get('soh', [])
    rte = data.get('rte', [])
    dod = data.get('dod', [])
    aug_qty = data.get('augQty', [])
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # 写入标题
    writer.writerow(['储能电站SOH仿真计算结果导出'])
    writer.writerow(['导出时间', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
    writer.writerow([])
    
    if export_type == 'matrix' or export_type == 'all':
        # 导出25年生命周期矩阵
        writer.writerow(['25年生命周期矩阵'])
        writer.writerow(['年份', '初始Gross(MWh)', '初始Aux(MWh)', '初始净可用(MWh)', 
                        '扩容Gross(MWh)', '扩容Aux(MWh)', '扩容净可用(MWh)', 
                        '总净可用(MWh)', '累计扩容数量', '是否满足需求'])
        
        N = 26
        for i in range(N):
            writer.writerow([
                i,
                round(results.get('initGross', [0]*N)[i], 4) if i < len(results.get('initGross', [])) else 0,
                round(results.get('initAux', [0]*N)[i], 4) if i < len(results.get('initAux', [])) else 0,
                round(results.get('initAcUsable', [0]*N)[i], 4) if i < len(results.get('initAcUsable', [])) else 0,
                round(results.get('augGross', [0]*N)[i], 4) if i < len(results.get('augGross', [])) else 0,
                round(results.get('augAux', [0]*N)[i], 4) if i < len(results.get('augAux', [])) else 0,
                round(results.get('augAcUsable', [0]*N)[i], 4) if i < len(results.get('augAcUsable', [])) else 0,
                round(results.get('totalAcUsable', [0]*N)[i], 4) if i < len(results.get('totalAcUsable', [])) else 0,
                int(results.get('augAccumQty', [0]*N)[i]) if i < len(results.get('augAccumQty', [])) else 0,
                '是' if results.get('meetsReq', [False]*N)[i] else '否' if i < len(results.get('meetsReq', [])) else ''
            ])
    
    if export_type == 'soh' or export_type == 'all':
        # 导出SOH/RTE数据
        writer.writerow([])
        writer.writerow(['SOH/RTE数据序列'])
        writer.writerow(['年份', 'SOH(%)', 'RTE(%)', 'DOD(%)', '扩容数量'])
        
        N = max(len(soh), len(rte), len(dod), len(aug_qty), 26)
        for i in range(N):
            writer.writerow([
                i,
                round(float(soh[i]) * 100, 2) if i < len(soh) and soh[i] is not None else 0.0,
                round(float(rte[i]) * 100, 2) if i < len(rte) and rte[i] is not None else 0.0,
                round(float(dod[i]), 2) if i < len(dod) and dod[i] is not None else 0.0,
                int(aug_qty[i]) if i < len(aug_qty) and aug_qty[i] is not None else 0
            ])
    
    if export_type == 'params' or export_type == 'all':
        # 导出参数配置
        writer.writerow([])
        writer.writerow(['参数配置'])
        writer.writerow(['参数名称', '参数值', '单位'])
        
        param_mapping = {
            'ratedEnergy': ('额定能量', 'MWh'),
            'initContainerQty': ('初始集装箱数量', '个'),
            'initPcsQty': ('初始PCS数量', '个'),
            'duration': ('储能时长', 'h'),
            'cyclesPerDay': ('每日循环次数', '次'),
            'acEfficiency': ('交流效率', '%'),
            'bessAuxRun': ('BESS运行辅助功耗', 'kW'),
            'bessAuxStandby': ('BESS待机辅助功耗', 'kW'),
            'pcsAuxRun': ('PCS运行辅助功耗', 'kW'),
            'pcsAuxStandby': ('PCS待机辅助功耗', 'kW'),
            'requiredEnergy': ('需求能量', 'MWh'),
        }
        
        for key, (label, unit) in param_mapping.items():
            value = params.get(key, '')
            if value != '':
                writer.writerow([label, value, unit])
    
    # 生成响应
    output.seek(0)
    response = make_response(output.getvalue())
    response.headers['Content-Type'] = 'text/csv; charset=utf-8-sig'
    response.headers['Content-Disposition'] = f'attachment; filename=soh_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    
    return response


@export_bp.route('/api/export/financial-csv', methods=['POST'])
def export_financial_csv():
    """
    导出财务分析结果为CSV格式
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'error': '无效的请求数据'}), 400
    
    cashflow = data.get('cashflow', [])
    metrics = data.get('metrics', {})
    params = data.get('params', {})
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # 写入标题
    writer.writerow(['储能电站财务分析结果'])
    writer.writerow(['导出时间', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
    writer.writerow([])
    
    # 写入财务指标
    writer.writerow(['财务指标汇总'])
    writer.writerow(['指标名称', '数值', '单位'])
    
    metrics_mapping = {
        'totalRevenue': ('25年总收入', '$'),
        'totalCost': ('25年总成本', '$'),
        'netCashflow': ('25年净现金流', '$'),
        'npv': ('净现值(NPV)', '$'),
        'irr': ('内部收益率(IRR)', '%'),
        'paybackYears': ('投资回收期', '年'),
        'lcos': ('储能度电成本(LCOS)', '$/MWh'),
    }
    
    for key, (label, unit) in metrics_mapping.items():
        value = metrics.get(key, '')
        if value != '':
            writer.writerow([label, round(float(value), 2), unit])
    
    # 写入现金流
    if cashflow:
        writer.writerow([])
        writer.writerow(['25年现金流明细'])
        writer.writerow(['年份', '收入', '成本', '净现金流', '累计现金流'])
        
        for i, cf in enumerate(cashflow):
            writer.writerow([
                i,
                round(cf.get('revenue', 0), 2),
                round(cf.get('cost', 0), 2),
                round(cf.get('net', 0), 2),
                round(cf.get('cumulative', 0), 2),
            ])
    
    # 生成响应
    output.seek(0)
    response = make_response(output.getvalue())
    response.headers['Content-Type'] = 'text/csv; charset=utf-8-sig'
    response.headers['Content-Disposition'] = f'attachment; filename=financial_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    
    return response


@export_bp.route('/api/export/simulation', methods=['POST'])
def export_simulation():
    """
    导出完整仿真结果（包含所有数据）
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'error': '无效的请求数据'}), 400
    
    # 保存仿真结果到数据库
    project_id = data.get('project_id')
    simulation_id = data.get('simulation_id')
    
    simulation_data = {
        'params': data.get('params', {}),
        'results': data.get('results', {}),
        'soh': data.get('soh', []),
        'rte': data.get('rte', []),
        'dod': data.get('dod', []),
        'aug_qty': data.get('augQty', []),
        'financial': data.get('financial', {}),
    }
    
    # 如果有simulation_id，更新记录
    if simulation_id:
        simulation = Simulation.query.get(simulation_id)
        if simulation:
            simulation.results = json.dumps(simulation_data)
            simulation.status = 'completed'
            simulation.completed_at = datetime.utcnow()
            db.session.commit()
            return jsonify({
                'success': True,
                'simulation_id': simulation_id,
                'message': '仿真结果已更新'
            })
    
    # 创建新仿真记录
    import uuid
    new_simulation_id = str(uuid.uuid4())
    
    simulation = Simulation(
        id=new_simulation_id,
        project_id=project_id,
        name=data.get('name', f'仿真_{datetime.now().strftime("%Y%m%d_%H%M%S")}'),
        algorithm_type=data.get('algorithm_type', 'arrhenius'),
        duration_years=data.get('duration_years', 25),
        correction_factor=data.get('correction_factor', 1.0),
        input_params=json.dumps(data.get('params', {})),
        results=json.dumps(simulation_data),
        status='completed',
        completed_at=datetime.utcnow()
    )
    
    db.session.add(simulation)
    
    try:
        db.session.commit()
        return jsonify({
            'success': True,
            'simulation_id': new_simulation_id,
            'message': '仿真结果已保存'
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'保存失败: {str(e)}'}), 500


@export_bp.route('/api/simulation/list', methods=['GET'])
def list_simulations():
    """获取仿真列表"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    project_id = request.args.get('project_id')
    
    query = Simulation.query
    if project_id:
        query = query.filter(Simulation.project_id == project_id)
    
    pagination = query.order_by(Simulation.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'simulations': [{
            'id': s.id,
            'name': s.name,
            'algorithm_type': s.algorithm_type,
            'status': s.status,
            'created_at': s.created_at.isoformat() if s.created_at else None,
            'completed_at': s.completed_at.isoformat() if s.completed_at else None,
        } for s in pagination.items],
        'total': pagination.total,
        'page': page,
        'per_page': per_page,
        'pages': pagination.pages
    }), 200


@export_bp.route('/api/simulation/<simulation_id>', methods=['GET'])
def get_simulation(simulation_id):
    """获取仿真详情"""
    simulation = Simulation.query.get(simulation_id)
    if not simulation:
        return jsonify({'error': '仿真不存在'}), 404
    
    result = {
        'id': simulation.id,
        'name': simulation.name,
        'description': simulation.description,
        'algorithm_type': simulation.algorithm_type,
        'duration_years': simulation.duration_years,
        'correction_factor': simulation.correction_factor,
        'status': simulation.status,
        'created_at': simulation.created_at.isoformat() if simulation.created_at else None,
        'completed_at': simulation.completed_at.isoformat() if simulation.completed_at else None,
    }
    
    if simulation.input_params:
        result['params'] = json.loads(simulation.input_params)
    
    if simulation.results:
        result['results'] = json.loads(simulation.results)
    
    return jsonify(result), 200