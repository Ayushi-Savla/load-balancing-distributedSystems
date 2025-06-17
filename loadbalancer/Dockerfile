FROM python:3.9-slim

WORKDIR /app

COPY loadbalancer.py .
COPY hash_map.py .

# Install Flask and Docker SDK (to spawn/remove containers)
RUN pip install flask docker

EXPOSE 5000

CMD ["python", "loadbalancer.py"]
