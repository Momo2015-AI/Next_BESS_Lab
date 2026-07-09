"""
三引擎基类

所有引擎（Design/Simulation/Financial）继承此基类，
提供统一的输入验证、结果缓存接口。
"""

from abc import ABC, abstractmethod


class BaseEngine(ABC):
    """引擎抽象基类"""

    # 引擎名称（子类覆盖）
    name: str = "base"

    def __init__(self):
        self._cache = {}
        self._last_input_hash = None

    @abstractmethod
    def run(self, **kwargs):
        """执行引擎计算（子类必须实现）"""
        ...

    @abstractmethod
    def validate_input(self, data: dict) -> list:
        """验证输入参数，返回错误列表（子类必须实现）"""
        ...

    def _input_hash(self, data: dict) -> str:
        """计算输入哈希，用于缓存判断"""
        import hashlib
        import json

        raw = json.dumps(data, sort_keys=True, default=str)
        return hashlib.md5(raw.encode()).hexdigest()

    def cached_run(self, **kwargs):
        """带缓存的执行：输入未变时返回缓存结果"""
        h = self._input_hash(kwargs)
        if h == self._last_input_hash and self._cache:
            return self._cache
        self._last_input_hash = h
        self._cache = self.run(**kwargs)
        return self._cache

    def clear_cache(self):
        """清除缓存"""
        self._cache = {}
        self._last_input_hash = None
