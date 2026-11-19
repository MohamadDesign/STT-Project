# بخش ۱.۱ — اسکلت زیرساخت

## هدف
محیط اجرایی پایه: PostgreSQL + pgvector، Redis، سرویس API با health/readiness.

## اجزا
- `docker-compose.yml`: سرویس‌های `postgres`, `redis`, `api`.
- `db/migrations/0001_init.sql`: افزونه `vector` و جدول `schema_meta`.
- `services/api`: FastAPI با `/health` (زنده‌بودن) و `/ready` (اتصال به Postgres و Redis).

## اجرا
1. `cp .env.example .env` و رمزها را عوض کنید.
2. `make up` و سپس `make logs`.
3. تست واحد: `make test`. تست یکپارچه (نیازمند compose): `make test-all`.

## آزمون پذیرش
- [ ] `docker compose up -d` هر سه سرویس را healthy می‌کند.
- [ ] `curl -s localhost:8000/health` مقدار `{"status":"ok"}` برمی‌گرداند.
- [ ] `curl -s localhost:8000/ready` مقدار `ready` با هر دو چک `true` برمی‌گرداند.
- [ ] `psql -c "SELECT extversion FROM pg_extension WHERE extname='vector'"` نسخه را نشان می‌دهد.
- [ ] اجرای دوباره‌ی migration خطا نمی‌دهد.
- [ ] `pytest -m integration` با ۴ تست سبز در حالت compose اجرا شود.
