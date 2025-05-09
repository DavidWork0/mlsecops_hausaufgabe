# Base image with specific Python version
FROM python:3.12.8-slim-bullseye

# Install system packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    procps \
    wget \
    gnupg2 \
    lsb-release \
    cmake \
    pkg-config \
    libssl-dev \
    libffi-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r mluser && useradd -r -g mluser -s /bin/bash -m mluser

# Set working directory
WORKDIR /app

# Copy health check script
COPY src/health_check.sh /app/health_check.sh
RUN chmod +x /app/health_check.sh

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies with special handling for problematic packages
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir numpy pandas matplotlib seaborn && \
    pip install --no-cache-dir scikit-learn fastapi uvicorn[standard] pydantic streamlit && \
    pip install --no-cache-dir mlflow requests && \
    pip install --no-cache-dir neptune && \
    pip install --no-cache-dir -r requirements.txt --ignore-installed

# Set environment variables
ENV PYTHONPATH=/app
ENV MLFLOW_TRACKING_URI=http://localhost:5000
ENV PYTHONUNBUFFERED=1

# Expose necessary ports
EXPOSE 5000 8000 8501

# Copy project code
COPY . /app/

# Create directory for logs and set permissions
RUN mkdir -p /app/logs /app/mlruns && \
    chmod 777 -R /app/logs /app/mlruns && \
    chown -R mluser:mluser /app

# Create start script with proper error handling and logging
RUN echo '#!/bin/bash\n\
\n\
# Setup logging function\n\
log() {\n\
    echo "[$(date +"%Y-%m-%d %H:%M:%S")] $1"\n\
}\n\
\n\
# Setup PYTHONPATH\n\
export PYTHONPATH=$PYTHONPATH:/app\n\
log "Environment setup complete"\n\
\n\
# Create logs directory\n\
mkdir -p /app/logs /app/mlruns\n\
\n\
# Start MLflow UI server\n\
log "Starting MLflow UI server..."\n\
mlflow ui --host 0.0.0.0 --port 5000 > /app/logs/mlflow.log 2>&1 &\n\
MLFLOW_PID=$!\n\
sleep 8\n\
\n\
# Start Streamlit dashboard\n\
log "Starting Streamlit dashboard..."\n\
streamlit run /app/src/streamlit_app.py --server.headless=true --server.port=8501 --server.address=0.0.0.0 > /app/logs/streamlit.log 2>&1 &\n\
STREAMLIT_PID=$!\n\
sleep 8\n\
\n\
# Initialize MLflow environment\n\
log "Initializing MLflow environment..."\n\
python /app/src/fix_mlflow.py > /app/logs/mlflow_init.log 2>&1 || log "Warning: MLflow initialization error, but continuing..."\n\
\n\
# Try to run model training but don'\''t exit if it fails\n\
log "Training and registering ML model..."\n\
python /app/src/api.py > /app/logs/model_training.log 2>&1 || log "Warning: Model training encountered an error, but continuing..."\n\
\n\
# Try to run Neptune monitoring but don'\''t exit if it fails\n\
log "Running Neptune.ai monitoring..."\n\
python /app/src/neptuneai_monitoring.py > /app/logs/neptune_monitoring.log 2>&1 || log "Warning: Neptune monitoring encountered an error, but continuing..."\n\
\n\
# Log service URLs\n\
log "All services are started. The application is available at:"\n\
log " - MLflow UI: http://localhost:5000"\n\
log " - FastAPI: http://localhost:8000/docs"\n\
log " - Streamlit Dashboard: http://localhost:8501"\n\
\n\
# Trap to handle container shutdown gracefully\n\
trap "log \"Shutting down services...\"; kill $MLFLOW_PID $STREAMLIT_PID; log \"Services stopped\"" SIGTERM SIGINT\n\
\n\
# Start FastAPI as the main process (this keeps the container running)\n\
log "Starting FastAPI server..."\n\
exec uvicorn src.api:app --host 0.0.0.0 --port 8000 --log-level info\n'\
> /app/start.sh && chmod +x /app/start.sh

# Switch to non-root user
USER mluser

# Set the entrypoint
CMD ["/app/start.sh"]
