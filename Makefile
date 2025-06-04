.PHONY: up build migrate makemigrations makemigrations-names createsuperuser down logs shell restart

up:
	docker-compose up -d

build:
	docker-compose build --no-cache

migrate:
	docker-compose exec web python manage.py migrate

makemigrations:
	docker-compose exec web python manage.py makemigrations

makemigrations-names:
	docker-compose exec web python manage.py makemigrations names

createsuperuser:
	docker-compose exec web python manage.py createsuperuser

down:
	docker-compose down

logs:
	docker-compose logs -f web

shell:
	docker-compose exec web bash

restart: down up
