"""P2-2 测试：ai_sim 路由 — 厂家列表、参数校准、模拟接口"""

import json

import pytest


class TestAiSimManufacturers:
    def test_list_manufacturers(self, auth_client):
        """GET /api/ai-sim/manufacturers 返回厂家列表"""
        resp = auth_client.get("/api/ai-sim/manufacturers")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data.get("success") is True

    def test_list_manufacturers_unauth(self, client):
        """未认证访问返回 401"""
        resp = client.get("/api/ai-sim/manufacturers")
        assert resp.status_code == 401
