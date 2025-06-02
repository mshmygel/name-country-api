@echo off
setlocal

if "%1" == "up" (
    docker-compose up -d
) else if "%1" == "build" (
    docker-compose build --no-cache
) else if "%1" == "migrate" (
    docker-compose exec web python manage.py migrate
) else if "%1" == "createsuperuser" (
    docker-compose exec web python manage.py createsuperuser
) else if "%1" == "down" (
    docker-compose down
) else if "%1" == "logs" (
    docker-compose logs -f web
) else if "%1" == "shell" (
    docker-compose exec web cmd
) else (
    echo Available commands: up, build, migrate, createsuperuser, down, logs, shell
)

endlocal
