PIP=venv/bin/pip
PYTHON=venv/bin/python
HONCHO=venv/bin/honcho

run: reqs
	${HONCHO} -f Procfile start

venv:
	test -d venv || virtualenv venv

reqs: requirements.txt venv
	${PIP} install -r requirements.txt

build:
	compass compile -e production --force
	mkdir -p build
	tar -v -czf build/draftsx.tgz --exclude ".git" --exclude "venv" \
							   --exclude "build/*" --exclude ".*cache*" \
							   --exclude "__pycache__" .

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

.PHONY: reqs build deploy
