import pandas as pd, pickle
from pathlib import Path
from fpl_ai.config import PROCESSED_DATA_DIR, MODEL_DIR

class RollingAverageModel:
    def __init__(self, window: int = 5):
        self.window = window
    def fit(self, df: pd.DataFrame):
        # Nothing to fit for rolling‑average
        self.cols = ["id", "ppg"]
    def predict(self, df: pd.DataFrame):
        return df["ppg"].rolling(self.window, min_periods=1).mean().shift(1)
    def save(self):
        Path(MODEL_DIR).mkdir(exist_ok=True, parents=True)
        pickle.dump(self, open(Path(MODEL_DIR)/"baseline.pkl", "wb"))
