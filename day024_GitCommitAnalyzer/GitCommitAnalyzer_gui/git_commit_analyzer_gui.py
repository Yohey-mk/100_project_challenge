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

def generate_ranking(df, top_n=None):
    counter = Counter()
    for _, row in df.iterrows():
        counter[row['author']] += 1
    lines = []
    for i, (username, count) in enumerate(counter.most_common(top_n), 1):
        lines.append(f"{i}: {username} - {count}")
    return "\n".join(lines)

def filter_by_weekdays(df):
    df_copy = df.copy()
    weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    cat_type = CategoricalDtype(categories=weekday_order, ordered=True)
    df_copy['weekday'] = df_copy['date'].dt.day_name().astype(cat_type)
    filtered_by_weekdays = df_copy.groupby('weekday').size().sort_index()
    return filtered_by_weekdays

def filter_by_time(df):
    filtered_by_time = df.groupby(df['date'].dt.hour).size().sort_index()
    return filtered_by_time

def visualizer(series, title, xlabel, ylabel, kind="Line"):
    fig, ax = plt.subplots(figsize=(10, 5))
    if kind == "bar":
        ax.bar(series.index, series.values)
    else:
        ax.set_xticks(range(24))
        ax.plot(series.index, series.values, marker="o")
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.xticks(rotation=45 if kind == "bar" else 0)
    st.pyplot(fig)

def select_command():
    option = st.selectbox(
        "Choose your option",
        ("Show summary", "Filter by committer", "Show ranking", "Filter by weekdays", "Filter by time")
    )
    return option 

### === RUN APP ===
st.title("Git Commit Analyzer")
log_output = get_git_log(command=["git", "log", "--pretty=format:'%h|%an|%ad|%s'", "--date=iso"])
df = pd.DataFrame(log_output)
option = select_command()
if not df.empty:
    if option == "Show summary":
        summary = pd.DataFrame(df)
        st.dataframe(summary)
    elif option == "Filter by committer":
        result = df.groupby(df['author']).size().sort_values(ascending=False)
        st.dataframe(result)
    elif option == "Show ranking":
        result = generate_ranking(df, top_n=10)
        st.write(result)
    elif option == "Filter by weekdays":
        result = filter_by_weekdays(df)
        st.dataframe(result)
        #matplotlibで描画
        visualizer(result, "Commits by Weekday", "Weekday", "Number of Commits", kind="bar")
        #以下不要（学びの記録として残しておく）
        #fig, ax = plt.subplots(figsize=(10, 5))
        #ax.bar(result.index, result.values)
        #ax.set_title("Commits by Weekday")
        #ax.set_xlabel("Weekday")
        #ax.set_ylabel("Number of Commits")
        #plt.xticks(rotation=45)
        #st.pyplot(fig)
    elif option == "Filter by time":
        result = filter_by_time(df)

        # すべての時間を含むようにreindex
        all_hours = pd.Series(range(24), name="Hour")
        result = result.reindex(all_hours, fill_value=0)

        st.dataframe(result)

        #matplotlibで描画
        visualizer(result, "Commit Hour Trend", "Hour", "Number of Commits", kind="line")
        #以下不要（学びの記録として残しておく）
        #fig, ax = plt.subplots(figsize=(10, 5))
        #ax.plot(result.index, result.values, marker="o")
        #ax.set_xticks(range(24))
        #ax.set_title("Commit Hour Trend")
        #ax.set_xlabel("Hour")
        #ax.set_ylabel("Number of commits")
        #st.pyplot(fig)
    else:
        st.subheader("Unknown")

else:
    st.warning("Git logが取得できませんでした。リポジトリ内で実行していますか？")