#!/bin/bash
set -e

echo "Indítás: MLflow UI..."

# Initialize the Airflow database
airflow db migrate

# Create admin user - In Airflow 3.0.0, user commands are handled differently
# Instead of: airflow users create ...
airflow variables set create_admin_user true

# Run a custom Python script to create users
python3 /app/create_admin_user.py

# Other initialization commands
# Add your additional initialization commands here