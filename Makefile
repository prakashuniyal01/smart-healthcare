# Makefile for Django Project

# Variables
PROJECT_DIR=config
APPS_DIR=apps
VENV_DIR=.venv
DOCKER_IMAGE=django-lms
DOCKER_CONTAINER=django-lms

.PHONY: env install run build migrate makemigrations collectstatic docker-run docker-stop docker-remove clean test seed

# Target to create a Python virtual environment
env:
	@echo "Creating Python virtual environment in $(VENV_DIR)..."
	python3 -m venv $(VENV_DIR)

# Target to install Python dependencies
install: env
	@echo "Activating virtual environment and installing dependencies..."
	@. $(VENV_DIR)/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

# Target to run the application
run:
	@echo "Activating virtual environment and running the application..."
	@. $(VENV_DIR)/bin/activate && python manage.py runserver

# Target to apply database migrations
migrate:
	@echo "Applying database migrations..."
	@. $(VENV_DIR)/bin/activate && python manage.py migrate

# Target to make database migrations
makemigrations:
	@echo "Making migrations..."
	@. $(VENV_DIR)/bin/activate && python manage.py makemigrations $(APPS_DIR)

# Target to collect static files
collectstatic:
	@echo "Collecting static files..."
	@. $(VENV_DIR)/bin/activate && python manage.py collectstatic --noinput

# Target to build the Docker image
build:
	@echo "Building Docker image $(DOCKER_IMAGE)..."
	docker build -t $(DOCKER_IMAGE) .

# Target to run the Docker container
docker-run:
	@echo "Running Docker container $(DOCKER_CONTAINER)..."
	docker run -d -p 8000:8000 --name $(DOCKER_CONTAINER) --env-file $(PROJECT_DIR)/.env $(DOCKER_IMAGE)

# Target to stop the Docker container
docker-stop:
	@echo "Stopping Docker container $(DOCKER_CONTAINER)..."
	docker stop $(DOCKER_CONTAINER)

# Target to remove the Docker container
docker-remove:
	@echo "Removing Docker container $(DOCKER_CONTAINER)..."
	docker rm $(DOCKER_CONTAINER)

# Target to clean up virtual environment and temporary files
clean:
	@echo "Cleaning up: removing virtual environment and temporary files..."
	rm -rf $(VENV_DIR) *.pyc __pycache__
	@echo "Clean up completed."

# Target to seed the database with sample data
seed:
	@echo "Seeding the database with sample data..."
	@. $(VENV_DIR)/bin/activate && python manage.py loaddata apps/articles/fixtures/sample_data.json

# Target to run tests
test:
	@echo "Running tests..."
	@. $(VENV_DIR)/bin/activate && pytest $(APPS_DIR) --cov=$(APPS_DIR) -v

# Target to create superuser
superuser:
	@echo "Creating a Django superuser..."
	@. $(VENV_DIR)/bin/activate && python manage.py createsuperuser