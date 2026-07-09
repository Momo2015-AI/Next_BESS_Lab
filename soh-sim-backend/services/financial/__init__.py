"""
财务引擎 (Financial Engine)

输入: 仿真结果 + 设计方案
处理: CAPEX自动估算 → OPEX自动估算 → 收入模型选择 → 敏感性
输出: 财务模型（IRR/NPV/LCOS/DSCR/Payback）
"""
from .calculator import (
    BOQ_TO_CAPEX_MAP,
    NUM_YEARS,
    calculate_full_financial,
)
from .engine import FinancialEngine, run_financial

__all__ = [
    "FinancialEngine",
    "run_financial",
    "calculate_full_financial",
    "NUM_YEARS",
    "BOQ_TO_CAPEX_MAP",
]
