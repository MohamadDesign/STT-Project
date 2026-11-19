from fastapi import FastAPI, Response

from app.core.checks import check_postgres, check_redis
from app.core.config import get_settings

app = FastAPI(title="media-ai", version="0.1.0")


@app.get("/health")
def health() -> dict:
    """Liveness: the process is up. Does not touch dependencies."""
    return {"status": "ok"}


@app.get("/ready")
def ready(response: Response) -> dict:
    """Readiness: PostgreSQL and Redis are reachable."""
    settings = get_settings()
    checks = {
        "postgres": check_postgres(settings.database_url),
        "redis": check_redis(settings.redis_url),
    }
    ok = all(checks.values())
    if not ok:
        response.status_code = 503
    return {"status": "ready" if ok else "not_ready", "checks": checks}
