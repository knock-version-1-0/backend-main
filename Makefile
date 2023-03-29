up dev:
	docker-compose -f docker-compose-dev.yaml up -d

up-prod:
	docker-compose -f docker-compose-prod.yaml up -d

down-dev:
	docker-compose -f docker-compose-dev.yaml down --remove-orphans

clean:
	docker stop webapp postgres nginx
	docker rm webapp postgres nginx
	docker rmi backend-webapp nginx:latest postgres:14.2

shell-db:
	docker exec -it postgres bash

shell-app:
	docker exec -it webapp bash

shell-nginx:
	docker exec -it nginx bash
