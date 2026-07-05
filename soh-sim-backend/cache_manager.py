"""
缓存管理器 - 用于缓存计算密集型结果
"""

import logging
import threading
import time
from functools import wraps

logger = logging.getLogger(__name__)


class LRUCache:
    """
    简单的LRU缓存实现
    TTL 基于插入时间（insert_time）判断，不受访问频率影响。
    热数据不会因为频繁访问而永不过期。
    """

    def __init__(self, capacity: int = 100, ttl: int = 3600):
        self.capacity = capacity
        self.ttl = ttl  # Time-to-live in seconds
        self.cache = {}
        self.insert_times = {}  # 用于 TTL 判断
        self.access_times = {}  # 用于 LRU 淘汰
        self.lock = threading.Lock()

    def get(self, key):
        with self.lock:
            if key in self.cache:
                # 基于插入时间检查是否过期
                if time.time() - self.insert_times[key] <= self.ttl:
                    # 更新访问时间（仅用于 LRU 淘汰排序）
                    self.access_times[key] = time.time()
                    return self.cache[key]
                else:
                    # 过期，删除键值对
                    del self.cache[key]
                    del self.insert_times[key]
                    del self.access_times[key]
            return None

    def put(self, key, value):
        with self.lock:
            if key in self.cache:
                # 更新现有键的值、插入时间和访问时间
                self.cache[key] = value
                self.insert_times[key] = time.time()
                self.access_times[key] = time.time()
            else:
                if len(self.cache) >= self.capacity:
                    # 找到最久未使用的键（基于 access_time）
                    oldest_key = min(self.access_times.keys(), key=lambda k: self.access_times[k])
                    del self.cache[oldest_key]
                    del self.insert_times[oldest_key]
                    del self.access_times[oldest_key]

                self.cache[key] = value
                self.insert_times[key] = time.time()
                self.access_times[key] = time.time()

    def invalidate(self, key):
        with self.lock:
            if key in self.cache:
                del self.cache[key]
                del self.insert_times[key]
                del self.access_times[key]

    def clear(self):
        with self.lock:
            self.cache.clear()
            self.insert_times.clear()
            self.access_times.clear()


# 全局缓存实例
calculation_cache = LRUCache(capacity=50, ttl=7200)  # 2小时过期时间


def cached_function(ttl=3600):
    """
    缓存装饰器
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 生成缓存键
            cache_key = f"{func.__name__}:{str(args)}:{str(sorted(kwargs.items()))}"

            # 尝试从缓存获取结果
            cached_result = calculation_cache.get(cache_key)
            if cached_result is not None:
                logger.debug("Cache hit for %s", func.__name__)
                return cached_result

            # 计算结果
            result = func(*args, **kwargs)

            # 存储到缓存
            calculation_cache.put(cache_key, result)
            logger.debug("Cache miss for %s, cached result", func.__name__)

            return result

        return wrapper

    return decorator


def invalidate_cache(pattern=None):
    """
    清除特定模式的缓存
    """
    if pattern is None:
        calculation_cache.clear()
    else:
        # 这里可以实现更复杂的清除逻辑
        keys_to_remove = [key for key in calculation_cache.cache.keys() if pattern in key]
        for key in keys_to_remove:
            calculation_cache.invalidate(key)


# 示例用法
if __name__ == "__main__":

    @cached_function(ttl=1800)  # 30分钟过期
    def expensive_calculation(x, y):
        print(f"Performing expensive calculation for {x}, {y}")
        time.sleep(1)  # 模拟耗时计算
        return x * y + x**2 + y**2

    # 测试缓存
    print(expensive_calculation(2, 3))  # 第一次调用，会计算
    print(expensive_calculation(2, 3))  # 第二次调用，从缓存获取
    print(expensive_calculation(4, 5))  # 新的参数，会计算
