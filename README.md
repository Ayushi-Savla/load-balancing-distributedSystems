# Consistent Hashing Load Balancer


## Overview

This project implements a customizable load balancer using **consistent hashing** to evenly distribute client requests across multiple backend servers. 

The system consists of:
- A **Load Balancer** that receives client requests and distributes them.
- Multiple **replicated backend servers**.
- A **consistent hashing algorithm** to ensure even and fault-tolerant load distribution.
- Support for **dynamic scaling** by adding/removing server replicas.

The project demonstrates core distributed systems concepts like fault tolerance, scalability, container orchestration, and hashing-based load balancing.



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
python3 demo_distribution.py
```
---
## Dependencies

Ensure the following are installed:

- Docker (version 20.10.23+)
- Docker Compose
- Python 3.8+
- `requests` and `matplotlib` libraries for testing and plotting

Install Python dependencies (for testing scripts):

```bash
pip install -r requirements.txt

```
---
## Screenshots
![image](https://github.com/user-attachments/assets/c47d7724-75e3-47ca-980f-975acf41fbbd)
![image](https://github.com/user-attachments/assets/e2b7672f-2fd9-45f0-8723-1e7a24e668ab)
![image](https://github.com/user-attachments/assets/86175407-0086-4143-a889-8d41f07ae44c)



