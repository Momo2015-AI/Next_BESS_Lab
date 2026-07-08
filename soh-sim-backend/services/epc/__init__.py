"""
EPC模块服务层（按子模块拆分）

系统架构 | 电网合规 | 安全消防 | IPP财务 | 合规矩阵 |
热管理 | SCADA/EMS | 高压接入 | 投标文档
"""

from .architecture import design_architecture_service
from .bid import generate_bid_document_service
from .compliance import generate_compliance_matrix_service
from .grid_compliance import analyze_grid_compliance_service
from .hv import design_hv_interconnection_service
from .ipp import calculate_ipp_service
from .safety import analyze_safety_design_service
from .scada import design_scada_ems_service
from .thermal import calculate_thermal_service

__all__ = [
    "design_architecture_service",
    "analyze_grid_compliance_service",
    "analyze_safety_design_service",
    "calculate_ipp_service",
    "generate_compliance_matrix_service",
    "calculate_thermal_service",
    "design_scada_ems_service",
    "design_hv_interconnection_service",
    "generate_bid_document_service",
]
