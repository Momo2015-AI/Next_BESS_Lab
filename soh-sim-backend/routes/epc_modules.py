"""
EPC模块路由 - 向后兼容代理

原始路由已拆分为 routes/epc/ 目录下的 9 个独立 Blueprint。
如需继续使用旧的 epc_bp 对象，此文件提供向后兼容。
建议新代码使用:
  from routes.epc import register_epc_blueprints
  register_epc_blueprints(app)
"""
from routes.epc import register_epc_blueprints

# 向后兼容：提供一个空 Blueprint，实际路由已通过
# register_epc_blueprints 注册
from flask import Blueprint

epc_bp = Blueprint("epc", __name__)
