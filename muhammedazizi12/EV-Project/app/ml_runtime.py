import joblib
import os
import numpy as np

MODEL_FILE = "model.joblib"


class MLDetector:
    def __init__(self):
        if os.path.exists(MODEL_FILE):
            self.model = joblib.load(MODEL_FILE)
            print("✅ ML model loaded.")
        else:
            self.model = None
            print(" No model found. Run trainer.py first.")

    def predict_anomaly(self, energy, delta, ocpp_flag):
        """
        returns:
            (is_anomaly: bool, score: float)
        """

        if self.model is None:
            return False, 0.0

        # feature vector for prediction
        x = np.array([[energy, delta, ocpp_flag]])

        # score_samples → قيم أصغر = شذوذ أكبر
        score = self.model.score_samples(x)[0]

        # isolation forest:
        # label: -1 = anomaly, 1 = normal
        label = self.model.predict(x)[0]

        is_anomaly = (label == -1)

        return is_anomaly, float(score)
