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
├── client
    ├── client.html
    ├── demo_distribution.py                   
├── server/
│   ├── Dockerfile            
│   └── server.py            
└── loadbalancer/
    ├── Dockerfile           
    ├── balancer.py       
    └── consistent_hash.py      
```

---
## Clone the repository: 
```bash
git clone https://github.com/yourusername/load_balancer_project.git
cd load_balancer_project
```

## Build the project:
```bash
docker-compose up --build -d
```

## Access the load balancer and Sample Website:
```bash
curl http://localhost:5000/home 

python -m http.server 8000
http://localhost:8000/client.html
```

## Test the Distribution Script
```bash
cd client
python3 test_distribution.py
```
---
