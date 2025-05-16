### === Imports ===
import json
import os
import sys

def resource_path(filename):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(os.path.abspath("."), filename)

def save_data(expense_book, filename="data.json"):
    path = resource_path(filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(expense_book, f, ensure_ascii=False, indent=2)

def load_data(filename="data.json"):
    path = resource_path(filename)
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []