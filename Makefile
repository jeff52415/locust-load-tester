.PHONY: up down logs scale clean test-single test-info

# Default number of workers to scale to
WORKERS ?= 4
HOST_PORT ?= 8080
CURL_OPTS ?= -s

# Start all services
up:
	mkdir -p data
	docker-compose up -d

# Stop all services
down:
	docker-compose down

# View logs of all services
logs:
	docker-compose logs -f

# Scale locust workers
scale:
	docker-compose up -d --scale locust-worker=$(WORKERS)

# Clean up containers and volumes
clean:
	docker-compose down -v
	rm -rf data

# Run a single test request against the embedding service
test-single:
	curl -X POST "http://localhost:$(HOST_PORT)/v1/embeddings" \
		-H "Content-Type: application/json" \
		-d '{"input":["What is Deep Learning?", "What is BGE M3?"]}'

# Test the info endpoint
test-info:
	@echo "Testing info endpoint..."
	@if ! curl $(CURL_OPTS) "http://127.0.0.1:$(HOST_PORT)/info"; then \
		echo "Error: Info endpoint test failed"; \
		exit 1; \
	fi

# Helper message
help:
	@echo "Available commands:"
	@echo "  make up              - Start all services"
	@echo "  make down            - Stop all services"
	@echo "  make logs            - View logs from all services"
	@echo "  make scale WORKERS=3 - Scale to specific number of workers"
	@echo "  make clean           - Clean up containers and volumes"
	@echo "  make test-single     - Test the embedding service with a single request"
	@echo "  make test-info       - Test the info endpoint" 