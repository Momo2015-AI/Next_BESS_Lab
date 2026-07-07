"""
EPC模块路由（按子模块拆分为独立 Blueprint）

注册到 app 时只需: from routes.epc import register_epc_blueprints; register_epc_blueprints(app)
"""
from .architecture import architecture_bp
from .grid_compliance import grid_compliance_bp
from .safety import safety_bp
from .ipp import ipp_bp
from .compliance import compliance_bp
from .thermal import thermal_bp
from .scada import scada_bp
from .hv import hv_bp
from .bid import bid_bp


def register_epc_blueprints(app):
    """注册所有 EPC 子模块 Blueprint 到 Flask app"""
    app.register_blueprint(architecture_bp)
    app.register_blueprint(grid_compliance_bp)
    app.register_blueprint(safety_bp)
    app.register_blueprint(ipp_bp)
    app.register_blueprint(compliance_bp)
    app.register_blueprint(thermal_bp)
    app.register_blueprint(scada_bp)
    app.register_blueprint(hv_bp)
    app.register_blueprint(bid_bp)
