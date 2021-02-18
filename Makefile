update:
	git pull;

build: docker-compose build --parallel --compress;

start:
	docker-compose up -d --remove-orphans;

stop:
	docker-compose down;

restart: stop start

deploy: update; docker-compose build --parallel --compress; docker-compose up -d --remove-orphans;
