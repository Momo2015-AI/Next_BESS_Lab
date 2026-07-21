import csv
import io
import math
import os
import re
import tempfile

import numpy as np
from flask import Flask, request
from flask_cors import CORS

from database import Project, Survey, db, init_db
from routes.admin import admin_bp
from routes.ai_sim import ai_sim_bp, seed_manufacturers
from routes.algorithm import algorithm_bp, seed_algorithms
from routes.auth import auth_bp, hash_password, limiter
from routes.aux_power import aux_power_bp
from routes.boq import boq_bp
from routes.degradation import degradation_bp
from routes.design_engine import design_engine_bp
from routes.efficiency import efficiency_bp
from routes.epc import register_epc_blueprints
from routes.exchange_rate import exchange_rate_bp
from routes.export import export_bp
from routes.financial import financial_bp
from routes.financial_engine import fin_engine_bp
from routes.orchestrator import orchestrator_bp
from routes.products import products_bp, seed_products
from routes.project import project_bp
from routes.rbac import rbac_bp
from routes.report import report_bp
from routes.simulation import simulation_bp
from routes.simulation_engine import sim_engine_bp
from routes.survey import survey_bp
from services.boq import seed_boq_sections
from utils.api_response import error_response

app = Flask(__name__)
allowed_origins = os.environ.get("CORS_ORIGINS", "").split(",")
CORS(
    app,
    origins=[o.strip() for o in allowed_origins if o.strip()],
    supports_credentials=True,
)

# 数据库配置
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "TEST_DATABASE_URI",
    "sqlite:///" + os.path.join(os.path.dirname(os.path.abspath(__file__)), "soh_sim.db"),
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# JWT Secret Key — 生产环境必须设置环境变量，否则拒绝启动
_secret_key = os.environ.get("SECRET_KEY")
if not _secret_key:
    import logging
    import sys

    logging.critical("❌ SECRET_KEY 环境变量未设置！生产环境拒绝启动。")
    logging.critical("   请在环境变量中设置: export SECRET_KEY=<your-secure-random-key>")
    logging.critical('   可使用 python -c "import secrets; print(secrets.token_hex(32))" 生成强密钥')
    sys.exit(1)
app.config["SECRET_KEY"] = _secret_key

# 初始化数据库
init_db(app)

# 初始化速率限制器
limiter.init_app(app)

# 注册路由
app.register_blueprint(survey_bp)
app.register_blueprint(export_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(products_bp)
app.register_blueprint(project_bp)
app.register_blueprint(simulation_bp)
app.register_blueprint(algorithm_bp)
app.register_blueprint(report_bp)
app.register_blueprint(aux_power_bp)

app.register_blueprint(ai_sim_bp)
register_epc_blueprints(app)

app.register_blueprint(financial_bp)
app.register_blueprint(design_engine_bp)
app.register_blueprint(sim_engine_bp)
app.register_blueprint(fin_engine_bp)
app.register_blueprint(orchestrator_bp)
app.register_blueprint(boq_bp)
app.register_blueprint(efficiency_bp)
app.register_blueprint(degradation_bp)
app.register_blueprint(exchange_rate_bp)
app.register_blueprint(rbac_bp)
app.register_blueprint(admin_bp)


# ==================== 全局错误处理器 ====================


@app.errorhandler(400)
def bad_request(e):
    return error_response("请求参数错误", status_code=400)


@app.errorhandler(401)
def unauthorized(e):
    return error_response("未授权访问", status_code=401)


@app.errorhandler(403)
def forbidden(e):
    return error_response("权限不足", status_code=403)


@app.errorhandler(404)
def not_found(e):
    return error_response("资源不存在", status_code=404)


@app.errorhandler(405)
def method_not_allowed(e):
    return error_response("请求方法不允许", status_code=405)


@app.errorhandler(429)
def rate_limited(e):
    return error_response("请求过于频繁，请稍后再试", status_code=429)


@app.errorhandler(500)
def internal_error(e):
    import traceback

    app.logger.error(f"服务器内部错误: {traceback.format_exc()}")
    return error_response("服务器内部错误", status_code=500)


# ==================== 种子数据 ====================


def seed_users():
    """初始化默认用户（管理员 + 演示工程师），仅当数据库中无用户时执行

    种子密码使用随机强密码，首次登录后建议立即修改。
    种子密码仅在首次数据库初始化时创建，已有用户时跳过。
    """
    from database import User

    if User.query.first() is not None:
        return  # 已有用户，跳过种子

    import secrets
    import uuid as _uuid

    # 生成随机强密码（16 字符，含大小写字母+数字）
    def _gen_pwd():
        alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        return "".join(secrets.choice(alphabet) for _ in range(16))

    admin_pwd = _gen_pwd()
    eng_pwd = _gen_pwd()

    default_users = [
        {
            "id": "admin-000000000000000000000001",
            "username": "admin",
            "email": "admin@soh-sim.com",
            "password": admin_pwd,
            "role": "admin",
        },
        {
            "id": "eng-000000000000000000000001",
            "username": "engineer",
            "email": "engineer@soh-sim.com",
            "password": eng_pwd,
            "role": "solution_engineer",
        },
    ]

    for u in default_users:
        user = User(
            id=u["id"],
            tenant_id="00000000-0000-0000-0000-000000000001",
            username=u["username"],
            email=u["email"],
            password_hash=hash_password(u["password"]),
            role=u["role"],
            is_active=True,
        )
        db.session.add(user)

    db.session.commit()
    import logging

    logging.info("种子用户已创建: admin / engineer")


with app.app_context():
    seed_users()
    seed_manufacturers()
    seed_products()

    seed_algorithms()

    seed_boq_sections(db)

    # 种子方案模板
    from models.admin import DesignTemplate

    _builtin_templates = [
        {
            "name": "经济优先方案",
            "name_en": "Economic Priority",
            "strategy": "economic",
            "description": "选用大容量集装箱，最小化 BOP 和施工成本，适合预算优先项目",
            "is_default": True,
            "sort_order": 1,
        },
        {
            "name": "均衡方案",
            "name_en": "Balanced",
            "strategy": "balanced",
            "description": "中等容量集装箱，最优单位成本（CAPEX/MWh），适合大多数项目",
            "is_default": True,
            "sort_order": 2,
        },
        {
            "name": "灵活分期方案",
            "name_en": "Flexible Phased",
            "strategy": "flexible",
            "description": "小容量集装箱，便于分期部署和扩容，适合分阶段投资项目",
            "is_default": True,
            "sort_order": 3,
        },
    ]
    for tmpl in _builtin_templates:
        existing = DesignTemplate.query.filter_by(name=tmpl["name"], is_builtin=True).first()
        if not existing:
            db.session.add(
                DesignTemplate(
                    name=tmpl["name"],
                    name_en=tmpl["name_en"],
                    strategy=tmpl["strategy"],
                    description=tmpl["description"],
                    is_default=tmpl["is_default"],
                    is_builtin=True,
                    sort_order=tmpl["sort_order"],
                )
            )
    db.session.commit()


if __name__ == "__main__":
    app.run(debug=False)
