# Python FastAPI

## Dependencies
```text
- fastapi[standard]   FastAPI
- sqlalchemy          ORM
- asyncpg             PostgreSQL driver (asynchronous database access)
- psycopg[binary]     PostgreSQL driver (synchronous database access. use for alembic migrations)
- alembic             DB migrations
- pwdlib[argon2]      Password hashing
```

## Quick Start (local)

### 1) Start PostgreSQL (Docker)

```bash
docker compose up -d
```
This starts Postgres on localhost:5432 using the credentials in `docker-compose.yml`.

### 2) Run the API

```bash
fastapi dev
```
Server started at http://localhost:8000

Documentation at http://localhost:8000/docs (Swagger UI)

Documentation at http://localhost:8000/redoc (ReDoc)

## Alembic Guide

- Generate migration
```bash
alembic revision --autogenerate -m "create users table"
```

- Show migration history
```bash
alembic history
```

- Apply migration (THIS updates DB)
```bash
alembic upgrade head
```
- Go back one version
```bash
alembic downgrade -1
```

- See current DB version
```bash
alembic current
```

**To fully remove the last revision in Alembic, you need to revert the changes in the database and then delete the migration file.**

1. Roll back the Database State

    If you have already applied the migration to your database using `alembic upgrade`, you must first run a relative downgrade to step back by one revision:
    ```bash
    alembic downgrade -1
    ```

2. Verification

    To ensure everything is clean and your local state matches the database, run:
    ```bash
    alembic current
    ```
    This will confirm your database is now pointed at the previous valid revision hash.

3. Delete the Migration File

    Once the database is safely pointing to the previous revision, manually remove the python migration file from project directory
    - Open project's version folder (at `alembic/versions/`)
    - Find the script starting with the unique hash of your last revision (e.g., `1a2b3c4d5e6f_your_migration_name.py`).


> If you generated the file using `alembic revision --autogenerate` but never actually ran `alembic upgrade head`, you do not need to run the downgrade command. You can simply *delete the file* from the versions folder right away.