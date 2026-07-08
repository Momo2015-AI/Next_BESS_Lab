"""
数据库配置与模型定义（向后兼容入口）

此文件现为 models/ 包的代理，保持所有现有 `from database import X` 的兼容性。
所有模型类和辅助函数均从 models 子包导入。
"""

# flake8: noqa: F401, F403

from models import *  # noqa: F403
from models import _model_to_dict, _serialize_value, db, init_db
