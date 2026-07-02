import csv
import io
import math
import os
import re
import tempfile

import numpy as np
from flask import Flask, jsonify, request
from flask_cors import CORS

from database import Project, Survey, db, init_db
from routes.ai_sim import ai_sim_bp, seed_manufacturers
from routes.algorithm import algorithm_bp, seed_algorithms
from routes.auth import auth_bp
from routes.aux_power import aux_power_bp
from routes.boq import boq_bp
from routes.degradation import degradation_bp
from routes.efficiency import efficiency_bp
from routes.export import export_bp
from routes.financial import financial_bp
from routes.pipeline import pipeline_bp
from routes.products import products_bp, seed_products
from routes.project import project_bp
from routes.report import report_bp
from routes.simulation import simulation_bp
from routes.survey import survey_bp
from services.boq import seed_boq_sections

from routes.epc_modules import epc_bp


app = Flask(__name__)
CORS(app)

# 数据库配置
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"sqlite:///{os.path.join(os.path.dirname(os.path.abspath(__file__)), 'soh_sim.db')}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# JWT Secret Key (生产环境请使用环境变量)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "soh-sim-secret-key-change-in-production")

# 初始化数据库
init_db(app)

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
app.register_blueprint(epc_bp)

app.register_blueprint(pipeline_bp)
app.register_blueprint(financial_bp)
app.register_blueprint(boq_bp)
app.register_blueprint(efficiency_bp)
app.register_blueprint(degradation_bp)


with app.app_context():
    seed_manufacturers()
    seed_products()

    seed_algorithms()

    seed_boq_sections(db)


if __name__ == "__main__":
    app.run(debug=False)
