build:
	docker build . -t knock-server

runserver:
	docker run -p 8000:8000 --name knock-server knock-server

clean:
	docker stop knock-server
	docker rm knock-server
	docker rmi knock-server

rebuild:
	docker stop knock-server
	docker rm knock-server
	docker rmi knock-server
	docker build . -t knock-server
	docker run -p 8000:8000 --name knock-server knock-server
