"""
MLflow tracking URI fix script
This script properly configures MLflow to use the local filesystem for artifact storage
"""

import os
import sys
import mlflow
import shutil
import subprocess
from pathlib import Path

def fix_mlflow_paths():
    """Configure MLflow to store artifacts in the local filesystem instead of trying to use absolute Windows paths"""
    
    # Set the tracking URI to the local MLflow server
    os.environ["MLFLOW_TRACKING_URI"] = "http://localhost:5000"
    
    # Set artifact path explicitly to a directory in the container
    os.environ["MLFLOW_ARTIFACT_ROOT"] = "file:///app/mlruns"
    os.environ["MLFLOW_TRACKING_DIR"] = "/app/mlruns"
    
    # Disable the Windows path conversion which can cause problems
    os.environ["MLFLOW_DISABLE_USAGE_LOGGING"] = "1"
    
    # Set the tracking URI
    mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI"))
    
    # Create the mlruns directory if it doesn't exist and ensure permissions
    os.makedirs("/app/mlruns", exist_ok=True)
    
    # Fix permissions with subprocess to ensure it works correctly
    try:
        subprocess.run(["chmod", "-R", "777", "/app/mlruns"], check=True)
        print("Successfully set permissions on /app/mlruns")
    except subprocess.CalledProcessError as e:
        print(f"Failed to set permissions: {e}")
    
    # Try to create a test run to ensure everything is working
    try:
        with mlflow.start_run(run_name="test_connectivity") as run:
            # Save artifact locally first to avoid Windows path issues
            with open("/tmp/test.txt", "w") as f:
                f.write("This is a test artifact")
            
            # Log a parameter
            mlflow.log_param("test", "success")
            
            # Log the artifact from the tmp location
            mlflow.log_artifact("/tmp/test.txt")
            
            print(f"MLflow test run created successfully: {run.info.run_id}")
            print(f"MLflow artifact URI: {mlflow.get_artifact_uri()}")
            print("MLflow configuration complete!")
    except Exception as e:
        print(f"MLflow test run failed: {e}")
        print("Will try to continue anyway")

if __name__ == "__main__":
    fix_mlflow_paths()
