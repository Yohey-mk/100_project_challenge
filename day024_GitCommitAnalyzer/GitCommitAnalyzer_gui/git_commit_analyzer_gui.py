# git_commit_analyzer_gui.py

import streamlit as st
import subprocess
from datetime import datetime
from collections import Counter
import pandas as pd
from pandas.api.types import CategoricalDtype
import matplotlib.pyplot as plt

### === Functions ===
def get_git_log(command=None):
    if command is None:
        command = ["git", "log", "--pretty=format:'%h|%an|%ad|%s'", "--date=iso"]
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True
            )
            commits = []
            for line in result.stdout.split("\n"):
                try:
                    commit_hash, author, date_str, message = line.split("|", 3)
                    date_obj = datetime.strptime(date_str.strip(), "%Y-%m-%d %H:%M:%S %z")
                    commits.append({
                        "hash": commit_hash,
                        "author": author,
                        "date": date_obj,
                        "message": message
                    })
                except ValueError:
                    continue
            return commits
        except subprocess.CalledProcessError as e:
            st.write("Error", e.stderr or str(e))
            return []



### === RUN APP ===
st.title("Git Commit Analyzer")
df = pd.DataFrame(get_git_log())
#test 