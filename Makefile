PIP=venv/bin/pip
PYTHON=venv/bin/python
HONCHO=venv/bin/honcho

run:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

production:
	docker-compose up

build:
	docker-compose build

deploy: build
	scp build/draftsx.tgz draft.sx:/home/lucas
	ssh draft.sx '	mv draft.sx "$(shell date +"%s")" && \
					mkdir draft.sx && \
					tar -xzf draftsx.tgz -C draft.sx && \
					cd draft.sx && \
					virtualenv venv && \
					venv/bin/pip install -r requirements.txt && \
					cd .. && \
					sudo /usr/local/bin/draftsx-restart \
				'

.PHONY: run build deploy
