@echo off
setlocal

if "%1" == "up" (
    docker-compose up -d
) else if "%1" == "build" (
    docker-compose build --no-cache
) else if "%1" == "migrate" (
    docker-compose exec web python manage.py migrate
) else if "%1" == "makemigrations" (
    docker-compose exec web python manage.py makemigrations
) else if "%1" == "makemigrations-names" (
    docker-compose exec web python manage.py makemigrations names
) else if "%1" == "createsuperuser" (
    docker-compose exec web python manage.py createsuperuser
) else if "%1" == "down" (
    docker-compose down
) else if "%1" == "logs" (
    docker-compose logs -f web
) else if "%1" == "shell" (
    docker-compose exec web cmd
) else if "%1" == "restart" (
    docker-compose down && docker-compose up -d
) else (
    echo Available commands: up, build, migrate, makemigrations, makemigrations-names, createsuperuser, down, logs, shell, restart
)

endlocal
