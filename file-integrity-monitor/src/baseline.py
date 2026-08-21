import json
import os

def save_baseline(data, path):
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)

def load_baseline(path):
    if not os.path.exists(path):
        return {}
    with open(path, 'r') as f:
        return json.load(f)
