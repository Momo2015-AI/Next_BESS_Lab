"""Pytest fixtures for SOH-Sim backend testing.

Provides:
- app / client: Flask test app with in-memory SQLite + all blueprints
- db_session: SQLAlchemy session (SAVEPOINT-rolled-back per test)
- auth_token / auth_headers / auth_client: Authenticated test client
- seed_tenant / seed_user: Seeded test data factories
"""

import os
import uuid

# Must be set BEFORE importing app so that app.py reads the in-memory DB URI
os.environ.setdefault("TEST_DATABASE_URI", "sqlite:///:memory:")
os.environ.setdefault("SECRET_KEY", "test-secret-for-pytest-2026")
os.environ.setdefault("CORS_ORIGINS", "*")

import pytest  # noqa: E402
from flask import g  # noqa: E402

from app import app as _app  # noqa: E402
from database import Tenant, User, db  # noqa: E402
from routes.auth import generate_token  # noqa: E402


# ---------- Fixtures ----------


@pytest.fixture(scope="session")
def app():
    """Session-scoped Flask app — in-memory DB with schema created once."""
    with _app.app_context():
        db.create_all()
    yield _app


@pytest.fixture()
def client(app):
    """Flask test client (unauthenticated)."""
    with app.test_client() as c:
        yield c


@pytest.fixture()
def db_session(app):
    """Per-test DB session — rolled back via SAVEPOINT after each test.

    This fixture depends on client (implicit via function-scope) so that
    each test gets a fresh transaction context.
    """
    connection = db.engine.connect()
    transaction = connection.begin()
    try:
        yield db.session
    finally:
        transaction.rollback()
        connection.close()
        db.session.remove()


# ---------- Seed helpers ----------


@pytest.fixture()
def seed_tenant(db_session):
    """Ensure default tenant exists; returns the tenant instance."""
    tid = "00000000-0000-0000-0000-000000000001"
    t = db_session.get(Tenant, tid)
    if not t:
        t = Tenant(id=tid, name="Default Tenant", code="default", status="active")
        db_session.add(t)
        db_session.flush()
    return t


@pytest.fixture()
def seed_user(db_session, seed_tenant):
    """Create a unique test engineer user per test; returns dict with id/tenant_id/username."""
    from routes.auth import hash_password

    # Use unique email per test fixture call to avoid UNIQUE constraint
    uid = str(uuid.uuid4())
    email = f"test_{uid[:8]}@example.com"
    username = f"test_{uid[:8]}"

    pw = hash_password("testpass123")
    user = User(
        id=uid,
        tenant_id=seed_tenant.id,
        username=username,
        email=email,
        password_hash=pw,
        role="engineer",
        is_active=True,
    )
    db_session.add(user)
    db_session.flush()
    return {"id": uid, "tenant_id": seed_tenant.id, "username": username, "email": email}


# ---------- Auth helpers ----------


@pytest.fixture()
def auth_token(app, seed_user):
    """Valid JWT for the seeded test user."""
    return generate_token(seed_user["id"])


@pytest.fixture()
def auth_headers(auth_token):
    """Auth header dict — pass to client.get(..., headers=auth_headers)."""
    return {"Authorization": f"Bearer {auth_token}"}


@pytest.fixture()
def auth_client(client, auth_headers):
    """Client proxy that injects Bearer token into every request.

    Usage:
        resp = auth_client.get("/api/products/list")
    """
    # Use a small wrapper so each call gets fresh headers
    class AuthenticatedClient:
        def __init__(self, base, headers):
            self._base = base
            self._headers = headers

        def get(self, url, **kw):
            h = {**self._headers, **kw.pop("headers", {})}
            return self._base.get(url, headers=h, **kw)

        def post(self, url, **kw):
            h = {**self._headers, **kw.pop("headers", {})}
            return self._base.post(url, headers=h, **kw)

        def put(self, url, **kw):
            h = {**self._headers, **kw.pop("headers", {})}
            return self._base.put(url, headers=h, **kw)

        def delete(self, url, **kw):
            h = {**self._headers, **kw.pop("headers", {})}
            return self._base.delete(url, headers=h, **kw)

    return AuthenticatedClient(client, auth_headers)
