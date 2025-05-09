# Docker Best Practices for MLSecOps Projects

This document outlines best practices for Docker containerization in machine learning and MLOps/MLSecOps projects.

## Image Building

### 1. Use Specific Base Images
- Always specify exact version tags (e.g., `python:3.12.8-slim-bullseye` instead of `python:latest`)
- Prefer slim or distroless images when possible to reduce attack surface

### 2. Multi-stage Builds
- Use multi-stage builds to separate build dependencies from runtime dependencies
- Example:
  ```dockerfile
  # Build stage
  FROM python:3.12.8-slim-bullseye AS builder
  WORKDIR /build
  COPY requirements.txt .
  RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

  # Runtime stage
  FROM python:3.12.8-slim-bullseye
  COPY --from=builder /wheels /wheels
  RUN pip install --no-cache-dir --no-index --find-links=/wheels /wheels/* && rm -rf /wheels
  ```

### 3. Layer Optimization
- Order Dockerfile instructions from least to most frequently changing
- Group RUN commands with `&&` to reduce layers
- Use .dockerignore to exclude unnecessary files

## Security

### 1. Non-root User
- Avoid running containers as root
- Add a dedicated user:
  ```dockerfile
  RUN useradd -m appuser
  USER appuser
  ```

### 2. Secret Management
- Never hardcode secrets in Dockerfile or image
- Use environment variables, Docker secrets, or external vaults
- Avoid exposing API keys in environment variables (use volumes for credential files)

### 3. Dependency Scanning
- Regularly scan images for vulnerabilities using tools like Docker Scout, Trivy, or Snyk
- Keep base images updated

## ML-specific Best Practices

### 1. Model Artifact Management
- Use volumes to persist model artifacts
- Consider pre-loading common models in the image for faster startup

### 2. GPU Support
- Use NVIDIA Container Toolkit for GPU-accelerated containers
- Specify the CUDA version your application needs

### 3. Monitoring
- Export metrics to external monitoring systems
- Include health checks that verify ML services are operational

## Deployment

### 1. Resource Constraints
- Always define memory and CPU limits
- Consider using resource quotas for large-scale deployments

### 2. Container Orchestration
- Use Docker Compose for development
- Consider Kubernetes for production deployments
- Use StatefulSets for stateful ML applications

### 3. CI/CD Integration
- Automate image building, testing, and deployment
- Implement comprehensive testing of containerized applications

## Performance Optimization

### 1. Use Docker Buildkit
- Enable BuildKit for faster builds:
  ```bash
  DOCKER_BUILDKIT=1 docker build -t myimage .
  ```

### 2. Use docker-compose Up with Dependencies
- Use `depends_on` to ensure services start in the correct order

### 3. Data Volume Management
- Use volumes for data that needs to persist
- Use tmpfs for temporary data that doesn't need to persist

## Examples

### Example Dockerfile for ML Application
```dockerfile
FROM python:3.12.8-slim-bullseye

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m appuser

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY --chown=appuser:appuser . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV MODEL_DIR=/models

# Create and set permissions for model directory
RUN mkdir -p /models && chown -R appuser:appuser /models

# Switch to non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["python", "app.py"]
```

### Example docker-compose.yml
```yaml
services:
  ml-api:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    volumes:
      - ./models:/models
      - ./logs:/app/logs
    environment:
      - MODEL_VERSION=v1
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
```

---

Remember: The most effective Docker setup is one that balances security, performance, and ease of use for your specific ML workflow requirements.
