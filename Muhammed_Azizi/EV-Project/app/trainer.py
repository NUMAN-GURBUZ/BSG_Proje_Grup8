import os
import pandas as pd
from sklearn.ensemble import IsolationForest
from joblib import dump


DATA_FILE = os.path.join("data", "normal_data.csv")
MODEL_FILE = "model.joblib"


def train_model():
    if not os.path.exists(DATA_FILE):
        print(f"[ERROR] {DATA_FILE} not found.")
        return

    df = pd.read_csv(DATA_FILE)

    if df.empty:
        print("[ERROR] No data found in CSV.")
        return

    # Features
    features = ["energy", "delta_energy", "ocpp_connected"]

    for col in features:
        if col not in df.columns:
            print(f"[ERROR] Missing column: {col}")
            return

    X = df[features].values

    model = IsolationForest(
        n_estimators=200,
        contamination=0.01,
        random_state=42
    )

    model.fit(X)

    dump(model, MODEL_FILE)

    print("✅ Model trained and saved to", MODEL_FILE)


if __name__ == "__main__":
    train_model()
