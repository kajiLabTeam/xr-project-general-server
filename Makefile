-include .env

build:
	docker compose build

up:
	docker compose up -d

db:
	docker exec -it $(POSTGRES_HOST) psql -U $(POSTGRES_USER) -d $(POSTGRES_DB)

auth-server:
	docker exec -it application-authentication-server ash

area-server:
	docker exec -it area-estimation-server bash

spot-server:
	docker exec -it spot-estimation-server bash

object-server:
	docker exec -it object-server bash