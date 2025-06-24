# save_notebook.py

import os
import json
import sys

def resource_path(filename):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys.MEIPASS, filename)
    return os.path.abspath(os.path.join(".", filename))

def save_notebook(notebook, filename="day17_schedule_gui.json"):
    path = resource_path(filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(notebook, f, ensure_ascii=False, indent=2)

def load_notebook(filename="day17_schedule_gui.json"):
    path = resource_path(filename)
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []