"""
产品库 API 路由
支持电芯、Pack、Rack、Cluster、集装箱、PCS 的 CRUD 操作和种子数据初始化
支持电池层级配置规则自动匹配
支持企业隔离（多租户）：超级管理员可见全部，普通用户仅可见自己企业
"""

import json
import os
import uuid

from flask import Blueprint, current_app, request
from sqlalchemy import or_

from database import (
    BatteryConfigRule,
    BatteryManufacturer,
    CellProduct,
    ClusterProduct,
    ContainerProduct,
    PackProduct,
    PcsProduct,
    RackProduct,
    User,
    db,
)
from routes.auth import optional_token_required, token_required
from services.products import apply_tenant_filter as _apply_tenant_filter
from services.products import camel_to_snake as _camel_to_snake
from services.products import get_models as _get_models
from services.products import is_super_admin as _is_super_admin
from services.products import json_to_model as _json_to_model
from services.products import (
    seed_products,
)
from utils.api_response import error_response, paginated_response, success_response

products_bp = Blueprint("products", __name__)

_MODELS = _get_models()


@products_bp.route("/api/products/seed", methods=["POST"])
@optional_token_required
def seed_api():
    """手动触发种子数据初始化"""
    try:
        seed_products()
        return success_response(message="种子数据已初始化")
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"种子产品数据失败: {e}", exc_info=True)
        return error_response("初始化失败，请重试", status_code=500)


@products_bp.route("/api/products/refresh", methods=["POST"])
@token_required
def refresh_products():
    """刷新产品库：清空现有数据并重新导入种子数据"""
    try:
        for category, model_cls in _MODELS.items():
            # 仅清空系统内置数据
            if hasattr(model_cls, "is_builtin"):
                model_cls.query.filter(model_cls.is_builtin.is_(True)).delete()
            else:
                model_cls.query.delete()
        seed_products()
        return success_response(message="产品库已刷新")
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"刷新产品库失败: {e}", exc_info=True)
        return error_response("刷新失败，请重试", status_code=500)


@products_bp.route("/api/products/<category>", methods=["GET"])
@optional_token_required
def list_products(category):
    """获取产品列表（支持企业隔离，未登录时返回内置数据）"""
    if category not in _MODELS:
        return error_response(f"未知产品类别: {category}", status_code=400)

    user = request.current_user
    model_cls = _MODELS[category]
    mfr = request.args.get("mfr")
    model_name = request.args.get("model")
    chemistry = request.args.get("chemistry")
    scope = request.args.get("scope", "all")  # all / mine / builtin

    query = model_cls.query

    # 应用企业隔离
    if scope == "builtin":
        if hasattr(model_cls, "is_builtin"):
            query = query.filter(model_cls.is_builtin.is_(True))
    elif scope == "mine":
        if user and hasattr(model_cls, "tenant_id"):
            query = query.filter(model_cls.tenant_id == user.tenant_id)
        else:
            query = query.filter(False)
    else:
        if user:
            query = _apply_tenant_filter(query, model_cls, user)
        elif hasattr(model_cls, "is_builtin"):
            # 未登录时仅返回内置数据
            query = query.filter(model_cls.is_builtin.is_(True))

    if mfr:
        query = query.filter(model_cls.mfr == mfr)
    if model_name:
        query = query.filter(model_cls.model == model_name)
    if chemistry and hasattr(model_cls, "chemistry"):
        query = query.filter(model_cls.chemistry == chemistry)

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    items = [item.to_dict() for item in pagination.items]
    return paginated_response(items=items, page=pagination.page, page_size=pagination.per_page, total=pagination.total)


@products_bp.route("/api/products/<category>/<item_id>", methods=["GET"])
@token_required
def get_product(category, item_id):
    """获取单个产品详情"""
    if category not in _MODELS:
        return error_response(f"未知产品类别: {category}", status_code=400)

    user = request.current_user
    model_cls = _MODELS[category]
    item = model_cls.query.get(item_id)
    if not item:
        return error_response("产品不存在", status_code=404)

    # 权限检查
    if not _is_super_admin(user):
        if hasattr(item, "tenant_id") and hasattr(item, "is_builtin"):
            if not item.is_builtin and (not user or item.tenant_id != user.tenant_id):
                return error_response("无权访问", status_code=403)

    return success_response(data=item.to_dict())


@products_bp.route("/api/products/<category>", methods=["POST"])
@token_required
def create_product(category):
    """新增产品（自动归属到当前用户的企业）"""
    if category not in _MODELS:
        return error_response(f"未知产品类别: {category}", status_code=400)

    user = request.current_user

    data = request.get_json()
    if not data:
        return error_response("无效请求数据", status_code=400)

    # 自动设置 tenant_id 与 is_builtin
    data["tenant_id"] = user.tenant_id
    data["is_builtin"] = False  # 用户新增的产品不是系统内置

    # 若未提供 id，自动生成
    if "id" not in data or not data["id"]:
        data["id"] = str(uuid.uuid4())

    obj = _json_to_model(data, category)
    db.session.add(obj)

    try:
        db.session.commit()
        return success_response(data={"id": obj.id, "item": obj.to_dict()}, status_code=201)
    except Exception:
        db.session.rollback()
        return error_response("创建失败，ID可能已存在", status_code=500)


@products_bp.route("/api/products/<category>/<item_id>", methods=["PUT"])
@token_required
def update_product(category, item_id):
    """更新产品（仅能修改自己企业的非系统内置数据）"""
    if category not in _MODELS:
        return error_response(f"未知产品类别: {category}", status_code=400)

    user = request.current_user

    model_cls = _MODELS[category]
    item = model_cls.query.get(item_id)
    if not item:
        return error_response("产品不存在", status_code=404)

    # 权限检查：仅超级管理员可改系统内置数据；普通用户仅能改自己企业数据
    if not _is_super_admin(user):
        if hasattr(item, "is_builtin") and item.is_builtin:
            return error_response("无权修改系统内置数据", status_code=403)
        if hasattr(item, "tenant_id") and item.tenant_id != user.tenant_id:
            return error_response("无权修改其他企业的数据", status_code=403)

    data = request.get_json()
    if not data:
        return error_response("无效请求数据", status_code=400)

    for k, v in data.items():
        key = _camel_to_snake(k, category)
        if hasattr(item, key) and key not in ("id", "tenant_id", "is_builtin"):
            setattr(item, key, v)

    try:
        db.session.commit()
        return success_response()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"更新产品失败: {e}", exc_info=True)
        return error_response("更新失败", status_code=500)


@products_bp.route("/api/products/<category>/<item_id>", methods=["DELETE"])
@token_required
def delete_product(category, item_id):
    """删除产品（仅能删除自己企业的非系统内置数据）"""
    if category not in _MODELS:
        return error_response(f"未知产品类别: {category}", status_code=400)

    user = request.current_user

    model_cls = _MODELS[category]
    item = model_cls.query.get(item_id)
    if not item:
        return error_response("产品不存在", status_code=404)

    # 权限检查
    if not _is_super_admin(user):
        if hasattr(item, "is_builtin") and item.is_builtin:
            return error_response("无权删除系统内置数据", status_code=403)
        if hasattr(item, "tenant_id") and item.tenant_id != user.tenant_id:
            return error_response("无权删除其他企业的数据", status_code=403)

    db.session.delete(item)
    try:
        db.session.commit()
        return success_response()
    except Exception:
        db.session.rollback()
        return error_response("删除失败", status_code=500)


@products_bp.route("/api/products/mfrs/<category>", methods=["GET"])
@token_required
def list_manufacturers(category):
    """获取某类产品的厂商列表（受企业隔离影响，分页返回）"""
    if category not in _MODELS:
        return error_response(f"未知产品类别: {category}", status_code=400)

    user = request.current_user
    model_cls = _MODELS[category]
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 50, type=int)
    query = _apply_tenant_filter(db.session.query(model_cls.mfr), model_cls, user)
    total = query.distinct().count()
    rows = query.distinct().offset((page - 1) * per_page).limit(per_page).all()
    mfrs = [r[0] for r in rows if r[0]]
    return paginated_response(items=mfrs, page=page, page_size=per_page, total=total)


@products_bp.route("/api/products/models/<category>", methods=["GET"])
@token_required
def list_models(category):
    """获取某类产品的型号列表（受企业隔离影响，分页返回）"""
    if category not in _MODELS:
        return error_response(f"未知产品类别: {category}", status_code=400)

    user = request.current_user
    model_cls = _MODELS[category]
    mfr = request.args.get("mfr")
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 50, type=int)

    query = _apply_tenant_filter(db.session.query(model_cls.model), model_cls, user)
    if mfr:
        query = query.filter(model_cls.mfr == mfr)

    total = query.distinct().count()
    rows = query.distinct().offset((page - 1) * per_page).limit(per_page).all()
    models = [r[0] for r in rows if r[0]]
    return paginated_response(items=models, page=page, page_size=per_page, total=total)


@products_bp.route("/api/products/match-config", methods=["POST"])
@token_required
def match_config_rule():
    """根据电芯/电池型号自动匹配配置规则（受企业隔离影响）"""
    data = request.get_json()
    if not data:
        return error_response("无效请求数据", status_code=400)

    user = request.current_user
    cell_model = data.get("cellModel")
    pack_model = data.get("packModel")
    rack_model = data.get("rackModel")
    cluster_model = data.get("clusterModel")
    container_model = data.get("containerModel")

    query = _apply_tenant_filter(
        BatteryConfigRule.query.filter(BatteryConfigRule.status == "active"), BatteryConfigRule, user
    )

    if cell_model:
        query = query.filter(BatteryConfigRule.cell_model == cell_model)
    if pack_model:
        query = query.filter(BatteryConfigRule.pack_model == pack_model)
    if rack_model:
        query = query.filter(BatteryConfigRule.rack_model == rack_model)
    if cluster_model:
        query = query.filter(BatteryConfigRule.cluster_model == cluster_model)
    if container_model:
        query = query.filter(BatteryConfigRule.container_model == container_model)

    rules = query.limit(100).all()

    if rules:
        default_rule = next((r for r in rules if r.is_default), rules[0])
        return success_response(
            data={
                "matched": True,
                "rule": default_rule.to_dict(),
                "all_rules_count": len(rules),
            }
        )
    else:
        return success_response(
            data={
                "matched": False,
                "rule": None,
                "all_rules": [],
            },
            message="未找到匹配的配置规则，请手动配置",
        )


@products_bp.route("/api/products/config-rules", methods=["GET"])
@optional_token_required
def list_config_rules():
    """获取所有配置规则列表（受企业隔离影响，未登录时返回内置数据）"""
    status = request.args.get("status", "active")
    user = request.current_user
    if user:
        query = _apply_tenant_filter(BatteryConfigRule.query, BatteryConfigRule, user)
    else:
        query = BatteryConfigRule.query.filter(BatteryConfigRule.is_builtin.is_(True))

    if status:
        query = query.filter(BatteryConfigRule.status == status)

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    items = [r.to_dict() for r in pagination.items]
    return paginated_response(items=items, page=pagination.page, page_size=pagination.per_page, total=pagination.total)


@products_bp.route("/api/products/config-rules/<rule_id>", methods=["GET"])
@token_required
def get_config_rule(rule_id):
    """获取单个配置规则详情"""
    user = request.current_user
    rule = BatteryConfigRule.query.get(rule_id)
    if not rule:
        return error_response("配置规则不存在", status_code=404)

    if not _is_super_admin(user):
        if hasattr(rule, "is_builtin") and hasattr(rule, "tenant_id"):
            if not rule.is_builtin and (not user or rule.tenant_id != user.tenant_id):
                return error_response("无权访问", status_code=403)

    return success_response(data=rule.to_dict())


@products_bp.route("/api/products/config-rules", methods=["POST"])
@token_required
def create_config_rule():
    """创建配置规则（归属当前用户企业）"""
    user = request.current_user

    data = request.get_json()
    if not data:
        return error_response("无效请求数据", status_code=400)

    if "id" not in data:
        data["id"] = str(uuid.uuid4())

    data["tenant_id"] = user.tenant_id
    data["is_builtin"] = False

    rule = _json_to_model(data, "config_rules")
    db.session.add(rule)

    try:
        db.session.commit()
        return success_response(data={"id": rule.id}, status_code=201)
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"创建配置规则失败: {e}", exc_info=True)
        return error_response("创建失败，请重试", status_code=500)


@products_bp.route("/api/products/config-rules/<rule_id>", methods=["PUT"])
@token_required
def update_config_rule(rule_id):
    """更新配置规则"""
    user = request.current_user

    rule = BatteryConfigRule.query.get(rule_id)
    if not rule:
        return error_response("配置规则不存在", status_code=404)

    if not _is_super_admin(user):
        if hasattr(rule, "is_builtin") and rule.is_builtin:
            return error_response("无权修改系统内置数据", status_code=403)
        if hasattr(rule, "tenant_id") and rule.tenant_id != user.tenant_id:
            return error_response("无权修改其他企业的数据", status_code=403)

    data = request.get_json()
    if not data:
        return error_response("无效请求数据", status_code=400)

    for k, v in data.items():
        key = _camel_to_snake(k, "config_rules")
        if hasattr(rule, key) and key not in ("id", "tenant_id", "is_builtin"):
            setattr(rule, key, v)

    try:
        db.session.commit()
        return success_response()
    except Exception:
        db.session.rollback()
        return error_response("更新失败", status_code=500)


@products_bp.route("/api/products/config-rules/<rule_id>", methods=["DELETE"])
@token_required
def delete_config_rule(rule_id):
    """删除配置规则"""
    user = request.current_user

    rule = BatteryConfigRule.query.get(rule_id)
    if not rule:
        return error_response("配置规则不存在", status_code=404)

    if not _is_super_admin(user):
        if hasattr(rule, "is_builtin") and rule.is_builtin:
            return error_response("无权删除系统内置数据", status_code=403)
        if hasattr(rule, "tenant_id") and rule.tenant_id != user.tenant_id:
            return error_response("无权删除其他企业的数据", status_code=403)

    db.session.delete(rule)
    try:
        db.session.commit()
        return success_response()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"删除配置规则失败: {e}", exc_info=True)
        return error_response("删除失败", status_code=500)


@products_bp.route("/api/products/hierarchy", methods=["POST"])
@token_required
def get_hierarchy():
    """获取完整的电池层级配置信息（受企业隔离影响）"""
    user = request.current_user
    data = request.get_json()
    if not data:
        return error_response("无效请求数据", status_code=400)

    cell_model = data.get("cellModel")
    pack_model = data.get("packModel")

    result = {
        "cell": None,
        "pack": None,
        "rack": None,
        "cluster": None,
        "container": None,
        "config_rule": None,
    }

    if cell_model:
        cell_query = _apply_tenant_filter(CellProduct.query.filter(CellProduct.model == cell_model), CellProduct, user)
        cell = cell_query.first()
        if cell:
            result["cell"] = cell.to_dict()
            packs_query = _apply_tenant_filter(
                PackProduct.query.filter(PackProduct.cell_model == cell_model), PackProduct, user
            )
            pack = packs_query.first()
            if pack:
                result["pack"] = pack.to_dict()
                pack_model = pack.model
                rack = _apply_tenant_filter(
                    RackProduct.query.filter(RackProduct.pack_model == pack_model), RackProduct, user
                ).first()
                if rack:
                    result["rack"] = rack.to_dict()
                    rack_model = rack.model
                    cluster = _apply_tenant_filter(
                        ClusterProduct.query.filter(ClusterProduct.rack_model == rack_model), ClusterProduct, user
                    ).first()
                    if cluster:
                        result["cluster"] = cluster.to_dict()
                        cluster_model = cluster.model
                        container = _apply_tenant_filter(
                            ContainerProduct.query.filter(
                                or_(
                                    ContainerProduct.cluster_model == cluster_model,
                                    ContainerProduct.cell_model == cell_model,
                                )
                            ),
                            ContainerProduct,
                            user,
                        ).first()
                        if container:
                            result["container"] = container.to_dict()

    elif pack_model:
        pack_query = _apply_tenant_filter(PackProduct.query.filter(PackProduct.model == pack_model), PackProduct, user)
        pack = pack_query.first()
        if pack:
            result["pack"] = pack.to_dict()
            rack = _apply_tenant_filter(
                RackProduct.query.filter(RackProduct.pack_model == pack_model), RackProduct, user
            ).first()
            if rack:
                result["rack"] = rack.to_dict()
                rack_model = rack.model
                cluster = _apply_tenant_filter(
                    ClusterProduct.query.filter(ClusterProduct.rack_model == rack_model), ClusterProduct, user
                ).first()
                if cluster:
                    result["cluster"] = cluster.to_dict()
                    cluster_model = cluster.model
                    container = _apply_tenant_filter(
                        ContainerProduct.query.filter(ContainerProduct.cluster_model == cluster_model),
                        ContainerProduct,
                        user,
                    ).first()
                    if container:
                        result["container"] = container.to_dict()

    rule_query = _apply_tenant_filter(
        BatteryConfigRule.query.filter(
            BatteryConfigRule.status == "active",
        ),
        BatteryConfigRule,
        user,
    )
    if cell_model:
        rule_query = rule_query.filter(BatteryConfigRule.cell_model == cell_model)
    if pack_model:
        rule_query = rule_query.filter(BatteryConfigRule.pack_model == pack_model)

    rule_match = rule_query.first()
    if rule_match:
        result["config_rule"] = rule_match.to_dict()

    return success_response(data=result)
