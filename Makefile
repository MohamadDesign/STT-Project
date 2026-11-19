.PHONY: up down logs test test-all readiness copy

up:
	docker compose up -d postgres redis
down:
	docker compose down
logs:
	docker compose logs -f --tail=100
test:
	cd services/api && python -m pytest -q
test-all:
	cd services/api && python -m pytest -q -m "integration or not integration"
readiness:
	@curl -s localhost:8000/ready | python -m json.tool || echo "api not running"
