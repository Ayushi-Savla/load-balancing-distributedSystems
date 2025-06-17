# Consistent Hashing Load Balancer

A Dockerized load balancer that distributes incoming HTTP requests to backend servers using Consistent Hashing. Built using Python, Flask, and Docker. Automatically manages replica spawning, removal, and request routing through a consistent hash ring.

---

## Features

- Consistent Hashing with 512 hash slots and 9 virtual nodes per server
- Dynamic Docker container management via Docker SDK
- Stateless load distribution based on request hash ID
- RESTful API for managing server replicas
- Fault-resilient routing via live container lookup

---

## Project Structure

```bash
.
├── docker-compose.yml         
├── Makefile                   
├── server/
│   ├── Dockerfile            
│   └── server.py            
└── loadbalancer/
    ├── Dockerfile           
    ├── loadbalancer.py       
    └── hash_map.py      
```

---
## Clone the repository: 
```bash
git clone https://github.com/yourusername/load_balancer_project.git
cd load_balancer_project
```

## Build the project:
```bash
docker compose build
docker compose up
```

## Access the load balancer:
```bash
http://localhost:5000
```
---
