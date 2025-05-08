"""
Airflow DAG az Iris ML pipeline automatizálásához.
Lépések: modell tanítás, MLflow log, Neptune.ai monitoring.
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import subprocess

def train_and_log_model():
    # Jupyter notebook vagy script futtatása a modell tanításához és MLflow logoláshoz
    subprocess.run(['python', 'api.py'], check=True)

def run_neptune_monitoring():
    # Neptune.ai monitoring script futtatása
    subprocess.run(['python', 'neptuneai_monitoring.py'], check=True)

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 1
}

dag = DAG(
    'iris_ml_pipeline',
    default_args=default_args,
    description='Iris ML pipeline: train, log, monitor',
    schedule_interval=None,
    catchup=False
)

train_log_task = PythonOperator(
    task_id='train_and_log_model',
    python_callable=train_and_log_model,
    dag=dag
)

monitoring_task = PythonOperator(
    task_id='run_neptune_monitoring',
    python_callable=run_neptune_monitoring,
    dag=dag
)

train_log_task >> monitoring_task
