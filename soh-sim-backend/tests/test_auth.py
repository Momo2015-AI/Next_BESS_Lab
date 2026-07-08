"""P2-2 测试：auth 路由 — 注册、登录、me、认证守卫、响应格式"""

import json

import pytest

# ---------- 未认证请求 ----------


class TestUnauthenticated:
    def test_login_returns_token(self, client, seed_user):
        """正确用户名密码应返回 token + user info
        （统一响应格式 {success, data, error, message}）
        """
        resp = client.post(
            "/api/auth/login",
            data=json.dumps(
                {
                    "username": seed_user["username"],
                    "password": "testpass123",
                }
            ),
            content_type="application/json",
        )
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["success"] is True
        assert "token" in data["data"]
        assert data["data"]["user"]["username"] == seed_user["username"]
        assert data["data"]["user"]["role"] == "engineer"

    def test_login_wrong_password(self, client, seed_user):
        """错误密码应返回 401"""
        resp = client.post(
            "/api/auth/login",
            data=json.dumps(
                {
                    "username": seed_user["username"],
                    "password": "WRONG_PASS",
                }
            ),
            content_type="application/json",
        )
        assert resp.status_code == 401

    def test_login_nonexistent_user(self, client):
        """不存在用户返回 401"""
        resp = client.post(
            "/api/auth/login",
            data=json.dumps(
                {
                    "username": "ghost_zzzz",
                    "password": "testpass123",
                }
            ),
            content_type="application/json",
        )
        assert resp.status_code == 401

    def test_login_missing_fields(self, client):
        """缺少密码字段返回 400"""
        resp = client.post(
            "/api/auth/login",
            data=json.dumps({"username": "someone"}),
            content_type="application/json",
        )
        assert resp.status_code == 400


# ---------- 认证接口 ----------


class TestAuthenticated:
    def test_me_returns_user_info(self, auth_client, seed_user):
        """GET /api/auth/me 返回当前认证用户信息（统一响应格式）"""
        resp = auth_client.get("/api/auth/me")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["success"] is True
        assert data["data"]["username"] == seed_user["username"]
        assert data["data"]["role"] == "engineer"

    def test_protected_route_without_token(self, client):
        """无 token 访问受保护路由返回 401"""
        resp = client.get("/api/auth/me")
        assert resp.status_code == 401

    def test_protected_route_invalid_token(self, client):
        """无效 token 返回 401"""
        resp = client.get(
            "/api/auth/me",
            headers={"Authorization": "Bearer invalid.jwt.token"},
        )
        assert resp.status_code == 401


# ---------- 响应格式契约 ----------


class TestResponseContract:
    def test_login_success_format(self, client, seed_user):
        """登录成功响应包含 success/data.user/data.token 字段
        （统一响应格式）
        """
        resp = client.post(
            "/api/auth/login",
            data=json.dumps(
                {
                    "username": seed_user["username"],
                    "password": "testpass123",
                }
            ),
            content_type="application/json",
        )
        data = resp.get_json()
        assert "success" in data
        assert data["success"] is True
        assert "user" in data["data"]
        assert "token" in data["data"]

    def test_login_failure_format(self, client, seed_user):
        """登录失败响应包含 error 字段"""
        resp = client.post(
            "/api/auth/login",
            data=json.dumps(
                {
                    "username": seed_user["username"],
                    "password": "WRONG",
                }
            ),
            content_type="application/json",
        )
        data = resp.get_json()
        assert "error" in data
