.PHONY: up build migrate createsuperuser down logs shell restart

up:
	docker-compose up -d

build:
	docker-compose build --no-cache

migrate:
	docker-compose exec web python manage.py migrate

createsuperuser:
	docker-compose exec web python manage.py createsuperuser

down:
	docker-compose down

logs:
	docker-compose logs -f web

shell:
	docker-compose exec web bash

restart: down up
