"""URL Shortener tests — 每個 test 對應一條 AC."""

import pytest
from fastapi.testclient import TestClient

from app.main import app, db_conn, get_conn


@pytest.fixture
def client(tmp_path, monkeypatch) -> TestClient:
    """每個 test 用獨立 SQLite 檔, 避免互相污染."""
    db_file = tmp_path / "test.db"

    def _db_conn():
        with get_conn(str(db_file)) as conn:
            yield conn

    app.dependency_overrides[db_conn] = _db_conn
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_ac_001_same_url_returns_same_code(client: TestClient) -> None:
    """AC-001: POST /shorten 同一個 URL 兩次, short_code 必須相等 (REQ-003)."""
    r1 = client.post("/shorten", json={"url": "https://example.com"})
    r2 = client.post("/shorten", json={"url": "https://example.com"})
    assert r1.status_code == 200
    assert r2.status_code == 200
    assert r1.json()["short_code"] == r2.json()["short_code"]


def test_ac_002_missing_code_returns_404(client: TestClient) -> None:
    """AC-002: GET 不存在的 code 回傳 404 (REQ-004)."""
    r = client.get("/abc999")
    assert r.status_code == 404


def test_ac_003_url_too_long_returns_400(client: TestClient) -> None:
    """AC-003: 2049 字元 URL 回傳 400 (CON-001)."""
    long_url = "https://example.com/" + "x" * 2030
    assert len(long_url) > 2048
    r = client.post("/shorten", json={"url": long_url})
    assert r.status_code == 400


def test_ac_004_invalid_url_returns_400(client: TestClient) -> None:
    """AC-004: 無效格式 URL 回傳 400 (CON-002)."""
    r = client.post("/shorten", json={"url": "not-a-url"})
    assert r.status_code == 400


def test_ac_005_resolve_redirects_to_original(client: TestClient) -> None:
    """AC-005: POST 後 GET /{code} 回傳 302 並指向原始 URL (REQ-004)."""
    original = "https://example.com/some/path"
    r = client.post("/shorten", json={"url": original})
    code = r.json()["short_code"]

    r2 = client.get(f"/{code}", follow_redirects=False)
    assert r2.status_code == 302
    assert r2.headers["location"] == original


def test_req_002_short_code_format(client: TestClient) -> None:
    """REQ-002: short_code 長度 6, 字元集 [a-zA-Z0-9]."""
    r = client.post("/shorten", json={"url": "https://example.com/x"})
    code = r.json()["short_code"]
    assert len(code) == 6
    assert all(c.isalnum() for c in code)
