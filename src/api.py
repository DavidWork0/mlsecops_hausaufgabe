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
        # Először próbáljuk betölteni a Production stage-ből
        model = mlflow.pyfunc.load_model(f"models:/{MODEL_NAME}/{MODEL_STAGE}")
    except MlflowException as e:
        # Ha nem sikerül, akkor próbáljuk betölteni a legújabb verziót
        try:
            client = mlflow.tracking.MlflowClient()
            latest_version = max([int(mv.version) for mv in client.search_model_versions(f"name='{MODEL_NAME}'")])
            print(f"Production modell nem található, használom a legfrissebb verziót: {latest_version}")
            model = mlflow.pyfunc.load_model(f"models:/{MODEL_NAME}/{latest_version}")
        except Exception as e:
            return JSONResponse(status_code=500, content={"error": f"Nem sikerült betölteni a modellt: {e}"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Ismeretlen hiba: {e}"})
    
    data = np.array([[input.sepal_length, input.sepal_width, input.petal_length, input.petal_width]])
    prediction = model.predict(data)
    return {"prediction": int(prediction[0])}

def train_and_register_model():
    """
    Function to train and register the model.
    This is extracted from the __main__ block to be reusable by Airflow.
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
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Modell tanítása
    clf = DecisionTreeClassifier(random_state=42)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)

    # MLflow logolás
    with mlflow.start_run() as run:
        mlflow.sklearn.log_model(clf, "model")
        mlflow.log_metric("accuracy", acc)
        mlflow.log_param("model_type", "DecisionTreeClassifier")
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
            print(f"Model automatikusan beállítva Production stage-re: verzió {result.version}")
        except MlflowException as e:
            print(f"Model regisztrációs hiba vagy már létezik: {e}")
    
    print("Tanítás, logolás, regisztráció kész.")
    return acc

if __name__ == "__main__":
    """
    Ha futtatod: python api.py
    - Betanítja a modellt
    - Logolja MLflow-ba
    - Regisztrálja a model registry-be 'IrisDecisionTree' néven
    """
    train_and_register_model()
