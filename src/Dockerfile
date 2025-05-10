# Base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install git, curl, and additional dependencies for Airflow
RUN apt-get update && apt-get install -y \
    git \
    curl \
    gcc \
    g++ \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
# Install Apache Airflow 3.0.0 explicitly to match the version mentioned in the error
RUN pip install --no-cache-dir apache-airflow==3.0.0 && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create Airflow directories
RUN mkdir -p /app/airflow/dags /app/airflow/logs /app/airflow/plugins

# Make health check script executable
RUN chmod +x /app/health_check.sh

# Create a health check script if it doesn't exist
RUN if [ ! -f /app/health_check.sh ]; then \
    echo '#!/bin/bash' > /app/health_check.sh && \
    echo 'curl -f http://localhost:8080/health || exit 1' >> /app/health_check.sh && \
    chmod +x /app/health_check.sh; \
    fi

# Expose ports for all services
EXPOSE 5000 8000 8501 8080

# Set environment variables
ENV PYTHONPATH=/app \
    MLFLOW_TRACKING_URI=http://localhost:5000 \
    MLFLOW_ARTIFACT_ROOT=file:///app/mlruns \
    PYTHONUNBUFFERED=1 \
    DOCKER_MODE=true \
    GIT_PYTHON_REFRESH=quiet \
    AIRFLOW_HOME=/app/airflow \
    AIRFLOW__WEBSERVER__WEB_SERVER_HOST=0.0.0.0
