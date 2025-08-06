import json, os, requests, time
from pathlib import Path
from . import process
from fpl_ai.config import FPL_API_URL, RAW_DATA_DIR

def _get(endpoint: str):
    """Resilient GET with basic rate‑limit handling."""
    url = f"{FPL_API_URL}{endpoint}"
    for _ in range(5):
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return r.json()
        time.sleep(1)
    r.raise_for_status()

def download_static():
    out = Path(RAW_DATA_DIR) / "bootstrap_static.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    json.dump(_get("bootstrap-static/"), out.open("w"))

if __name__ == "__main__":
    download_static()
    process.main()  # optional auto‑process
