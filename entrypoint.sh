#!/bin/bash
set -e

# Initialize Airflow DB with the correct command
if [ "$1" = "init" ]; then
    # Use migrate instead of init for Airflow 3.0.0
    airflow db migrate
    exit 0
fi

# Execute the original entrypoint script
exec "$@"