"""P2-2 测试：products 路由 — 产品 CRUD、列表查询、租户隔离"""

import json

import pytest


class TestProducts:
    def test_list_products(self, auth_client):
        """GET /api/products/cells 返回产品列表（统一响应格式 {success, data, error, message, pagination}）"""
        resp = auth_client.get("/api/products/cells")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["success"] is True
        assert "data" in data
        assert isinstance(data["data"], list)
        assert "pagination" in data
        assert "total" in data["pagination"]

    def test_list_products_unauth(self, client):
        """未认证访问返回 200（optional_token_required 允许未认证访问）"""
        resp = client.get("/api/products/cells")
        assert resp.status_code == 200

    def test_response_has_items(self, auth_client):
        """响应包含产品列表（data 键内）"""
        resp = auth_client.get("/api/products/cells")
        data = resp.get_json()
        assert "data" in data
        assert isinstance(data["data"], list)
