# Section 1.1 — Infrastructure skeleton

## Goal
Baseline runtime: PostgreSQL + pgvector, Redis, and an API service with health/readiness endpoints.

## Components
- `docker-compose.yml`: `postgres`, `redis`, `api` services.
- `db/migrations/0001_init.sql`: the `vector` extension and `schema_meta`.
- `services/api`: FastAPI with `/health` (liveness) and `/ready` (Postgres + Redis reachability).

## Run
1. `cp .env.example .env` and change the secrets.
2. `make up`, then `make logs`.
3. Unit tests: `make test`. Integration tests (need compose): `make test-all`.

## Acceptance tests
- [ ] `docker compose up -d` brings all three services to healthy.
- [ ] `curl -s localhost:8000/health` returns `{"status":"ok"}`.
- [ ] `curl -s localhost:8000/ready` returns `ready` with both checks `true`.
- [ ] `psql -c "SELECT extversion FROM pg_extension WHERE extname='vector'"` shows a version.
- [ ] Re-running the migration does not fail.
- [ ] `pytest -m integration` passes 4 tests against compose.
