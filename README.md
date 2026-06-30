# Study Planner FastAPI

A simple beginner-friendly study planner API.

## Features

- Signup and login
- JWT authentication
- Subjects CRUD
- Tasks CRUD
- Goals CRUD
- Scalar API docs
- Docker Postgres
- Basic Alembic setup
- Simple middleware header: `X-Process-Time`

## Run the database

```bash
docker compose up -d
```

## Environment

Create a `.env` file from `.env.example`:

```env
DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/studyplanner"
JWT_SECRET="change_this_secret"
JWT_ALGORITHM="HS256"
```

## Run the API

```bash
uvicorn main:app --reload
```

Open Scalar docs:

```text
http://127.0.0.1:8000/scalar
```

## How to use auth in Scalar

1. Call `POST /auth/signup`
2. Call `POST /auth/login`
3. Copy the `access_token`
4. Click the lock/auth button in Scalar
5. Paste only the token value
6. Now call protected endpoints:
   - `GET /auth/is_auth`
   - `GET /subjects/`
   - `GET /tasks/`
   - `GET /goals/`

## API routes

### Auth

- `POST /auth/signup`
- `POST /auth/login`
- `GET /auth/is_auth`
- `POST /auth/logout`

### Subjects

- `GET /subjects/`
- `POST /subjects/`
- `GET /subjects/{subject_id}`
- `PUT /subjects/{subject_id}`
- `DELETE /subjects/{subject_id}`

### Tasks

- `GET /tasks/`
- `POST /tasks/`
- `GET /tasks/{task_id}`
- `PUT /tasks/{task_id}`
- `DELETE /tasks/{task_id}`

### Goals

- `GET /goals/`
- `POST /goals/`
- `GET /goals/{goal_id}`
- `PUT /goals/{goal_id}`
- `DELETE /goals/{goal_id}`

## Alembic basics

Create a new migration later:

```bash
alembic revision --autogenerate -m "your message"
```

Run migrations:

```bash
alembic upgrade head
```

For now the app also uses `create_all_tables()` on startup to keep development easy.
