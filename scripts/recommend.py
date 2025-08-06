import pandas as pd
from fpl_ai.models.baseline import RollingAverageModel
from fpl_ai.optimiser.solver import build_team
from fpl_ai.config import PROCESSED_DATA_DIR

def run():
    df = pd.read_parquet(f"{PROCESSED_DATA_DIR}/players_latest.parquet")
    model = RollingAverageModel(window=5)
    model.fit(df)
    df["xp"] = model.predict(df)
    squad = build_team(df["xp"], df)
    print(squad[["first_name", "second_name", "now_cost", "xp"]])

if __name__ == "__main__":
    run()
