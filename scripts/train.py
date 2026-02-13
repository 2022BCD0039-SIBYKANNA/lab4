import pandas as pd
import json
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# -------------------------------
# Create folders
# -------------------------------
os.makedirs("model", exist_ok=True)
os.makedirs("app/artifacts", exist_ok=True)

# -------------------------------
# Load dataset
# -------------------------------
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv"
data = pd.read_csv(url, sep=";")

X = data.drop("quality", axis=1)
y = data["quality"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -------------------------------
# Train model
# -------------------------------
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# -------------------------------
# Evaluate
# -------------------------------
y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# -------------------------------
# Save model in model/
# -------------------------------
joblib.dump(model, "model/model.pkl")

# -------------------------------
# Save metrics in app/artifacts/
# -------------------------------
metrics = {
    "mse": float(mse),
    "accuracy": float(r2)   # VERY IMPORTANT: use accuracy key
}

with open("app/artifacts/metrics.json", "w") as f:
    json.dump(metrics, f)

print("Training complete")
print(metrics)
