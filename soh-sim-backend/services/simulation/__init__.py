"""
仿真引擎 (Simulation Engine)

输入: 设计方案（containerQty/pcsQty/cellMfr/温度等）
处理: SOH退化预测 → 能量核算 → 补容策略 → 效率曲线
输出: 25年仿真矩阵
"""
from .engine import SimulationEngine, run_simulation

__all__ = ["SimulationEngine", "run_simulation"]
