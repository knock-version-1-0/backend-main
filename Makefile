up-dev:
	docker-compose -f docker-compose.dev.yaml up -d

up-prod:
	docker-compose -f docker-compose.prod.yaml up -d

down-dev:
	docker-compose -f docker-compose.dev.yaml down --remove-orphans

down-prod:
	docker-compose -f docker-compose.prod.yaml down --remove-orphans

clean:
	docker stop api_main postgres nginx redis cache_default
	docker rm api_main postgres nginx redis cache_default
	docker rmi api/main nginx:latest postgres:14.2 memcached:latest redis:latest

shell-db:
	docker exec -it postgres bash

shell-app:
	docker exec -it api_main bash

shell-nginx:
	docker exec -it nginx bash

shell-cache:
	docker exec -it cache_default bash
