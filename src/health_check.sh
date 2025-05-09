#!/bin/bash
# Health check script for Docker container
# This script checks if all required services are running

# Check if FastAPI is running
if curl --silent --fail http://localhost:8000/docs > /dev/null; then
    echo "FastAPI is running"
else
    echo "FastAPI is not running"
    exit 1
fi

# Check if MLflow is running
if curl --silent --fail http://localhost:5000 > /dev/null; then
    echo "MLflow is running"
else
    echo "MLflow is not running"
    exit 1
fi

# Check if Streamlit is running
if curl --silent --fail http://localhost:8501 > /dev/null; then
    echo "Streamlit is running"
else
    echo "Streamlit is not running"
    exit 1
fi

echo "All services are running"
exit 0
