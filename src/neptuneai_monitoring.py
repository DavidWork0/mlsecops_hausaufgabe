"""
Neptune.ai monitoring script az Iris modellhez.
Ez a script model teljesítményt és adatokat vizualizálja és rögzíti a Neptune.ai platformon.
"""

import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import neptune
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import credentials

# Adatok betöltése
iris = load_iris()
X = pd.DataFrame(iris.data, columns=iris.feature_names)
y = pd.Series(iris.target, name='target')

# Tanító és teszt adatok
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
train = X_train.copy()
train['target'] = y_train.values
test = X_test.copy()
test['target'] = y_test.values

# Neptune.ai kapcsolat inicializálása
run = neptune.init_run(
    project=credentials.neptune_ai.project,
    api_token=credentials.neptune_ai.api_token,
    tags=["monitoring", "iris-dataset"]
)

# Adat tulajdonságok monitorozása
run["data/train_shape"] = train.shape
run["data/test_shape"] = test.shape

# Statisztikai adatok rögzítése
train_stats = train.describe().to_dict()
test_stats = test.describe().to_dict()
run["data/train_stats"] = train_stats
run["data/test_stats"] = test_stats

# Feature eloszlások vizualizálása
fig, axes = plt.subplots(2, 2, figsize=(15, 10))
fig.suptitle("Feature Distributions: Train vs Test", fontsize=16)
axes = axes.flatten()

for i, feature in enumerate(iris.feature_names):
    sns.histplot(train[feature], kde=True, ax=axes[i], color="blue", label="Train", alpha=0.5)
    sns.histplot(test[feature], kde=True, ax=axes[i], color="red", label="Test", alpha=0.5)
    axes[i].set_title(feature)
    axes[i].legend()

plt.tight_layout()
run["visualizations/feature_distributions"].upload(fig)

# Adatok közötti különbségek (drift) számítása
for feature in iris.feature_names:
    mean_diff = np.mean(test[feature]) - np.mean(train[feature])
    std_diff = np.std(test[feature]) - np.std(train[feature])
    run[f"drift/{feature}/mean_difference"] = mean_diff
    run[f"drift/{feature}/std_difference"] = std_diff
    
    # KL divergencia vagy egyéb eltérési metrikák is számolhatók

# Összefoglaló
run["monitoring/summary"] = "A monitoring folyamat sikeresen befejeződött"

# Neptune.ai kapcsolat lezárása
run.stop()
print('Neptune.ai monitoring jelentés elkészült és feltöltve a Neptune platformra')
