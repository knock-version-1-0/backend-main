build:
	docker build -t api/main .

runserver:
	docker run -p 8000:8000 --name api_main api/main

clean:
	docker stop api_main
	docker rm api_main
	docker rmi api/main

rebuild:
	docker stop api_main
	docker rm api_main
	docker rmi api/main
	docker build -t api/main .
	docker run -p 8000:8000 --name webapp api/main
