# Task Management Api

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=flat&logo=pydantic&logoColor=white)](https://docs.pydantic.dev/)
[![Alembic](https://img.shields.io/badge/Alembic-Migrations-blue?style=flat&logo=python)](https://alembic.sqlalchemy.org/)
[![Auth](https://img.shields.io/badge/Auth-JWT%20%2F%20OAuth2-orange?style=flat&logo=json-web-tokens)](https://jwt.io/)

Task Management REST API built with FastAPI and PostgreSQL. Features secure JWT authentication, relational database architecture via SQLAlchemy, and fully containerized environments using Docker and Docker Compose.

## Features

- User registration and authentication
- JWT authentication
- Workspace management
- Task management
- PostgreSQL
- Database migrations
- Automated tests
- Docker

## 🛠 Tech Stack
* **Python**
* **FastAPI**
* **PostgreSQL**
* **SQLAlchemy**
* **Alembic**
* **Pydantic**
* **Pytest**
* **Docker**

## 📁 Project Structure

```text
Task-Management-Api/
│
├── app/
│   ├── routers/
│   │   ├── authentication.py
│   │   ├── workspaces.py
│   │   └── tasks.py
│   ├── auth.py
│   ├── config.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
├── tests/
│   ├── api/
│   │   └── test_endpoints.py
│   ├── unit/
│   │   └── test_unitarios.py
│   └── conftest.py
├── alembic/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── README.md
├── .env.example
├── .dockerignore
└── .gitignore
```

---

## 💻 How to run

Ensure you have **Docker** and **Docker Compose** installed on your system.

1. Clone this repository:
   ```bash
   git clone https://github.com/AndresPimentel-dev/Task-Management-Api.git
   cd Task-Management-Api
   ```

2. Create a `.env` file based on `.env.example`:
   ```env
   DATABASE_URL=postgresql://postgres:your_password@localhost:5432/taskforge_db
   POSTGRES_PASSWORD=your_password
   SECRET_KEY=your_secret_key_super_very_secret_and_long
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

3. Run with Docker Compose:
   ```bash
   docker compose up --build
   ```

## 💻 Testing

1. Create a virtual environment and activate it:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies and run tests:
   ```bash
   pip install -r requirements.txt
   pytest
   ```

## 🔎 API Documentation

Interactive Swagger UI available at:
`http://localhost:8000/docs`

---

## 📡 API Endpoints

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1.0/auth/register` | Register a new user and receive a JWT token |
| `POST` | `/api/v1.0/auth/login` | Login with username/email and password |

### Workspaces

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1.0/workspaces` | Get all workspaces owned by the user |
| `GET` | `/api/v1.0/workspaces/{workspace_id}` | Get a specific workspace by ID |
| `POST` | `/api/v1.0/workspaces` | Create a new workspace |
| `PUT` | `/api/v1.0/workspaces/{workspace_id}` | Update a workspace |
| `DELETE` | `/api/v1.0/workspaces/{workspace_id}` | Delete a workspace (cascades tasks) |

### Tasks

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1.0/tasks` | Get all tasks (optional filter: `?workspace_id=X&status=todo`) |
| `GET` | `/api/v1.0/tasks/{task_id}` | Get a task by ID |
| `POST` | `/api/v1.0/tasks` | Create a new task inside a workspace |
| `PUT` | `/api/v1.0/tasks/{task_id}` | Update task details or status |
| `DELETE` | `/api/v1.0/tasks/{task_id}` | Delete a task |

## 🎯 Project Scope

This is a **junior-level backend project** created to demonstrate the ability to build and organize a basic REST API.

It is not intended to be presented as a production-ready system. Instead, it serves as a foundation for progressively more advanced projects involving authentication, testing, architecture, deployment, and scalability.

## 📄 License

This project is licensed under the [MIT License](LICENSE).