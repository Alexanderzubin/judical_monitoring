# Tools

# Targets
.PHONY: check format up down infra reset-db

check:
	ruff check --fix --unsafe-fixes .

format:
	ruff format .

up:
	docker compose up -d

run-local-bot:
	python -m app.bot

run-local-scheduler:
	celery -A app beat --loglevel=info

run-local-worker:
	celery -A app worker --loglevel=info

stop:
	docker compose stop

infra:
	docker compose up -d postgres redis migrator

reset-db:
	docker compose run --rm migrator alembic downgrade base
	docker compose run --rm migrator alembic upgrade head