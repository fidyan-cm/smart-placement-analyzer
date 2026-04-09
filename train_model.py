import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from xgboost import XGBClassifier

# ── 1. Load data ──────────────────────────────────────────────
df = pd.read_csv("placement_data.csv")

X = df.drop("Placement_Status", axis=1)
y = df["Placement_Status"]

# ── 2. Train/test split ───────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ── 3. Scale features (needed for Logistic Regression) ────────
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)

# ── 4. Define models ──────────────────────────────────────────
models = {
    "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
    "Random Forest":       RandomForestClassifier(n_estimators=100, random_state=42),
    "XGBoost":             XGBClassifier(n_estimators=100, random_state=42,
                                     eval_metric="logloss"),
}

# ── 5. Train, evaluate, compare ───────────────────────────────
results = {}

print("\n" + "="*55)
print(f"{'Model':<25} {'Accuracy':>10}")
print("="*55)

for name, model in models.items():
    # Logistic Regression needs scaled data; tree models don't
    if name == "Logistic Regression":
        model.fit(X_train_scaled, y_train)
        y_pred = model.predict(X_test_scaled)
    else:
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    results[name] = {"model": model, "accuracy": acc, "scaled": name == "Logistic Regression"}
    print(f"{name:<25} {acc:>10.4f}")

print("="*55)

# ── 6. Pick best model ────────────────────────────────────────
best_name = max(results, key=lambda k: results[k]["accuracy"])
best_info  = results[best_name]

print(f"\nBest model: {best_name} ({best_info['accuracy']:.4f})")

# ── 7. Detailed report for best model ────────────────────────
if best_info["scaled"]:
    y_best_pred = best_info["model"].predict(X_test_scaled)
else:
    y_best_pred = best_info["model"].predict(X_test)

print("\nClassification Report:")
print(classification_report(y_test, y_best_pred))

# ── 8. Save model + scaler ────────────────────────────────────
bundle = {
    "model":        best_info["model"],
    "scaler":       scaler,
    "model_name":   best_name,
    "accuracy":     best_info["accuracy"],
    "feature_cols": list(X.columns),
    "uses_scaling": best_info["scaled"],
}
joblib.dump(bundle, "placement_model.pkl")
print(f"\nSaved → placement_model.pkl  (bundle includes scaler + metadata)")