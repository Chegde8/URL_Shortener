# Makefile for URL Shortening Service

# Variables
APP_NAME = url-shortening-service
DOCKER_IMAGE = mcr.microsoft.com/mssql/server:2022-latest
DOCKER_CONTAINER = url_db
DB_PASSWORD = SqlPassword.2024
FLASK_APP = src/main.py
SHELL := /bin/bash

# Targets
.PHONY: build-db stop-db clean-db install-deps run-flask install-activate-venv delete-venv clean

# Meta targets
clean: stop-db clean-db delete-venv

# Setup targets
install-activate-venv:
	sudo apt-get install python3-venv
	python3 -m venv url_shortener_env
	source url_shortener_env/bin/activate

delete-venv:
	# delete virtual environment
	rm -rf url-shortening-service/venv

install-deps:
	# install dependencies
	pip install -r requirements.txt

	# install odbc driver
	sudo apt-get install curl apt-transport-https
	curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
	curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list | sudo tee /etc/apt/sources.list.d/msprod.list
	sudo apt-get update
	sudo ACCEPT_EULA=Y apt-get install -y msodbcsql18
	odbcinst -j

	# install curl
	sudo apt-get install curl

# SQL db targets
build-db:
	sudo docker pull $(DOCKER_IMAGE)
	sudo docker run -e 'ACCEPT_EULA=Y' -e 'MSSQL_SA_PASSWORD=$(DB_PASSWORD)' -p 1433:1433 --name $(DOCKER_CONTAINER) -d $(DOCKER_IMAGE)

stop-db:
	sudo docker stop $(DOCKER_CONTAINER)

clean-db:
	sudo docker rm -f $(DOCKER_CONTAINER)

# Flask targets
run-flask:
	export FLASK_APP=$(FLASK_APP)
	python3 src/main.py

# setup db
setup-db:
	python src/main.py --dbsetup
