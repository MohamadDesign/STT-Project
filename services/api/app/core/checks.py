import psycopg
import redis


def check_postgres(url: str, timeout: float = 2.0) -> bool:
    try:
        with psycopg.connect(url, connect_timeout=int(timeout)) as conn:
            conn.execute("SELECT 1")
        return True
    except Exception:
        return False


def check_redis(url: str, timeout: float = 2.0) -> bool:
    try:
        return bool(redis.Redis.from_url(url, socket_timeout=timeout).ping())
    except Exception:
        return False
