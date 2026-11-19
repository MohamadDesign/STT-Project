from fastapi.testclient import TestClient

from app import main


def test_health_is_ok_without_dependencies():
    client = TestClient(main.app)
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_ready_returns_503_when_dependencies_down(monkeypatch):
    monkeypatch.setattr(main, "check_postgres", lambda *a, **k: False)
    monkeypatch.setattr(main, "check_redis", lambda *a, **k: False)
    r = TestClient(main.app).get("/ready")
    assert r.status_code == 503
    assert r.json()["status"] == "not_ready"


def test_ready_returns_200_when_dependencies_up(monkeypatch):
    monkeypatch.setattr(main, "check_postgres", lambda *a, **k: True)
    monkeypatch.setattr(main, "check_redis", lambda *a, **k: True)
    r = TestClient(main.app).get("/ready")
    assert r.status_code == 200
    assert r.json()["checks"] == {"postgres": True, "redis": True}
