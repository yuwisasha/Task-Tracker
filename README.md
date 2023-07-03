# Task-Tracker
Backend app, where you can create tasks for users
## Technologies
* **[FastAPI]**(https://github.com/tiangolo/fastapi) backend
* **async-[SQLAlchemy]**(https://github.com/sqlalchemy/sqlalchemy) models
* **[Alembic]**(https://github.com/sqlalchemy/alembic) migrations
* **[Docker]**(https://www.docker.com/) containerizing
* **Makefile** automating routine
* **[Poetry]**(https://github.com/python-poetry/poetry) managing python packages
* **async-[Pytest]**(https://github.com/pytest-dev/pytest) testing
* **[httpx]**(https://github.com/projectdiscovery/httpx) testing
* **[faker]**(https://github.com/joke2k/faker) testing

## Launch
```
make build
make up
```
* You shoul open a bash in docker containers
```docker -it exec app /bin/bash/``` to open a bash in app container and apply migrations ```make migrate```
* Open **0.0.0.0:8000/docs** for **SwaggerUI** and test APIs.