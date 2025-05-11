FROM apache/airflow:3.0.0

USER root

# Create directories
RUN mkdir -p /app/scripts

# Copy scripts
COPY scripts/ /app/scripts/
RUN chmod +x /app/scripts/*.py || true

USER airflow

# Run configuration update before starting Airflow
ENTRYPOINT ["bash", "-c", "python /app/scripts/update_airflow_config.py && exec airflow standalone"]