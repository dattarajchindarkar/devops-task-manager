
# AWS Deployment Documentation

## 1. Overview

The DevOps Task Manager is deployed on AWS using **Amazon EC2** and **Docker**.

GitHub Actions builds the Docker image and pushes it to **Amazon Elastic Container Registry (ECR)**. The EC2 instance then authenticates with ECR, pulls the image, and runs the application as a Docker container.

The deployment demonstrates:

- AWS IAM
- GitHub Actions OIDC
- Amazon ECR
- Amazon EC2
- VPC networking
- Security Groups
- Docker
- Application access
- CloudWatch monitoring

---

## 2. Architecture

```text
Developer
    |
    v
GitHub Repository
    |
    v
GitHub Actions
    |
    | OIDC Authentication
    v
AWS IAM
    |
    v
Amazon ECR
    |
    | Docker Image
    v
AWS VPC
    |
    v
Security Group
    |
    v
Amazon EC2
    |
    v
Docker Container
    |
    | Port 80 → 8000
    v
Flask Application
    |
    v
Internet
````

---

## 3. AWS Runtime

The selected runtime for this project is:

```text
Amazon EC2 + Docker
```

EC2 was selected because it provides a simple environment for demonstrating:

* Linux server administration
* Docker containerization
* AWS networking
* IAM
* ECR
* Security Groups
* Application deployment

The Flask application runs inside a Docker container on the EC2 instance.

---

## 4. Amazon ECR

Amazon ECR is used as the private Docker image registry.

ECR Repository:

```text
task-app-ecr
```

AWS Region:

```text
us-east-1
```

Repository URI:

```text
668453838840.dkr.ecr.us-east-1.amazonaws.com/task-app-ecr
```

The GitHub Actions workflow builds the Docker image and pushes it to this repository.

Images are tagged using:

```text
latest
```

and the Git commit SHA.

Using the commit SHA allows a particular application version to be identified.

---

## 5. GitHub Actions → ECR

The CI/CD flow is:

```text
Git Push
   |
   v
GitHub Actions
   |
   +--> Checkout Code
   |
   +--> Install Dependencies
   |
   +--> Run Tests
   |
   +--> Build Docker Image
   |
   v
AWS OIDC Authentication
   |
   v
Amazon ECR Login
   |
   v
Push Docker Image
```

The workflow runs automatically when code is pushed to the `main` branch or when a pull request targets `main`.

The pipeline is designed to fail if automated tests or the Docker image build fails.

---

## 6. IAM and GitHub OIDC

GitHub Actions uses **OpenID Connect (OIDC)** to authenticate with AWS.

The authentication flow is:

```text
GitHub Actions
      |
      | OIDC Token
      v
AWS STS
      |
      v
IAM Role
      |
      v
Amazon ECR
```

This approach avoids storing long-lived AWS access keys in GitHub.

The IAM trust policy restricts the role so that it can be assumed by the intended GitHub repository.

This provides a more secure authentication mechanism for CI/CD.

---

## 7. EC2 IAM Role

The EC2 instance uses an IAM instance role to access Amazon ECR.

The role provides the permissions required to pull container images.

The flow is:

```text
EC2
 |
 | IAM Instance Role
 v
Amazon ECR
 |
 | Pull Image
 v
Docker
```

Using an IAM role is preferable to storing AWS access keys directly on the EC2 server.

---

## 8. EC2 Configuration

The application is running on an Amazon Linux 2023 EC2 instance.

Docker is installed and running on the server.

The application container is named:

```text
devops-task-manager
```

The container exposes port `8000`.

The EC2 host publishes the application through port `80`.

```text
EC2 Host :80
      |
      v
Docker Container :8000
      |
      v
Gunicorn
      |
      v
Flask Application
```

---

## 9. Authenticate Docker with ECR

On the EC2 instance, Docker can authenticate to ECR using the AWS CLI:

```bash
aws ecr get-login-password --region us-east-1 | \
docker login \
--username AWS \
--password-stdin \
668453838840.dkr.ecr.us-east-1.amazonaws.com
```

After authentication, pull the image:

```bash
docker pull \
668453838840.dkr.ecr.us-east-1.amazonaws.com/task-app-ecr:latest
```

Verify the image:

```bash
docker images
```

---

## 10. Run the Application

The application can be started using:

```bash
docker run -d \
  --name devops-task-manager \
  -p 80:8000 \
  -e APP_NAME="DevOps Task Manager" \
  -e APP_ENV="production" \
  -e APP_VERSION="1.0.0" \
  -e APP_PORT="8000" \
  -e LOG_LEVEL="INFO" \
  668453838840.dkr.ecr.us-east-1.amazonaws.com/task-app-ecr:latest
```

The port mapping is:

```text
Host Port 80
     |
     v
Container Port 8000
     |
     v
Application
```

---

## 11. Verify the Deployment

Check whether the container is running:

```bash
docker ps
```

View application logs:

```bash
docker logs devops-task-manager
```

Follow logs:

```bash
docker logs -f devops-task-manager
```

Test the health endpoint locally on EC2:

```bash
curl http://localhost/health
```

The application should return a healthy response.

The application can then be accessed through:

```text
http://<EC2-PUBLIC-IP>
```

Health endpoint:

```text
http://<EC2-PUBLIC-IP>/health
```

---

## 12. VPC and Networking

The EC2 instance runs inside an AWS Virtual Private Cloud (VPC).

Simplified architecture:

```text
Internet
    |
    v
Internet Gateway
    |
    v
Route Table
    |
    v
Subnet
    |
    v
EC2
```

The VPC provides the network boundary for AWS resources.

The subnet determines where the EC2 instance is located within the VPC.

The route table determines how network traffic is routed.

The Internet Gateway provides a path between the VPC and the Internet when the appropriate routing and addressing configuration is present.

---

## 13. Security Groups

The EC2 instance uses an AWS Security Group as a virtual firewall.

The application requires:

```text
TCP 80 → HTTP
```

SSH administration uses:

```text
TCP 22 → SSH
```

Port `80` allows users to access the web application.

Port `22` allows administrators to connect to the server using SSH.

For better security, SSH should be restricted to a trusted administrator IP instead of:

```text
0.0.0.0/0
```

Only required ports should be publicly accessible.

---

## 14. Application Traffic Flow

The complete request flow is:

```text
User Browser
     |
     | HTTP :80
     v
EC2 Public IP
     |
     v
Security Group
     |
     v
EC2 Host :80
     |
     v
Docker Container :8000
     |
     v
Gunicorn
     |
     v
Flask Application
```

The application listens on port `8000` inside the container.

Docker maps EC2 port `80` to container port `8000`.

---

## 15. Public and Private IP

The EC2 instance has a private IP address inside the VPC.

A public IP allows users on the Internet to access the application when the required networking and Security Group rules are configured.

```text
Internet
    |
    v
Public IP
    |
    v
EC2
    |
    v
Private IP
```

The public IP of an EC2 instance can change after a stop/start unless an Elastic IP is used.

---

## 16. Logging and Monitoring

Application logs can be viewed directly using Docker:

```bash
docker logs devops-task-manager
```

For production environments, **Amazon CloudWatch** can be used for monitoring and logging.

CloudWatch can be used for:

* EC2 CPU utilization
* Network metrics
* Instance health
* Application logs
* Monitoring alarms

A production implementation could forward application logs to CloudWatch Logs and create alarms when resource usage or application health crosses defined thresholds.

---

## 17. Deployment Update Flow

When new code is pushed to GitHub:

```text
Developer
    |
    v
GitHub
    |
    v
GitHub Actions
    |
    +--> Run Tests
    |
    +--> Build Docker Image
    |
    v
Amazon ECR
    |
    v
EC2
    |
    +--> Pull New Image
    |
    +--> Stop Old Container
    |
    +--> Start New Container
    |
    v
Updated Application
```

Docker images are tagged with the Git commit SHA so that the source version associated with an image can be identified.

---

## 18. Security Practices

The deployment follows these security practices:

* GitHub Actions uses OIDC instead of long-lived AWS access keys.
* EC2 uses an IAM instance role.
* Amazon ECR is used as a private container registry.
* AWS credentials are not stored in source code.
* `.env` files are excluded from Git.
* Private keys must not be committed.
* Security Groups restrict network access.
* SSH should be restricted to trusted IP addresses.
* Only required ports should be exposed.

---

## 19. Future Production Improvements

The current EC2 + Docker architecture is suitable for demonstrating the required DevOps concepts.

For a production environment, it could be extended with:

* HTTPS/TLS
* Application Load Balancer
* Auto Scaling
* PostgreSQL or Amazon RDS
* AWS Secrets Manager
* CloudWatch dashboards and alarms
* Container vulnerability scanning
* Infrastructure as Code using Terraform or CloudFormation
* Private subnets
* Automated deployment and rollback

These improvements would provide better scalability, security, monitoring, and reliability.

````

Save it as:

```text
docs/aws-deployment.md
````

Then you'll have the **three final documentation files**:

```text
README.md
docs/linux-networking.md
docs/aws-deployment.md
```

After saving this one, we can do the **final GitHub/submission cleanup**.
