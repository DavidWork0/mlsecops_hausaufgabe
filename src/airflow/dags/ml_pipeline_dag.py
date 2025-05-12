"""
Airflow DAG for the ML pipeline workflow.
This DAG orchestrates the model training, evaluation, and deployment process.
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
import os
import sys
import subprocess
import requests
import time

# Add the project root to the path so we can import modules
sys.path.append('/app')

# Import project-specific modules
import mlflow
from src.api import train_and_register_model
from src.neptuneai_monitoring import run_monitoring

default_args = {
    'owner': 'mlsecops',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def notify_dashboard(status, task):
    """Notify the dashboard about the current DAG/task status."""
    try:
        payload = {"task": task, "status": status}
        # Use the dashboard's service name or host.docker.internal if on the same network
        requests.post("http://host.docker.internal:8000/dag_status", json=payload, timeout=2)
    except Exception as e:
        print(f"Failed to notify dashboard: {e}")

def train_model():
    """Train the ML model and register it with MLflow"""
    print("Starting model training and registration")
    notify_dashboard("running", "train_model")
    train_and_register_model()
    notify_dashboard("success", "train_model")
    return "Model training completed"

def run_model_monitoring():
    """Run the Neptune AI model monitoring"""
    print("Starting model monitoring with Neptune AI")
    notify_dashboard("running", "run_monitoring")
    run_monitoring()
    notify_dashboard("success", "run_monitoring")
    return "Monitoring completed"

def test_api_endpoint():
    """Test the FastAPI endpoint to ensure it's working"""
    print("Testing API endpoint")
    notify_dashboard("running", "test_api")
    max_retries = 5
    retry_delay = 5
    
    for attempt in range(max_retries):
        try:
            # Test data for Iris dataset
            test_data = {
                "sepal_length": 5.1,
                "sepal_width": 3.5,
                "petal_length": 1.4,
                "petal_width": 0.2
            }
            
            # Changed from "http://localhost:8000/predict" to "http://host.docker.internal:8000/predict"
            response = requests.post("http://host.docker.internal:8000/predict", json=test_data)
            response.raise_for_status()  # Raise an error for bad responses
            
            print(f"API test successful: {response.json()}")
            notify_dashboard("success", "test_api")
            return f"API test succeeded with response: {response.json()}"
        except Exception as e:
            print(f"API test attempt {attempt+1}/{max_retries} failed: {e}")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                notify_dashboard("failed", "test_api")
                raise Exception(f"API test failed after {max_retries} attempts")

# Create the DAG
with DAG(
    'ml_pipeline',
    default_args=default_args,
    description='ML Pipeline for training, monitoring, and deploying models',
    schedule=timedelta(days=1),
    catchup=False,
    tags=['ml', 'pipeline', 'mlsecops'],
) as dag:

    train_task = PythonOperator(
        task_id='train_model',
        python_callable=train_model,
    )
    
    monitor_task = PythonOperator(
        task_id='run_monitoring',
        python_callable=run_model_monitoring,
    )
    
    test_api_task = PythonOperator(
        task_id='test_api',
        python_callable=test_api_endpoint,
    )
    
    # Define task dependencies
    train_task >> monitor_task >> test_api_task
