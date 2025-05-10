# Base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install git and curl for MLflow and the health check
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Make health check script executable
RUN chmod +x /app/health_check.sh

# Expose ports for all services
EXPOSE 5000 8000 8501

# Set environment variables
ENV PYTHONPATH=/app \
    MLFLOW_TRACKING_URI=http://localhost:5000 \
    MLFLOW_ARTIFACT_ROOT=file:///app/mlruns \
    PYTHONUNBUFFERED=1 \
    DOCKER_MODE=true \
    GIT_PYTHON_REFRESH=quiet

# Default command is defined in docker-compose.yml
