{
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "intro",
        "language": "markdown"
      },
      "source": [
        "# Iris osztályozás gépi tanulással",
        "Ez a notebook bemutatja az Iris adathalmazon egy egyszerű döntési fa modell tanítását, MLflow trackinggel és model registry-vel."
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "data-load",
        "language": "markdown"
      },
      "source": [
        "## Adatok betöltése és előkészítése"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "load-data",
        "language": "python"
      },
      "source": [
        "import pandas as pd",
        "from sklearn.datasets import load_iris",
        "from sklearn.model_selection import train_test_split",
        "",
        "# Iris adathalmaz betöltése",
        "iris = load_iris()",
        "X = pd.DataFrame(iris.data, columns=iris.feature_names)",
        "y = pd.Series(iris.target, name='target')",
        "",
        "# Adatok felosztása tanító és teszt halmazra",
        "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "model-train",
        "language": "markdown"
      },
      "source": [
        "## Modell tanítása és értékelése"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "train-model",
        "language": "python"
      },
      "source": [
        "from sklearn.tree import DecisionTreeClassifier",
        "from sklearn.metrics import accuracy_score",
        "",
        "# Modell példányosítása és tanítása",
        "clf = DecisionTreeClassifier(random_state=42)",
        "clf.fit(X_train, y_train)",
        "",
        "# Előrejelzés és pontosság számítása",
        "y_pred = clf.predict(X_test)",
        "accuracy = accuracy_score(y_test, y_pred)",
        "print(f'Modell pontossága: {accuracy:.2f}')"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "mlflow-intro",
        "language": "markdown"
      },
      "source": [
        "## MLflow tracking és model registry használata"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "mlflow-track",
        "language": "python"
      },
      "source": [
        "import mlflow",
        "import mlflow.sklearn",
        "",
        "with mlflow.start_run():",
        "    mlflow.sklearn.log_model(clf, 'model')",
        "    mlflow.log_metric('accuracy', accuracy)",
        "    mlflow.log_param('model_type', 'DecisionTreeClassifier')",
        "    print('Modell és metrikák logolva MLflow-ba.')"
      ]
    }
  ]
}