import pandas as pd, json, os
from pathlib import Path
from fpl_ai.config import RAW_DATA_DIR, PROCESSED_DATA_DIR

def _load_static():
    path = Path(RAW_DATA_DIR) / "bootstrap_static.json"
    return json.load(path.open())

def build_player_weekly_df():
    static = _load_static()
    elements = pd.DataFrame(static["elements"])
    # minimal features
    df = elements[["id", "first_name", "second_name", "team", "element_type", "now_cost", "total_points"]]
    df["ppg"] = df["total_points"] / 38  # naive per‑GW
    return df

def main():
    df = build_player_weekly_df()
    out = Path(PROCESSED_DATA_DIR)
    out.mkdir(parents=True, exist_ok=True)
    df.to_parquet(out / "players_latest.parquet")
