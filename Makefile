update:
	git pull

build: update; docker-compose build

start: docker-compose up -d

stop: docker-compose down

restart: stop start

deploy: update; docker-compose build; docker-compose up -d;
