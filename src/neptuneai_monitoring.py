"""
Neptune AI alapú modell monitoring.
"""

import neptune
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import mlflow.pyfunc
from src.credentials import neptune_ai

def run_monitoring():
    """
    Run the monitoring process
    This function is extracted to be callable by Airflow
    """
    # Adatok betöltése
    iris = load_iris()
    X = pd.DataFrame(iris.data, columns=iris.feature_names)
    y = pd.Series(iris.target, name='target')
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Betöltjük a modellt az MLflow-ból
    try:
        model = mlflow.pyfunc.load_model("models:/IrisDecisionTree/Production")
    except Exception as e:
        print(f"Hiba a modell betöltésekor: {e}")
        try:
            print("Próbálkozás a legfrissebb verzióval...")
            client = mlflow.tracking.MlflowClient()
            latest_version = max([int(mv.version) for mv in client.search_model_versions("name='IrisDecisionTree'")])
            model = mlflow.pyfunc.load_model(f"models:/IrisDecisionTree/{latest_version}")
        except Exception as e2:
            print(f"Nem sikerült betölteni a modellt: {e2}")
            return

    # Inicializáljuk a Neptune kapcsolatot
    run = neptune.init_run(
        project=neptune_ai.project,
        api_token=neptune_ai.api_token,
        name="model-monitoring",
        tags=["monitoring", "mlsecops", "iris"]
    )

    try:
        # Monitoring metrikák számítása és logolása
        print("Monitoring metrikák számítása...")
        
        # Predikció a teszt adatokon
        y_pred = model.predict(X_test)
        
        # Neptuneba logolás
        run["test/confusion_matrix"] = neptune.types.File.as_html(
            pd.crosstab(y_test, y_pred, rownames=['Actual'], colnames=['Predicted'])
        )
        
        # Accuracy logolás
        accuracy = np.mean(y_pred == y_test)
        run["test/accuracy"] = accuracy
        
        # Feature fontosság szimuláció (mivel a DecisionTree modell nem adja vissza közvetlenül)
        # Valós esetben ez a modellből jönne
        feature_importance = np.random.random(size=X.shape[1])
        feature_importance = feature_importance / np.sum(feature_importance)
        for i, feature in enumerate(iris.feature_names):
            run[f"feature_importance/{feature}"] = feature_importance[i]
        
        print(f"Monitoring metrikák sikeresen logolva Neptune AI-ba: {run.get_url()}")
    finally:
        # Mindig zárjuk le a Neptune futtatást
        run.stop()

if __name__ == "__main__":
    run_monitoring()
