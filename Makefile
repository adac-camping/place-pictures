ifndef VERBOSE
MAKEFLAGS += --no-print-directory
endif

.DEFAULT_GOAL := help
PYTHON_CONTAINER := repo

help:
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | column -t -s'##'

build.dev: ## Build development image
	- make files
	# We need to pass UID values as build arguments here, in order to
	# prevent permission issues in CircleCI.
	docker-compose build --build-arg UID=`id -u`

build.prod: ## Build production image
	touch .env # In CircleCI will create an empty file
	docker-compose build --build-arg ENV=prod $(PYTHON_CONTAINER)

prod: ## Start production server inside the current container
	ddtrace-run gunicorn -w 9 --preload --bind 0.0.0.0:8000 --access-logfile - place_pictures.wsgi

tests: ## Run all tests
	docker-compose run --rm $(PYTHON_CONTAINER) pytest ${PYTEST_OPTS} ${PYTEST_FILES}

shell: ## Open an interactive shell inside the python container
	docker-compose run --rm $(PYTHON_CONTAINER) /bin/bash

server: ## Starts django development server
	docker-compose run --service-ports --rm $(PYTHON_CONTAINER) python manage.py runserver 0.0.0.0:8000

update.pipenv: ## Run 'pipenv update' inside the container
	docker-compose run --no-deps --rm $(PYTHON_CONTAINER) pipenv update

clear.pipenv: ## Run 'pipenv lock --clear' inside the container
	docker-compose run --no-deps --rm $(PYTHON_CONTAINER) pipenv lock --clear

lint: ## Check code formatting
	docker-compose run --no-deps --rm $(PYTHON_CONTAINER) isort --check-only .
	docker-compose run --no-deps --rm $(PYTHON_CONTAINER) flake8 .
	docker-compose run --no-deps --rm $(PYTHON_CONTAINER) black --check .

fix.lint: ## Automatically fix code formatting
	make fix.isort
	make fix.black

fix.isort: ## Run isort to fix code formatting
	docker-compose run --no-deps --rm $(PYTHON_CONTAINER) isort .

fix.black: ## Run black to fix code formatting
	docker-compose run --no-deps --rm $(PYTHON_CONTAINER) black .

down.containers: ## Shutdown all containers
	docker-compose down

nuclear.containers: ## Shutdown all containers and remove all volumes
	docker-compose down -v --remove-orphans --rmi all

files: ## Make default essential files (if not exist) to run containers
	cp -n .env.example .env || true

django.migrate: ## Run Django database migrations
	docker-compose run $(PYTHON_CONTAINER) python manage.py migrate

django.makemigration: ## Create new Django migrations
	docker-compose run $(PYTHON_CONTAINER) python manage.py makemigrations

cron.tag_images: ## Run the local image tagging job
	docker-compose run --rm $(PYTHON_CONTAINER) python manage.py tag_images

.PHONY: help build.dev build.prod shell lint files help tests cron.tag_images

$(V).SILENT:

SHELL = /bin/sh
