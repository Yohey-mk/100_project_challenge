#save_notebook.py
### === Imports ===
import os
import sys
import json

### === Functions ===
def resource_path(filename):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys.MEIPASS, filename)
    return os.path.join(os.path.abspath("."), filename)

def save_notebook(user_notebook, filename="day14_notebook.json"):
    path = resource_path(filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(user_notebook, f, ensure_ascii=False, indent=2)

def load_notebook(filename="day14_notebook.json"):
    path = resource_path(filename)
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return[]