"""
算法模型管理API - 支持算法模型库的CRUD操作
"""

from flask import Blueprint, request

from database import AlgorithmModel, db
from routes.auth import token_required
from services.algorithm import get_builtin_algorithms, seed_algorithms
from utils.api_response import error_response, success_response

algorithm_bp = Blueprint("algorithm", __name__)


# ==================== API 路由 ====================


@algorithm_bp.route("/api/algorithm/builtin_models", methods=["GET"])
def get_builtin_models_api():
    models = get_builtin_algorithms()
    return success_response(data=models)


@algorithm_bp.route("/api/algorithm/register", methods=["POST"])
@token_required
def register_algorithm_api():
    data = request.get_json()
    if not data:
        return error_response("无效的请求数据", 400)

    new_model = {
        "name": data.get("name"),
        "name_en": data.get("name_en"),
        "model_type": data.get("model_type"),
        "applicable_scenarios": data.get("applicable_scenarios", []),
        "mathematical_form": data.get("mathematical_form"),
        "formula_expression": data.get("formula_expression"),
        "parameters": data.get("parameters", {}),
        "accuracy_level": data.get("accuracy_level", "unknown"),
        "accuracy_desc": data.get("accuracy_desc", ""),
        "category": data.get("category", "other"),
        "is_builtin": False,
        "description": data.get("description", ""),
    }

    new_algorithm = AlgorithmModel(**new_model)
    db.session.add(new_algorithm)
    db.session.commit()

    return success_response(data={"registered_model": new_algorithm}, status_code=201)


@algorithm_bp.route("/api/algorithm/update/<model_id>", methods=["PUT"])
@token_required
def update_algorithm_api(model_id):
    data = request.get_json()
    if not data:
        return error_response("无效的请求数据", 400)

    algorithm = AlgorithmModel.query.get(model_id)
    if not algorithm:
        return error_response("算法模型不存在", 404)

    for key, value in data.items():
        setattr(algorithm, key, value)

    db.session.commit()

    return success_response(data={"updated_model": algorithm.to_dict()})


@algorithm_bp.route("/api/algorithm/delete/<model_id>", methods=["DELETE"])
@token_required
def delete_algorithm_api(model_id):
    algorithm = AlgorithmModel.query.get(model_id)
    if not algorithm:
        return error_response("算法模型不存在", 404)

    db.session.delete(algorithm)
    db.session.commit()

    return success_response(message="算法模型已删除")
