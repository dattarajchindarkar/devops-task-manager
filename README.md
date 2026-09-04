# DevOps Task Manager API

A small Flask REST API designed as the application component of a DevOps assignment.

The application provides task management endpoints, configuration through environment variables, structured logging, automated tests, and a health endpoint that can later be used by Docker and Kubernetes health checks.

## Features

- REST API for task management
- `GET /` application information
- `GET /health` health check
- Create, read, update and delete tasks
- Request validation
- Environment-based configuration
- Application logging
- Automated tests with pytest
- Gunicorn application server
- Docker-ready
- Runs as a non-root container user

## Tech Stack

- Python 3.12
- Flask
- Gunicorn
- Pytest
- Docker
- Docker Compose

## Project Structure

```text
devops-task-manager/
├── app/
│   ├── __init__.py
│   └── routes.py
├── tests/
│   ├── __init__.py
│   └── test_api.py
├── run.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .env.example
├── .gitignore
└── README.md
```

## Configuration

Copy the example environment file:

```bash
cp .env.example .env
```

Available configuration:

```text
APP_NAME=DevOps Task Manager
APP_ENV=development
APP_VERSION=1.0.0
APP_PORT=8000
LOG_LEVEL=INFO
```

Do not commit `.env` or other secrets to Git.

## Run Locally

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python run.py
```

The API will be available at:

```text
http://localhost:8000
```

## API Endpoints

### Application information

```http
GET /
```

### Health check

```http
GET /health
```

Example response:

```json
{
  "status": "healthy",
  "application": "DevOps Task Manager"
}
```

### List tasks

```http
GET /tasks
```

### Get a task

```http
GET /tasks/1
```

### Create a task

```http
POST /tasks
Content-Type: application/json
```

Example:

```json
{
  "title": "Learn Docker",
  "description": "Understand containers",
  "priority": "high"
}
```

### Update a task

```http
PUT /tasks/1
Content-Type: application/json
```

Example:

```json
{
  "completed": true
}
```

### Delete a task

```http
DELETE /tasks/1
```

## Run Tests

```bash
pytest
```

The test suite covers:

- Application endpoint
- Health endpoint
- Task creation
- Input validation
- Missing resources
- Task updates
- Task deletion

## Run with Docker

Build the image:

```bash
docker build -t devops-task-manager .
```

Run the container:

```bash
docker run --env-file .env -p 8000:8000 devops-task-manager
```

Or use Docker Compose:

```bash
docker compose up --build
```

Stop the application:

```bash
docker compose down
```

View logs:

```bash
docker compose logs -f
```

## Data Storage

The current version intentionally uses in-memory storage.

This keeps the application focused on the DevOps assignment rather than database administration.

Because data is stored in memory, tasks are lost when the application process/container restarts.

A persistent database can be introduced later if required.

## DevOps Roadmap

The application is the first stage of the project.

```text
Application
    ↓
Automated Tests
    ↓
Docker
    ↓
GitHub Actions
    ↓
Kubernetes
    ↓
Amazon ECR
    ↓
Amazon ECS
    ↓
Application Load Balancer
    ↓
CloudWatch
```

The infrastructure and deployment stages will be added incrementally after the application and container are verified.
