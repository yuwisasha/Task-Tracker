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
# Launch 
```
make up
```
Will pull, build and start 2 containers for application and database.
```
make down
```
Will stop both running containers
# Migrations
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
# Tests
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
# Truncate db
```
docker-compose down -v --remove-orphans
```
If you run it in your shell, it will stop runnig containers and undo all actions, such as test data in db