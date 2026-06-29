"""
数据库配置与模型定义
使用SQLite作为数据库，支持跨平台运行
完整支持所有功能模块的数据存储
"""
import os
import json
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()

# 这些列存储 JSON 字符串，序列化时需要解析回对象
_JSON_COLUMNS = {
    'Survey': {'attachments'},
    'Project': {'config'},
    'Simulation': {'input_params', 'results', 'manual_corrections'},
    'BatteryPCSConfig': {'connection_diagram', 'single_line_diagram'},
    'SohRteData': {'soh_values', 'rte_values', 'dod_values', 'aug_qty_values'},
    'FinancialData': {'cashflow_data'},
    'ProductConfig': {'certifications'},
    'FormulaConfig': {'parameters'},
}

def _serialize_value(model_name, column_name, value):
    """序列化单个字段值：datetime→ISO 字符串，JSON 列→解析回对象"""
    if value is None:
        return None
    if model_name in _JSON_COLUMNS and column_name in _JSON_COLUMNS[model_name]:
        if isinstance(value, str):
            try:
                return json.loads(value)
            except (json.JSONDecodeError, ValueError):
                return value
        return value
    if isinstance(value, datetime):
        return value.isoformat()
    return value

def _model_to_dict(self):
    """通用 to_dict：遍历所有列，按需序列化"""
    model_name = type(self).__name__
    return {
        column.name: _serialize_value(model_name, column.name, getattr(self, column.name))
        for column in self.__table__.columns
    }

class PinnModelWeights(db.Model):
    __tablename__ = 'pinn_model_weights'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    model_name = db.Column(db.String(255), nullable=False)
    weights = db.Column(db.LargeBinary, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    def __repr__(self):
        return f'<PinnModelWeights {self.model_name}>'

# 初始化数据库
def init_db(app):
    with app.app_context():
        db.init_app(app)
        db.create_all()