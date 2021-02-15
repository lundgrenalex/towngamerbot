update:
	git pull

build: update; docker-compose build

deploy: update; docker-compose build; start

start: docker-compose up -d

stop: docker-compose down

restart: stop start
