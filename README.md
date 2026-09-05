# DevOps Task Manager

A simple Flask-based Task Manager application created to demonstrate practical DevOps concepts including automated testing, Docker containerization, GitHub Actions CI/CD, Kubernetes deployment, and AWS deployment.

The application is intentionally simple because the main focus is on the DevOps implementation rather than application complexity.

## Technology Stack

- Python 3.12
- Flask
- Gunicorn
- Pytest
- Docker
- Docker Compose
- GitHub Actions
- Kubernetes
- Kind
- Amazon ECR
- Amazon EC2
- AWS IAM

## Application Features

The application provides a simple interface for creating and managing tasks.

Each task contains:

- Title
- Description
- Priority
- Completion status

### API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Task Manager web interface |
| GET | `/health` | Application health check |
| GET | `/api/info` | Application information |
| GET | `/tasks` | Get all tasks |
| POST | `/tasks` | Create a task |
| GET | `/tasks/<id>` | Get a task |
| PUT | `/tasks/<id>` | Update a task |
| DELETE | `/tasks/<id>` | Delete a task |

## Project Structure

```text
devops-task-manager/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── templates/
│   │   └── index.html
│   └── static/
│       ├── app.js
│       └── style.css
├── tests/
│   ├── __init__.py
│   └── test_api.py
├── k8s/
│   ├── configmap.yaml
│   ├── deployment.yaml
│   └── service.yaml
├── docs/
│   ├── linux-networking.md
│   └── aws-deployment.md
├── .github/
│   └── workflows/
│       └── ci.yml
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .env.example
├── .gitignore
├── requirements.txt
├── run.py
└── README.md
 Author

DevOps Task Manager

Repository:

https://github.com/dattarajchindarkar/devops-task-manager