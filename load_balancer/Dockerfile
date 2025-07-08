FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install flask requests flask_cors pandas
EXPOSE 5000
CMD ["python", "balancer.py"]

