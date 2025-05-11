#!/bin/bash

# Initialize the database if it doesn't exist
airflow db init

# Create a user for the web UI (if it doesn't exist)
airflow users create \
    --username admin \
    --password admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com

# Start the API server in the background
airflow api-server --port 8080 &

# Start the scheduler
airflow scheduler
```
