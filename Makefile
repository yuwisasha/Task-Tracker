build:
	docker-compose build
up:
	docker-compose up -d
down:
	docker-compose down
migration:
	alembic revision --autogenerate -m "Initial"
migrate:
	alembic upgrade head