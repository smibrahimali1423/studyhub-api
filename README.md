# StudyHub API

A REST API for organising study notes by subject, built with FastAPI and PostgreSQL. Users sign
up, log in with a JWT, and manage their own subjects and the notes inside them.

## Tech

FastAPI, SQLAlchemy, PostgreSQL, Alembic migrations, JWT (python-jose), bcrypt password hashing
(passlib), Redis, Docker Compose.

## Endpoints

Routes marked 🔒 need an `Authorization: Bearer <token>` header from `/auth/login`.

| Method | Path | What it does |
|---|---|---|
| `POST` | `/auth/signup` | Create an account |
| `POST` | `/auth/login` | Log in; returns an access token (expires after 30 minutes) |
| `GET` | `/auth/me` 🔒 | The signed-in user |
| `POST` | `/subjects/` 🔒 | Create a subject |
| `GET` | `/subjects/` 🔒 | List your subjects |
| `GET` | `/subjects/{subject_id}` 🔒 | Get one subject |
| `DELETE` | `/subjects/{subject_id}` 🔒 | Delete a subject |
| `POST` | `/notes/` 🔒 | Add a note to one of your subjects |
| `GET` | `/notes/subject/{subject_id}` 🔒 | List the notes in a subject |
| `GET` | `/notes/{note_id}` 🔒 | Get one note |
| `DELETE` | `/notes/{note_id}` 🔒 | Delete a note |

Every protected request also checks a Redis token blacklist, so revoked tokens are rejected
until they expire.

Interactive docs: <http://localhost:8000/docs>.

## Running it

```bash
cp .env.example .env      # set SECRET_KEY to a long random string
docker compose up --build
docker compose exec api alembic upgrade head
```

This starts PostgreSQL, Redis and the API on <http://localhost:8000>.

| Variable | Meaning |
|---|---|
| `DATABASE_URL` | PostgreSQL connection string |
| `SECRET_KEY` | Secret used to sign tokens |
| `ALGORITHM` | JWT signing algorithm (HS256) |
| `REDIS_HOST` | Redis host (defaults to `redis`) |
