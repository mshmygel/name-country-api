# 🌟 Name-Country API

A Django RESTful backend that predicts the nationality of a given name and lists the most frequent names per country. Powered by external APIs and secured with JWT.

---

## 📌 Table of Contents

* [🌐 Overview](#-overview)

* [✨ Features](#-features)

* [🛠 Tech Stack](#-tech-stack)

* [🪟 System Requirements](#-system-requirements)

* [⚙️ Installation](#-installation)

  * [Poetry Setup](#poetry-setup)
  * [Environment Configuration](#environment-configuration)
  * [Docker Setup](#docker-setup)
  * [Running Commands](#running-commands)

* [📂 API Documentation](#-api-documentation)

* [🚪 Admin Panel](#-admin-panel)

* [🔮 Testing](#-testing)

* [🔍 API Endpoints](#-api-endpoints)

---

## 🌐 Overview

This API allows users to input a name and receive predicted nationalities, as well as view the most popular names per country. All predictions are cached and refreshed using nationalize.io and REST Countries data.

## ✨ Features

* JWT authentication (`djangorestframework-simplejwt`)
* Swagger & Redoc auto-generated docs via `drf-spectacular`
* Name lookup using nationalize.io
* Country enrichment from restcountries.com
* Top-5 name analytics per country
* Admin panel customization with Jazzmin
* Dockerized setup for dev/prod environments

## 🛠 Tech Stack

* Python 3.12
* Django 5.2
* Django REST Framework
* PostgreSQL
* Docker & Docker Compose
* Poetry (dependency management)
* Jazzmin (admin UI customization)

## 🪟 System Requirements

* Python >= 3.12
* Poetry
* Docker & Docker Compose

## ⚙️ Installation

### Poetry Setup

```bash
    python -m venv .venv
    .venv\Scripts\activate  # Windows
    source .venv/bin/activate  # macOS/Linux
    pip install poetry
    poetry install
```

### Environment Configuration

```bash
    copy .env.sample .env  # Windows
    cp .env.sample .env     # macOS/Linux
```

### Docker Setup

> 🫠 Windows:

```bash
    .\make build
    .\make up
```

> 🍏 macOS/Linux:

```bash
    make build
    make up
```

### Running Commands

> 🫠 Windows:

```bash
    .\make migrate
    .\make createsuperuser
    .\make up
    .\make down
    .\make logs
    .\make restart
```

> 🍏 macOS/Linux:

```bash
    make migrate
    make createsuperuser
    make up
    make down
    make logs
    make restart
```

## 📂 API Documentation

* Swagger UI: [http://localhost:8000/docs/](http://localhost:8000/docs/)
* Redoc: [http://localhost:8000/redoc/](http://localhost:8000/redoc/)
* Schema: [http://localhost:8000/schema/](http://localhost:8000/schema/)

## 🚪 Admin Panel

* Jazzmin-powered Django Admin: [http://localhost:8000/admin/](http://localhost:8000/admin/)

## 🔮 Testing

Run tests:

```bash
    docker compose exec web python manage.py test
```

## 🔍 API Endpoints

* `POST /api/token/` — obtain JWT
* `POST /api/token/refresh/` — refresh JWT
* `GET /names/?name=...` — predict countries for a given name
* `GET /popular-names/?country=...` — get most frequent names by country

---

📆 Uses Poetry for dependencies. Jazzmin for admin interface. External APIs: nationalize.io, restcountries.com

