# Task-Tracker

Backend app, where you can create tasks for users
## Features
* **[FastAPI](https://github.com/tiangolo/fastapi)** backend
* **asynchronous-[SQLAlchemy](https://github.com/sqlalchemy/sqlalchemy)** models and ORM
* **[Alembic](https://github.com/sqlalchemy/alembic)** migrations
* **[Docker](https://www.docker.com/)** containerizing
* **Makefile** automating routine
* **[Poetry](https://github.com/python-poetry/poetry)** managing python packages
* **asynchronous-[Pytest](https://github.com/pytest-dev/pytest)** testing
* **[httpx](https://github.com/projectdiscovery/httpx)** asynchronous testing endpoints
* **[faker](https://github.com/joke2k/faker)** testing
* **Secure password** hashing by default
* **JWT token** authentication

## How to use

### Launch 

```
make up
```
Will pull, build and start 2 containers for application and database.
```
make down
```
Will stop both running containers

### Migrations

Project has a *initial* migrations file, to apply it, need to enter an app container:
```
make app-shell
```
You should see an output like:
```
root@d131e5ae1281:/app#
```
and then apply migrations:
```
root@d131e5ae1281:/app# make migrate
```
If you changed the models, you can create a migration file using:
```
root@d131e5ae1281:/app# make migration
```
and then run it as stated earlier.

### Tests

To start tests, need to apply migrations, and after that run in container:
```
root@d131e5ae1281:/app# make test
```
You can see results of tests in db shell (run it in your shell, not in container):
```
make db-shell
```
You should see an output like:
```
root@b76c025c43d5:/#
```
You can also start psql:
```
root@b76c025c43d5:/# psql -U postgres -d app
```

## Truncate db

```
docker-compose down -v --remove-orphans
```
Run it in your shell, it will stop runnig containers and undo all actions, such as test data in db

## Endpoints

To access documentation, open **0.0.0.0:8000/docs**, you will see the automatic interactive API documentation (provided by [Swagger UI](https://swagger.io/)), or **0.0.0.0:8000/redoc**, will see the alternative automatic documentation (provided by [ReDoc](https://github.com/Redocly/redoc)).

## Project structure 

```
.
├── alembic.ini                     - a generic, single database configuration      
├── app
│   ├── api                       
│   │   ├── api_v1                
│   │   │   ├── api.py              - API router
│   │   │   ├── endpoints          
│   │   │   │   ├── __init__.py
│   │   │   │   ├── login.py
│   │   │   │   ├── tasks.py
│   │   │   │   └── users.py
│   │   │   ├── __init__.py
│   │   ├── deps.py                 - endpoints dependencies
│   │   ├── __init__.py
│   ├── core
│   │   ├── config.py               - application settings
│   │   ├── __init__.py
│   │   └── security.py             - JWT and password stuff
│   ├── crud
│   │   ├── base.py
│   │   ├── crud_task.py
│   │   ├── crud_user.py
│   │   ├── __init__.py
│   ├── db
│   │   ├── base_class.py           - base async class for tables
│   │   ├── base.py
│   │   ├── __init__.py
│   │   └── session.py              - async engine and session
│   ├── __init__.py
│   ├── main.py                     - application instance
│   ├── models                      - database models
│   │   ├── __init__.py
│   │   ├── task.py
│   │   ├── user.py
│   │   └── user_task.py
│   └── schemas                     - Pydantic schemas
│       ├── __init__.py
│       ├── task.py
│       ├── token.py
│       └── user.py
├── migrations
│   ├── env.py                      - migrations configuration
│   ├── script.py.mako
│   └── versions
│       ├── 355a9617c26e_initial.py - initial migration
└── tests
    ├── api
    │   ├── api_v1
    │   │   ├── __init__.py
    │   │   ├── test_tasks.py
    │   │   └── test_users.py
    │   ├── __init__.py
    ├── conftest.py                 - tests fixtures
    ├── crud
    │   ├── __init__.py
    │   ├── test_tasks.py
    │   └── test_users.py
    ├── __init__.py
    └── utils                       - tests utilities 
        ├── __init__.py
        ├── tasks.py
        ├── users.py
        └── utils.py
```