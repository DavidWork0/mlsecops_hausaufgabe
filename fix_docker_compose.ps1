# This script fixes the docker-compose.yml file
$content = @'
services:
  mlsecops-app:
    build:
      context: .
      dockerfile: src/Dockerfile
    ports:
      - "5000:5000"  # MLflow UI
      - "8000:8000"  # FastAPI
      - "8501:8501"  # Streamlit
    volumes:
      - ./mlruns:/app/mlruns  # Persist MLflow data
      - ./src:/app/src  # For hot-reloading during development
    environment:
      - PYTHONPATH=/app
      - MLFLOW_TRACKING_URI=http://localhost:5000
      - PYTHONUNBUFFERED=1
      - DOCKER_MODE=true
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "/app/health_check.sh"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    networks:
      - mlsecops-network
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G

networks:
  mlsecops-network:
    driver: bridge
'@

Set-Content -Path 'docker-compose.yml' -Value $content -Encoding UTF8
Write-Host "docker-compose.yml has been fixed!"
