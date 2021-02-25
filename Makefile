VIRTUALENV_NAME=.env

update:
	git pull;

build:
	docker-compose build --parallel --compress;

start:
	docker-compose up -d --remove-orphans;

stop:
	docker-compose down;

restart: stop start

deploy: update; docker-compose build --parallel --compress; docker-compose up -d --remove-orphans;

install_requirements:
	@echo "Install requirements.txt:"
	$(VIRTUALENV_NAME)/bin/pip3 install -r requirements.txt

create_venv:
	@echo "Creating virtual env:"
	python3 -m venv --clear $(VIRTUALENV_NAME)
	$(VIRTUALENV_NAME)/bin/pip3 install --upgrade pip

clean:
	@echo "Cleaning Python compiled files:"
	find . -name __pycache__ -exec rm -fr {} +
	find . -name '*.pyc' -delete
