-include .env

up:
	sudo docker compose build && docker compose up -d

logs:
	sudo docker compose logs -f

down:
	sudo docker compose down

db:
	sudo docker exec -it $(POSTGRES_HOST) psql -U $(POSTGRES_USER) -d $(POSTGRES_DB)

auth-server:
	sudo docker exec -it application-authentication-server ash

area-server:
	sudo docker exec -it area-estimation-server bash

spot-server:
	sudo docker exec -it spot-estimation-server bash

object-server:
	sudo docker compose exec object-server sh
