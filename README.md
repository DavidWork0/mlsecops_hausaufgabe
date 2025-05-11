# mlsecops_haufaufgabe
mlsecops_haufaufgabe

## Viewing Airflow DAGs

There are several ways to view and interact with the Airflow DAGs:

1. **Using the Airflow Web UI**:
   - Start the Airflow server using `./start_airflow.sh`
   - Open your browser and navigate to `http://localhost:8080`
   - Login with username `admin` and password `admin`
   - You'll see all available DAGs in the main interface

2. **Command Line**:
   - List all DAGs: `airflow dags list`
   - Show DAG details: `airflow dags show ml_pipeline`
   - Test a specific task: `airflow tasks test ml_pipeline train_model 2023-01-01`

3. **Programmatically**:
   You can also view DAG structure directly in Python:
   ```python
   from src.airflow.dags.ml_pipeline_dag import dag
   print(dag.tasks)
   ```
