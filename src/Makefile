build:
	docker build -t backend-webapp .

runserver:
	docker run -p 8000:8000 --name webapp backend-webapp

clean:
	docker stop webapp
	docker rm webapp
	docker rmi backend-webapp

rebuild:
	docker stop webapp
	docker rm webapp
	docker rmi backend-webapp
	docker build -t backend-webapp .
	docker run -p 8000:8000 --name webapp backend-webapp
