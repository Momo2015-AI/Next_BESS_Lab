import math
import os
import re
import csv
import io
import tempfile
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from database import db, init_db, Survey, Project
from routes.survey import survey_bp
from routes.export import export_bp
from routes.auth import auth_bp
from routes.products import products_bp, seed_products
from routes.algorithm import algorithm_bp, seed_algorithms
from routes.project import project_bp
from routes.simulation import simulation_bp
from routes.report import report_bp
from routes.aux_power import aux_power_bp
from routes.ai_sim import ai_sim_bp, seed_manufacturers
from routes.epc_modules import epc_bp

app = Flask(__name__)
CORS(app)

# 数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(os.path.abspath(__file__)), 'soh_sim.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# JWT Secret Key (生产环境请使用环境变量)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'soh-sim-secret-key-change-in-production')

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

with app.app_context():
    seed_manufacturers()
    seed_products()
    seed_algorithms()

if __name__ == '__main__':
    app.run(debug=True)