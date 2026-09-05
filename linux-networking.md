
# Linux and Networking Documentation

This document explains the Linux and networking concepts used to run, troubleshoot, and expose the DevOps Task Manager application.

---

## 1. CPU, Memory and Disk

### CPU

To monitor CPU usage and running processes:

```bash
top
````

If available:

```bash
htop
```

These commands help identify high CPU utilization, system load, and resource-heavy processes.

### Memory

```bash
free -h
```

This displays total, used, free, and available memory.

### Disk

```bash
df -h
```

This displays disk usage for mounted filesystems.

To check the size of a directory:

```bash
du -sh <directory>
```

These commands are useful when troubleshooting performance and resource problems on a server.

---

## 2. Processes

To list running processes:

```bash
ps aux
```

To find a specific process:

```bash
pgrep -af gunicorn
```

To terminate a process:

```bash
kill <PID>
```

Processes are important when troubleshooting whether an application or service is actually running.

For this project, Gunicorn is used as the application server.

---

## 3. Ports and Listening Services

To view listening TCP ports:

```bash
ss -lntp
```

To check port `8000` specifically:

```bash
ss -lntp | grep 8000
```

Important options:

```text
-l  Listening sockets
-n  Numeric output
-t  TCP sockets
-p  Process information
```

The Task Manager application listens on port `8000`.

---

## 4. Network Interfaces

To display network interfaces and their IP addresses:

```bash
ip addr
```

This shows:

* Network interface names
* IP addresses
* Interface state
* MAC addresses

The loopback interface is normally:

```text
lo
```

The loopback interface is used for communication within the same machine.

---

## 5. Routing

To view the routing table:

```bash
ip route
```

A typical server contains a default route similar to:

```text
default via <gateway> dev <interface>
```

The default route is used when there is no more specific route for the destination.

Routing is important because it determines how packets leave the server and reach other networks.

---

## 6. Logs

Logs are one of the most important tools for troubleshooting.

### Docker Logs

View container logs:

```bash
docker logs devops-task-manager
```

Follow logs in real time:

```bash
docker logs -f devops-task-manager
```

### Kubernetes Logs

```bash
kubectl logs <pod-name>
```

### Linux Service Logs

```bash
journalctl -u <service-name>
```

For Docker:

```bash
journalctl -u docker
```

Logs can help identify:

* Application startup failures
* Configuration errors
* Crashes
* Network problems
* Container failures

---

## 7. 127.0.0.1 vs 0.0.0.0

### 127.0.0.1

`127.0.0.1` is the IPv4 loopback address.

If an application listens on:

```text
127.0.0.1:8000
```

it normally accepts connections only through the local machine or container.

### 0.0.0.0

`0.0.0.0` means that the application listens on all IPv4 network interfaces.

The Task Manager application uses:

```text
0.0.0.0:8000
```

This is important when running the application inside Docker or Kubernetes because external networking components need to reach the application.

---

## 8. Public IP vs Private IP

A private IP address is normally used inside a private network such as an AWS VPC.

Common private IPv4 ranges include:

```text
10.0.0.0/8
172.16.0.0/12
192.168.0.0/16
```

A public IP can be used to access an EC2 instance from the Internet when the required routing and security rules are configured.

Simplified flow:

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

The public IP provides external access while the private IP is used for communication inside the VPC.

---

## 9. Host Port vs Container Port

Docker containers have their own networking environment.

For example:

```bash
docker run -p 80:8000 image-name
```

means:

```text
Host Port 80
     |
     v
Container Port 8000
     |
     v
Application
```

The first port is the host port and the second port is the container port.

For this project:

```text
Local Docker:
Host 8000 → Container 8000

AWS EC2:
Host 80 → Container 8000
```

The application itself continues to listen on port `8000`.

---

## 10. TCP and HTTP

TCP is a transport-layer protocol that provides reliable and ordered communication.

HTTP is an application-layer protocol commonly transported over TCP.

A simplified request flow is:

```text
Browser
   |
   | HTTP Request
   v
TCP Connection
   |
   v
Server
   |
   | HTTP Response
   v
Browser
```

For example, when the browser requests:

```text
GET /health
```

the request is sent to the application over the network.

---

## 11. Docker Networking

The Flask application runs inside a Docker container and listens on port `8000`.

Docker publishes the container port to the host.

```text
Host
 |
 | Port Mapping
 v
Container
 |
 v
Gunicorn
 |
 v
Flask Application :8000
```

The port mapping allows clients outside the container to communicate with the application.

---

## 12. Kubernetes Networking

The Kubernetes Deployment runs two replicas of the application.

A Kubernetes Service provides a stable network endpoint and routes traffic to available pods.

```text
             Service
             /     \
            /       \
         Pod 1     Pod 2
         :8000     :8000
```

The Service selects pods using labels.

This allows traffic to be distributed between the two application replicas.

---

## 13. Kubernetes Readiness Probe

The application provides a health endpoint:

```text
GET /health
```

The Kubernetes readiness probe calls this endpoint to determine whether a pod is ready to receive traffic.

If the readiness check fails, Kubernetes can temporarily remove the pod from the Service endpoints.

This prevents traffic from being sent to an application that is not ready.

---

## 14. Kubernetes Liveness Probe

The liveness probe also checks:

```text
GET /health
```

Its purpose is to determine whether the application is still functioning.

If the liveness probe repeatedly fails, Kubernetes can restart the container.

The difference is:

```text
Readiness → Can this pod receive traffic?

Liveness  → Is this application still running correctly?
```

---

## 15. AWS Security Groups

An AWS Security Group acts as a virtual firewall for resources such as EC2.

For this application, the main ports are:

```text
TCP 80 → HTTP application
TCP 22 → SSH administration
```

Port `80` allows users to access the web application.

Port `22` is used for SSH administration.

SSH should preferably be restricted to a trusted administrator IP rather than allowing:

```text
0.0.0.0/0
```

Only the required ports should be exposed publicly.

---

## 16. AWS Network Flow

The AWS deployment follows this network path:

```text
Internet
    |
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

The Security Group controls whether the incoming connection is allowed.

Docker then forwards host port `80` to container port `8000`.

---

## 17. VPC Networking

The EC2 instance runs inside an AWS VPC.

A simplified architecture is:

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

The VPC provides the network boundary.

The route table determines where network traffic is sent.

The Internet Gateway provides a path between the VPC and the Internet when the appropriate route and addressing configuration exists.

---

## 18. Basic Troubleshooting

If the application is unavailable, the following checks can be performed.

### Check the application process

```bash
ps aux | grep gunicorn
```

### Check listening ports

```bash
ss -lntp
```

### Check Docker containers

```bash
docker ps
```

### Check Docker logs

```bash
docker logs devops-task-manager
```

### Check Kubernetes pods

```bash
kubectl get pods
```

### Check Kubernetes deployment

```bash
kubectl get deployment
```

### Check Kubernetes service

```bash
kubectl get service
```

### Check Kubernetes logs

```bash
kubectl logs <pod-name>
```

### Check network interfaces

```bash
ip addr
```

### Check routing

```bash
ip route
```

### Test the health endpoint

```bash
curl http://localhost:8000/health
```

These checks help determine whether a problem is related to the application, process, container, port, networking, routing, or firewall configuration.

---

## 19. Summary

The main networking flow used by this project is:

```text
User
 |
 | HTTP
 v
Public IP / Host Port
 |
 v
Security Group
 |
 v
Docker / Kubernetes
 |
 v
Container / Pod
 |
 v
Application :8000
```

Understanding processes, ports, IP addresses, routing, Docker port mapping, Kubernetes Services, health probes, and AWS Security Groups is essential for deploying and troubleshooting the application.

````

Save this as exactly:

```text
docs/linux-networking.md
````

So your **three documentation files** are:

```text
README.md
docs/linux-networking.md
docs/aws-deployment.md
```
