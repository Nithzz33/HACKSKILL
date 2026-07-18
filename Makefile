.PHONY: help setup test dev catalyst-demo catalyst-bundle prod clean

help:
	@echo "Secure Crime Intelligence Platform"
	@echo "make setup  - create venv and install dependencies"
	@echo "make test   - run tests"
	@echo "make dev    - run local API"
	@echo "make catalyst-demo   - run AppSail-style local demo"
	@echo "make catalyst-bundle - create managed-runtime AppSail bundle"
	@echo "make prod   - start production-shape compose stack"
	@echo "make clean  - stop compose stack"

setup:
	python -m venv .venv
	.venv/Scripts/python -m pip install --upgrade pip
	.venv/Scripts/pip install -r requirements.txt

test:
	.venv/Scripts/pytest

dev:
	.venv/Scripts/uvicorn secure_crime_api.app:app --app-dir src --host 127.0.0.1 --port 8000 --reload

catalyst-demo:
	.venv/Scripts/python -m secure_crime_api.catalyst_entry

catalyst-bundle:
	.venv/Scripts/python scripts/build_catalyst_appsail.py

prod:
	docker compose -f docker-compose.prod.yml up --build

clean:
	docker compose -f docker-compose.prod.yml down
