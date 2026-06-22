"""
产品库API路由
支持电芯库、集装箱库、PCS库的CRUD操作
"""
import uuid
import json
from datetime import datetime
from flask import Blueprint, request, jsonify
from database import db, CellLibrary, ContainerLibrary, PCS_LIBRARY

library_bp = Blueprint('library', __name__)


# ==================== 电芯库API ====================

@library_bp.route('/api/library/cells', methods=['GET'])
def get_cells():
    """获取电芯列表"""
    try:
        cells = CellLibrary.query.order_by(CellLibrary.created_at.desc()).all()
        return jsonify({
            'success': True,
            'data': [{
                'id': c.id,
                'model': c.model,
                'mfr': c.mfr,
                'chemistry': c.chemistry,
                'capacityAh': c.capacity_ah,
                'voltageNominal': c.voltage_nominal,
                'voltageMax': c.voltage_max,
                'voltageMin': c.voltage_min,
                'energyWh': c.energy_wh,
                'cycleLife': c.cycle_life,
                'calendarLife': c.calendar_life,
                'dimensions': c.dimensions,
                'weight': c.weight,
                'energyDensity': c.energy_density,
                'status': c.status,
                'certifications': json.loads(c.certifications) if c.certifications else [],
                'unitPrice': c.unit_price,
                'remarks': c.remarks,
                'createdAt': c.created_at.isoformat() if c.created_at else None,
            } for c in cells]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@library_bp.route('/api/library/cells', methods=['POST'])
def create_cell():
    """创建电芯"""
    data = request.get_json()
    
    if not data:
        return jsonify({'success': False, 'error': '无效的请求数据'}), 400
    
    cell_id = str(uuid.uuid4())
    cell = CellLibrary(
        id=cell_id,
        model=data.get('model'),
        mfr=data.get('mfr'),
        chemistry=data.get('chemistry', 'LFP'),
        capacity_ah=data.get('capacityAh'),
        voltage_nominal=data.get('voltageNominal'),
        voltage_max=data.get('voltageMax'),
        voltage_min=data.get('voltageMin'),
        energy_wh=data.get('energyWh'),
        cycle_life=data.get('cycleLife'),
        calendar_life=data.get('calendarLife'),
        dimensions=data.get('dimensions'),
        weight=data.get('weight'),
        energy_density=data.get('energyDensity'),
        status=data.get('status', 'mass-production'),
        certifications=json.dumps(data.get('certifications', [])),
        unit_price=data.get('unitPrice'),
        remarks=data.get('remarks'),
    )
    
    try:
        db.session.add(cell)
        db.session.commit()
        return jsonify({'success': True, 'id': cell_id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@library_bp.route('/api/library/cells/<cell_id>', methods=['PUT'])
def update_cell(cell_id):
    """更新电芯"""
    data = request.get_json()
    cell = CellLibrary.query.get(cell_id)
    
    if not cell:
        return jsonify({'success': False, 'error': '电芯不存在'}), 404
    
    # 更新字段
    if 'model' in data:
        cell.model = data['model']
    if 'mfr' in data:
        cell.mfr = data['mfr']
    if 'chemistry' in data:
        cell.chemistry = data['chemistry']
    if 'capacityAh' in data:
        cell.capacity_ah = data['capacityAh']
    if 'voltageNominal' in data:
        cell.voltage_nominal = data['voltageNominal']
    if 'cycleLife' in data:
        cell.cycle_life = data['cycleLife']
    if 'status' in data:
        cell.status = data['status']
    cell.updated_at = datetime.utcnow()
    
    try:
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@library_bp.route('/api/library/cells/<cell_id>', methods=['DELETE'])
def delete_cell(cell_id):
    """删除电芯"""
    cell = CellLibrary.query.get(cell_id)
    
    if not cell:
        return jsonify({'success': False, 'error': '电芯不存在'}), 404
    
    try:
        db.session.delete(cell)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== 集装箱库API ====================

@library_bp.route('/api/library/containers', methods=['GET'])
def get_containers():
    """获取集装箱列表"""
    try:
        containers = ContainerLibrary.query.order_by(ContainerLibrary.created_at.desc()).all()
        return jsonify({
            'success': True,
            'data': [{
                'id': c.id,
                'model': c.model,
                'mfr': c.mfr,
                'spec': c.spec,
                'ratedEnergyMWh': c.rated_energy_mwh,
                'ratedPowerMW': c.rated_power_mw,
                'dcVoltageRange': c.dc_voltage_range,
                'maxDcCurrent': c.max_dc_current,
                'cellModel': c.cell_model,
                'seriesCount': c.series_count,
                'parallelCount': c.parallel_count,
                'dimensions': c.dimensions,
                'weight': c.weight,
                'cooling': c.cooling,
                'rte': c.rte,
                'auxRun': c.aux_run,
                'auxStandby': c.aux_standby,
                'status': c.status,
                'certifications': json.loads(c.certifications) if c.certifications else [],
                'unitPrice': c.unit_price,
                'remarks': c.remarks,
                'createdAt': c.created_at.isoformat() if c.created_at else None,
            } for c in containers]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@library_bp.route('/api/library/containers', methods=['POST'])
def create_container():
    """创建集装箱"""
    data = request.get_json()
    
    if not data:
        return jsonify({'success': False, 'error': '无效的请求数据'}), 400
    
    container_id = str(uuid.uuid4())
    container = ContainerLibrary(
        id=container_id,
        model=data.get('model'),
        mfr=data.get('mfr'),
        spec=data.get('spec'),
        rated_energy_mwh=data.get('ratedEnergyMWh'),
        rated_power_mw=data.get('ratedPowerMW'),
        dc_voltage_range=data.get('dcVoltageRange'),
        max_dc_current=data.get('maxDcCurrent'),
        cell_model=data.get('cellModel'),
        series_count=data.get('seriesCount'),
        parallel_count=data.get('parallelCount'),
        dimensions=data.get('dimensions'),
        weight=data.get('weight'),
        cooling=data.get('cooling'),
        rte=data.get('rte'),
        aux_run=data.get('auxRun'),
        aux_standby=data.get('auxStandby'),
        status=data.get('status', 'mass-production'),
        certifications=json.dumps(data.get('certifications', [])),
        unit_price=data.get('unitPrice'),
        remarks=data.get('remarks'),
    )
    
    try:
        db.session.add(container)
        db.session.commit()
        return jsonify({'success': True, 'id': container_id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@library_bp.route('/api/library/containers/<container_id>', methods=['PUT'])
def update_container(container_id):
    """更新集装箱"""
    data = request.get_json()
    container = ContainerLibrary.query.get(container_id)
    
    if not container:
        return jsonify({'success': False, 'error': '集装箱不存在'}), 404
    
    # 更新字段
    if 'model' in data:
        container.model = data['model']
    if 'mfr' in data:
        container.mfr = data['mfr']
    if 'ratedEnergyMWh' in data:
        container.rated_energy_mwh = data['ratedEnergyMWh']
    if 'ratedPowerMW' in data:
        container.rated_power_mw = data['ratedPowerMW']
    if 'status' in data:
        container.status = data['status']
    container.updated_at = datetime.utcnow()
    
    try:
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@library_bp.route('/api/library/containers/<container_id>', methods=['DELETE'])
def delete_container(container_id):
    """删除集装箱"""
    container = ContainerLibrary.query.get(container_id)
    
    if not container:
        return jsonify({'success': False, 'error': '集装箱不存在'}), 404
    
    try:
        db.session.delete(container)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== PCS库API ====================

@library_bp.route('/api/library/pcs', methods=['GET'])
def get_pcs_list():
    """获取PCS列表"""
    try:
        pcs_list = PCS_LIBRARY.query.order_by(PCS_LIBRARY.created_at.desc()).all()
        return jsonify({
            'success': True,
            'data': [{
                'id': p.id,
                'model': p.model,
                'mfr': p.mfr,
                'ratedPowerMW': p.rated_power_mw,
                'efficiency': p.efficiency,
                'acVoltage': p.ac_voltage,
                'dcVoltageRange': p.dc_voltage_range,
                'maxDcCurrent': p.max_dc_current,
                'frequencyRange': p.frequency_range,
                'dimensions': p.dimensions,
                'weight': p.weight,
                'cooling': p.cooling,
                'auxRun': p.aux_run,
                'auxStandby': p.aux_standby,
                'status': p.status,
                'certifications': json.loads(p.certifications) if p.certifications else [],
                'unitPrice': p.unit_price,
                'remarks': p.remarks,
                'createdAt': p.created_at.isoformat() if p.created_at else None,
            } for p in pcs_list]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@library_bp.route('/api/library/pcs', methods=['POST'])
def create_pcs():
    """创建PCS"""
    data = request.get_json()
    
    if not data:
        return jsonify({'success': False, 'error': '无效的请求数据'}), 400
    
    pcs_id = str(uuid.uuid4())
    pcs = PCS_LIBRARY(
        id=pcs_id,
        model=data.get('model'),
        mfr=data.get('mfr'),
        rated_power_mw=data.get('ratedPowerMW'),
        efficiency=data.get('efficiency'),
        ac_voltage=data.get('acVoltage'),
        dc_voltage_range=data.get('dcVoltageRange'),
        max_dc_current=data.get('maxDcCurrent'),
        frequency_range=data.get('frequencyRange'),
        dimensions=data.get('dimensions'),
        weight=data.get('weight'),
        cooling=data.get('cooling'),
        aux_run=data.get('auxRun'),
        aux_standby=data.get('auxStandby'),
        status=data.get('status', 'mass-production'),
        certifications=json.dumps(data.get('certifications', [])),
        unit_price=data.get('unitPrice'),
        remarks=data.get('remarks'),
    )
    
    try:
        db.session.add(pcs)
        db.session.commit()
        return jsonify({'success': True, 'id': pcs_id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@library_bp.route('/api/library/pcs/<pcs_id>', methods=['PUT'])
def update_pcs(pcs_id):
    """更新PCS"""
    data = request.get_json()
    pcs = PCS_LIBRARY.query.get(pcs_id)
    
    if not pcs:
        return jsonify({'success': False, 'error': 'PCS不存在'}), 404
    
    # 更新字段
    if 'model' in data:
        pcs.model = data['model']
    if 'mfr' in data:
        pcs.mfr = data['mfr']
    if 'ratedPowerMW' in data:
        pcs.rated_power_mw = data['ratedPowerMW']
    if 'efficiency' in data:
        pcs.efficiency = data['efficiency']
    if 'status' in data:
        pcs.status = data['status']
    pcs.updated_at = datetime.utcnow()
    
    try:
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@library_bp.route('/api/library/pcs/<pcs_id>', methods=['DELETE'])
def delete_pcs(pcs_id):
    """删除PCS"""
    pcs = PCS_LIBRARY.query.get(pcs_id)
    
    if not pcs:
        return jsonify({'success': False, 'error': 'PCS不存在'}), 404
    
    try:
        db.session.delete(pcs)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== 批量操作API ====================

@library_bp.route('/api/library/seed', methods=['POST'])
def seed_library():
    """初始化产品库默认数据"""
    try:
        # 检查是否已有数据
        if CellLibrary.query.first():
            return jsonify({'success': False, 'error': '库中已有数据，请勿重复初始化'}), 400
        
        # 初始化电芯数据
        default_cells = [
            {'model': 'LFP280', 'mfr': '宁德时代', 'chemistry': 'LFP', 'capacityAh': 280, 'voltageNominal': 3.2, 'voltageMax': 3.65, 'voltageMin': 2.5, 'energyWh': 896, 'cycleLife': 6000, 'calendarLife': 20, 'status': 'mass-production'},
            {'model': 'LFP302', 'mfr': '比亚迪', 'chemistry': 'LFP', 'capacityAh': 302, 'voltageNominal': 3.2, 'voltageMax': 3.65, 'voltageMin': 2.5, 'energyWh': 966, 'cycleLife': 6000, 'calendarLife': 20, 'status': 'mass-production'},
            {'model': 'LFP314', 'mfr': '亿纬锂能', 'chemistry': 'LFP', 'capacityAh': 314, 'voltageNominal': 3.2, 'voltageMax': 3.65, 'voltageMin': 2.5, 'energyWh': 1005, 'cycleLife': 5000, 'calendarLife': 20, 'status': 'mass-production'},
            {'model': 'NCM523', 'mfr': 'LG新能源', 'chemistry': 'NCM', 'capacityAh': 150, 'voltageNominal': 3.65, 'voltageMax': 4.2, 'voltageMin': 2.8, 'energyWh': 548, 'cycleLife': 3000, 'calendarLife': 15, 'status': 'mass-production'},
        ]
        
        for cell_data in default_cells:
            cell = CellLibrary(id=str(uuid.uuid4()), **cell_data)
            db.session.add(cell)
        
        # 初始化集装箱数据
        default_containers = [
            {'model': 'C20-5MWh', 'mfr': '宁德时代', 'spec': '20ft', 'ratedEnergyMWh': 5.0, 'ratedPowerMW': 2.5, 'dcVoltageRange': '1000-1500V', 'maxDcCurrent': 2500, 'cooling': '液冷', 'rte': 95, 'auxRun': 15, 'auxStandby': 5, 'status': 'mass-production'},
            {'model': 'C20-3.44MWh', 'mfr': '比亚迪', 'spec': '20ft', 'ratedEnergyMWh': 3.44, 'ratedPowerMW': 1.72, 'dcVoltageRange': '1000-1500V', 'maxDcCurrent': 1720, 'cooling': '液冷', 'rte': 95, 'auxRun': 12, 'auxStandby': 4, 'status': 'mass-production'},
            {'model': 'C40-10MWh', 'mfr': '亿纬锂能', 'spec': '40ft', 'ratedEnergyMWh': 10.0, 'ratedPowerMW': 5.0, 'dcVoltageRange': '1000-1500V', 'maxDcCurrent': 5000, 'cooling': '液冷', 'rte': 95, 'auxRun': 25, 'auxStandby': 8, 'status': 'mass-production'},
        ]
        
        for container_data in default_containers:
            container = ContainerLibrary(id=str(uuid.uuid4()), **container_data)
            db.session.add(container)
        
        # 初始化PCS数据
        default_pcs = [
            {'model': 'PCS1.25MW', 'mfr': '阳光电源', 'ratedPowerMW': 1.25, 'efficiency': 99, 'acVoltage': '400V', 'dcVoltageRange': '900-1500V', 'cooling': '风冷', 'auxRun': 2, 'auxStandby': 0.5, 'status': 'mass-production'},
            {'model': 'PCS1.725MW', 'mfr': '华为', 'ratedPowerMW': 1.725, 'efficiency': 99, 'acVoltage': '400V', 'dcVoltageRange': '900-1500V', 'cooling': '风冷', 'auxRun': 2.5, 'auxStandby': 0.5, 'status': 'mass-production'},
            {'model': 'PCS2.5MW', 'mfr': '阳光电源', 'ratedPowerMW': 2.5, 'efficiency': 99, 'acVoltage': '690V', 'dcVoltageRange': '1000-1500V', 'cooling': '液冷', 'auxRun': 3, 'auxStandby': 1, 'status': 'mass-production'},
            {'model': 'PCS3.45MW', 'mfr': '上能电气', 'ratedPowerMW': 3.45, 'efficiency': 99, 'acVoltage': '690V', 'dcVoltageRange': '1000-1500V', 'cooling': '液冷', 'auxRun': 4, 'auxStandby': 1, 'status': 'mass-production'},
        ]
        
        for pcs_data in default_pcs:
            pcs = PCS_LIBRARY(id=str(uuid.uuid4()), **pcs_data)
            db.session.add(pcs)
        
        db.session.commit()
        return jsonify({'success': True, 'message': '产品库初始化成功'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
