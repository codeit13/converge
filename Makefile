.PHONY: up down build logs frontend-build restart clean status

up:
	@echo "Starting all services via Docker Compose..."
	docker-compose up -d
	@echo "Docker services status:"
	docker-compose ps

down:
	@echo "Stopping all services..."
	docker-compose down

build:
	@echo "Building all services..."
	docker-compose build

restart:
	@echo "Restarting all services..."
	docker-compose restart

logs:
	@echo "Showing logs..."
	docker-compose logs -f

frontend-build:
	@echo "Building frontend..."
	cd frontend && yarn install && yarn build

clean:
	@echo "Cleaning up Docker resources..."
	docker-compose down -v --remove-orphans

status:
	@echo "Docker services status:"
	docker-compose ps
