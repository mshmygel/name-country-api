# Stage 1: Builder
FROM python:3.12-slim AS builder

WORKDIR /app

# Install system dependencies for psycopg2
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock ./

RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

COPY . .

# Collect static files for admin UI
RUN python manage.py collectstatic --noinput


# Stage 2: Runtime
FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.12 /usr/local/lib/python3.12
COPY --from=builder /usr/local/bin /usr/local/bin
COPY . .

# Copy static files from build stage
COPY --from=builder /app/staticfiles /app/staticfiles

EXPOSE 8000

ENV DJANGO_SETTINGS_MODULE=name_country.settings

CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn name_country.wsgi:application --bind 0.0.0.0:8000"]
