PIP=venv/bin/pip
PYTHON=venv/bin/python
HONCHO=venv/bin/honcho

run:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

production:
	docker-compose up

build:
	docker-compose build

deploy:
	scripts/deploy

.PHONY: run build deploy
