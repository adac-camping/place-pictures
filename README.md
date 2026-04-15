# django-template

Basic template configuration for a django application.

It can be used both for
- Web development
- and/or internal service development (through management/command module of django-template).

## Project and app generation
After cloning the repo, you'll want to create your new Django project and the first app.

```
pipenv install --dev
pipenv shell
django-admin startproject django_project .
django-admin startapp app_name_here
```

This will generate the `manage.py` development script, as well as the project and app directories.
The setting will be at `django_project/settings.py`.

## Docker configuration
Contains both a Dockerfile for basic configuration (without a db config) and a docker-compose
for local development.

### Docker - Storage
In case a database is needed both Dockerfile and docker-compose needs to be updated
in order to handle the db resource. The same applies to any kind of storage. 
This template is agnostic in terms of storage.

### Docker - Ports
Exposing ports through Dockerfile and docker-compose needs to be handled manually if needed.
The exposed ports for the local machines needs to be documented here: 
https://adac-camping.atlassian.net/wiki/spaces/DEV/pages/1975025665/Local+Docker-Compose+ports

### Docker - Naming conventions
For naming conventions simply rename the services in docker-compose regarding the name
of the repository or service that you are creating


### Docker - Networking
All the containers that have public access by an API needs to connect in docker-compose
based on the `pincamp-local-net` network. In that way we can connect multiple
containers together locally. 

The non-public accessed containers needs to be configured for the bridge network inside 
the docker-compose pseudo-cluster

## Makefile
Contains basic commands for building and running the django project. It can be 
extended based on the needs.

## Django
Each concretion of this template needs to create through django a new django application
based on the main (manage.py) commands of django

## CircleCi CI/CD
