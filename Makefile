-include .env

up:
	docker compose build && docker compose up -d

logs:
	docker compose logs -f

db:
	docker exec -it $(POSTGRES_HOST) psql -U $(POSTGRES_USER) -d $(POSTGRES_DB)

auth-server:
	docker exec -it application-authentication-server ash

area-server:
	docker exec -it area-estimation-server bash

spot-server:
	docker exec -it spot-estimation-server bash

object-server:
	docker compose exec object-server sh
