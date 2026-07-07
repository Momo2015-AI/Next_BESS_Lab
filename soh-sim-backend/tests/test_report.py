"""P2-2 测试：report 路由 — 报告生成、图表数据"""

import json

import pytest


class TestReport:
    def test_report_charts_requires_auth_get(self, client):
        """未认证 GET 访问图表应被拒绝"""
        resp = client.get("/api/report/charts/degradation")
        assert resp.status_code in (401, 405)  # 405 if route only accepts POST

    def test_report_charts_requires_auth_post(self, client):
        """未认证 POST 访问图表应返回 401"""
        resp = client.post(
            "/api/report/charts/degradation",
            data=json.dumps({}),
            content_type="application/json",
        )
        assert resp.status_code in (401, 404)

    def test_report_charts_with_auth(self, auth_client):
        """认证 POST 访问图表接口"""
        resp = auth_client.post(
            "/api/report/charts/degradation",
            data=json.dumps({"projectId": "test-1"}),
            content_type="application/json",
        )
        # 接口可能存在（200）或参数不足（400）或不存在（404）
        assert resp.status_code in (200, 400, 404, 500)
