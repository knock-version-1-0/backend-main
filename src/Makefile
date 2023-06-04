build:
	docker build --no-cache -t api/main .

runserver:
	docker run -p 8000:8000 --name api_main --network backend-main_default api/main

runserver-d:
	docker run -d -p 8000:8000 --name api_main --network backend-main_default api/main

shell:
	docker exec -it api_main bash

down:
	docker stop api_main
	docker rm api_main
	docker rmi api/main

clean:
	docker stop api_main redis postgres cache_default
	docker rm api_main redis postgres cache_default
	docker rmi api/main redis:latest postgres:14.2 memcached:latest

restart:
	docker stop api_main
	docker rm api_main
	docker rmi api/main
	docker build -t api/main .
	docker run -p 8000:8000 --name api_main --network backend-main_default api/main

dev-environment:
	docker-compose -f ../docker-compose.env.yaml up -d
