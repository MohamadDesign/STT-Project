"""Integration tests: need `docker compose up -d postgres redis` running."""
import os

import pytest

from app.core.checks import check_postgres, check_redis

pytestmark = pytest.mark.integration

DB = os.getenv(
    "DATABASE_URL", "postgresql://media:change-me@localhost:5432/media")
RD = os.getenv("REDIS_URL", "redis://localhost:6379/0")


def test_postgres_reachable():
    assert check_postgres(DB)


def test_redis_reachable():
    assert check_redis(RD)


def test_pgvector_extension_available():
    import psycopg

    with psycopg.connect(DB) as conn:
        conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
        row = conn.execute(
            "SELECT extversion FROM pg_extension WHERE extname='vector'").fetchone()
        assert row is not None


def test_migration_applies_and_is_idempotent():
    import pathlib

    import psycopg

    sql = (pathlib.Path(__file__).parents[3] /
           "db/migrations/0001_init.sql").read_text()
    with psycopg.connect(DB, autocommit=True) as conn:
        conn.execute(sql)
        conn.execute(sql)  # second run must not fail
        v = conn.execute(
            "SELECT value FROM schema_meta WHERE key='schema_version'").fetchone()
        assert v == ("1",)
