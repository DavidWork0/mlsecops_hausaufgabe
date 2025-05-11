#!/bin/bash
set -e

echo "Running configuration update script..."
python /app/scripts/update_airflow_config.py

echo "Starting Airflow..."
exec airflow standalone
