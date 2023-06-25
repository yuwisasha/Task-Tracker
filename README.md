## Launch
```
make build
make up
```
* You shoul open a bash in docker containers
```docker -it exec app /bin/bash/``` to open a bash in app container and apply migrations ```make migrate```
* Open **0.0.0.0:8000/docs** for **SwaggerUI** and test APIs.