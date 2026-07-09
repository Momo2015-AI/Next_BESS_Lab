"""
三引擎事件总线（已废弃）

评估结论：三引擎是线性串联关系（设计→仿真→财务），Flask 同步请求模型下
事件总线无实际解耦价值，反而增加复杂度。

当前三引擎由 services/orchestrator.py 的 run_full_workflow() 顺序调用编排。
此文件保留仅供参考，所有 emit() 调用已从引擎代码中移除。
"""

import warnings

warnings.warn(
    "EngineBus is deprecated. Use services/orchestrator.py for engine orchestration.",
    DeprecationWarning,
    stacklevel=2,
)


class EngineBus:
    """[已废弃] 轻量级事件总线 — 不再使用，保留仅供兼容"""

    _listeners: dict = {}

    @classmethod
    def on(cls, event: str, callback):
        """[已废弃]"""
        cls._listeners.setdefault(event, []).append(callback)

    @classmethod
    def emit(cls, event: str, data: dict = None):
        """[已废弃]"""
        for cb in cls._listeners.get(event, []):
            try:
                cb(data or {})
            except Exception as e:
                import logging

                logging.warning(f"EngineBus [{event}] 回调异常: {e}")

    @classmethod
    def off(cls, event: str, callback=None):
        """[已废弃]"""
        if callback is None:
            cls._listeners.pop(event, None)
        elif event in cls._listeners:
            cls._listeners[event] = [cb for cb in cls._listeners[event] if cb != callback]

    @classmethod
    def clear(cls):
        """[已废弃]"""
        cls._listeners.clear()
