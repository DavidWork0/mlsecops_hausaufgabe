#!/bin/bash

# Check if MLflow UI is running
if ! curl -s http://localhost:5000 > /dev/null; then
  echo "MLflow UI is not responding"
  exit 1
fi

# Check if REST API is running
if ! curl -s http://localhost:8000/docs > /dev/null; then
  echo "REST API is not responding"
  exit 1
fi

# Check if Streamlit is running
if ! curl -s http://localhost:8501 > /dev/null; then
  echo "Streamlit is not responding"
  exit 1
fi

# Check if Airflow UI is running
if ! curl -s http://localhost:8080 > /dev/null; then
  echo "Airflow UI is not responding"
  exit 1
fi

echo "All services are running"
exit 0
