"""
REST API a gépi tanulási modell predikciójához FastAPI-val.
A modell az MLflow model registry-ből töltődik be.
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import mlflow.pyfunc
import numpy as np
from mlflow.exceptions import MlflowException
import mlflow.tracking
import os
import sys

# Configure MLflow properly for Docker
os.environ["MLFLOW_TRACKING_URI"] = "http://localhost:5000"
os.environ["MLFLOW_ARTIFACT_ROOT"] = "file:///app/mlruns"

# Set a local artifact location to avoid permission errors
if os.environ.get("DOCKER_MODE") == "true":
    # Make sure mlruns directory exists and is writable
    os.makedirs("/app/mlruns", exist_ok=True)
    # Fix permissions just to be sure
    if os.path.exists("/app/mlruns"):
        os.system("chmod -R 777 /app/mlruns")

# FastAPI példány létrehozása
app = FastAPI(title="Iris ML Model API", description="REST API MLflow modellel", version="1.0")

# Bemeneti adatok sémája
class IrisInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

# Modell neve és stage-je
MODEL_NAME = "IrisDecisionTree"
MODEL_STAGE = "Production"  # vagy "Staging"

@app.post("/predict")
def predict(input: IrisInput):
    """
    Predikció végpont. Bemenet: IrisInput, Kimenet: predikált osztály.
    """
    try:
        print(f"MLflow tracking URI: {mlflow.get_tracking_uri()}")
        # First, check for local model availability as a fallback
        local_model_path = "/tmp/iris_model.pkl"
        
        if os.path.exists(local_model_path):
            print(f"Loading model from local path: {local_model_path}")
            import joblib
            model = joblib.load(local_model_path)
        else:
            # Try to load from MLflow registry
            try:
                print(f"Attempting to load model from MLflow registry: models:/{MODEL_NAME}/{MODEL_STAGE}")
                model = mlflow.pyfunc.load_model(f"models:/{MODEL_NAME}/{MODEL_STAGE}")
                print(f"Successfully loaded model from MLflow registry")
            except MlflowException as e:
                print(f"MLflow model registry error: {e}")
                # If that fails, try to get the latest version
                try:
                    client = mlflow.tracking.MlflowClient()
                    versions = [int(mv.version) for mv in client.search_model_versions(f"name='{MODEL_NAME}'")]
                    if not versions:
                        return JSONResponse(status_code=500, content={"error": f"No versions found for model {MODEL_NAME}"})
                    
                    latest_version = max(versions)
                    print(f"Production model not found, using latest version: {latest_version}")
                    model = mlflow.pyfunc.load_model(f"models:/{MODEL_NAME}/{latest_version}")
                except Exception as inner_e:
                    print(f"Error loading from registry: {inner_e}")
                    import traceback
                    traceback.print_exc()
                    return JSONResponse(status_code=500, content={"error": f"Failed to load model: {inner_e}"})
    except Exception as e:
        print(f"Unexpected error in prediction endpoint: {e}")
        import traceback
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": f"Unexpected error: {e}"})
    
    data = np.array([[input.sepal_length, input.sepal_width, input.petal_length, input.petal_width]])
    prediction = model.predict(data)
    return {"prediction": int(prediction[0])}

if __name__ == "__main__":
    """
    Ha futtatod: python api.py
    - Betanítja a modellt
    - Logolja MLflow-ba
    - Regisztrálja a model registry-be 'IrisDecisionTree' néven
    """
    import pandas as pd
    from sklearn.datasets import load_iris
    from sklearn.model_selection import train_test_split
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.metrics import accuracy_score
    import mlflow
    import mlflow.sklearn
    from mlflow.exceptions import MlflowException

    # Adatok betöltése
    iris = load_iris()
    X = pd.DataFrame(iris.data, columns=iris.feature_names)
    y = pd.Series(iris.target, name='target')
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)    # Modell tanítása
    clf = DecisionTreeClassifier(random_state=42)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    
    # MLflow logolás - bizonyosodjunk meg róla, hogy a helyes könyvtárat használjuk
    try:
        # Explicitly set the artifact location to avoid Windows path issues
        mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI", "http://localhost:5000"))
        artifact_location = os.environ.get("MLFLOW_ARTIFACT_ROOT", "file:///app/mlruns")
        
        print(f"Using MLflow tracking URI: {mlflow.get_tracking_uri()}")
        print(f"Using artifact location: {artifact_location}")
        
        with mlflow.start_run() as run:            # Save model to local disk first for direct access
            import joblib
            local_model_path = "/tmp/iris_model.pkl"
            print(f"Saving model to local path: {local_model_path}")
            joblib.dump(clf, local_model_path)
            
            # Log metrics and params first
            mlflow.log_metric("accuracy", acc)
            mlflow.log_param("model_type", "DecisionTreeClassifier")
            
            # Make sure the artifact path is correctly configured
            os.environ["MLFLOW_TRACKING_DIR"] = "/app/mlruns"
            
            # Log model file as artifact
            print("Logging model to MLflow")
            mlflow.sklearn.log_model(
                sk_model=clf,
                artifact_path="model",
                registered_model_name=MODEL_NAME  # Directly register the model
            )
            
            model_uri = f"runs:/{run.info.run_id}/model"
            print(f"Model logolva: {model_uri}")
            
            # Modell regisztrálása a registry-be
            try:
                result = mlflow.register_model(model_uri, MODEL_NAME)
                print(f"Model regisztrálva: {MODEL_NAME}")
                
                # Automatikusan állítsuk be a Production stage-et a legújabb verzióra
                client = mlflow.tracking.MlflowClient()
                client.transition_model_version_stage(
                    name=MODEL_NAME,
                    version=result.version,
                    stage="Production"
                )
                print(f"Modell verzió {result.version} beállítva mint Production")
            except Exception as reg_error:
                print(f"Modell regisztráció hiba: {reg_error}")
    except Exception as e:
        print(f"MLflow hiba: {e}")
        print(f"Error during MLflow operations: {e}")
        # Log the exact traceback for better debugging
        import traceback
        traceback.print_exc()

    print("Tanítás, logolás, regisztráció kész.")
