# Docker Troubleshooting Guide

This guide provides solutions for common issues when running the MLSecOps application in Docker.

## Common Issues and Solutions

### 1. Container fails to start or exits immediately

**Symptoms:** 
- Docker container exits immediately after starting
- Error in logs about a service failing to start

**Solutions:**
1. Check logs for specific error messages:
   ```bash
   docker-compose logs
   ```

2. Make sure all ports are available:
   ```bash
   # On Windows
   netstat -ano | findstr "5000 8000 8501"
   
   # On Linux/Mac
   netstat -tulpn | grep -E '5000|8000|8501'
   ```

3. Try stopping any conflicting applications or changing the port mappings in `docker-compose.yml`.

### 2. Services are unreachable

**Symptoms:**
- Container is running but services don't respond
- Cannot access endpoints from browser

**Solutions:**
1. Check container health:
   ```bash
   docker ps
   ```
   Look for "healthy" status.

2. Inspect logs to see if services started properly:
   ```bash
   docker-compose exec mlsecops-app cat /app/logs/mlflow.log
   docker-compose exec mlsecops-app cat /app/logs/streamlit.log
   ```

3. Try accessing services using curl from inside the container:
   ```bash
   docker-compose exec mlsecops-app curl -v http://localhost:5000
   docker-compose exec mlsecops-app curl -v http://localhost:8000/docs
   docker-compose exec mlsecops-app curl -v http://localhost:8501
   ```

### 3. Performance Issues

**Symptoms:**
- Container running slowly
- High CPU/memory usage

**Solutions:**
1. Check resource usage:
   ```bash
   docker stats
   ```

2. Increase container resource limits in `docker-compose.yml` if needed:
   ```yaml
   deploy:
     resources:
       limits:
         cpus: '4'  # Increase CPU limit
         memory: 8G  # Increase memory limit
   ```

### 4. Data Persistence Issues

**Symptoms:**
- MLflow models or experiment data missing after restart

**Solutions:**
1. Make sure the volume mount is correct in `docker-compose.yml`:
   ```yaml
   volumes:
     - ./mlruns:/app/mlruns
   ```

2. Check permissions on host directory:
   ```bash
   # Linux/Mac
   ls -la ./mlruns
   chmod -R 777 ./mlruns
   ```

## Advanced Debugging

For deeper debugging, you can get a shell inside the running container:

```bash
docker-compose exec mlsecops-app /bin/bash
```

This allows you to inspect logs, processes, and the filesystem directly within the container.
