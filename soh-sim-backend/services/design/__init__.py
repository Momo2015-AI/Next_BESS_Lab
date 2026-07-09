"""
方案设计引擎 (Design Engine)

输入: 调研表（功率/能量/温度/地点/DOD/C-Rate）
处理: 约束求解 → 产品匹配 → 拓扑生成 → 多方案排序
输出: 3-5 套设计方案（含 BOM + 预估 CAPEX）
"""
from .engine import DesignEngine, auto_design

__all__ = ["DesignEngine", "auto_design"]
