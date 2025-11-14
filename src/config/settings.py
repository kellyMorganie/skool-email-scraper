thonpython
import json

def load_settings(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception:
        return {}