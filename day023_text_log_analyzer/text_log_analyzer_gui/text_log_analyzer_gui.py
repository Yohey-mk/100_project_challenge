# text_log_analyzer_gui.py

import streamlit as st
from collections import Counter
import pandas as pd


# load log file
def get_log_lines(filename="log_file.txt"):
    with open("log_file.txt", "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

# Count number of user comments
def count_user_msg(log_lines):
    counter = Counter()
    for line in log_lines:
        try:
            _, username, _ = line.rsplit(":", 2)
            counter[username] += 1
        except ValueError:
            continue
    return counter

# Count filtered user comments
def filter_by_user(log_lines, username):
    results = []
    for line in log_lines:
        try:
            timestamp, u_name, comment = line.rsplit(":", 2)
            if username == "" or u_name == username:
                results.append({"timestamp": timestamp, "username": u_name, "comment": comment})
        except ValueError:
            continue
    return results

# GUI Components
st.title("Text Log Analyzer")

# file upload
uploaded_file = st.file_uploader("Upload text log", type=["txt"])
if uploaded_file is not None:
    log_lines = [line.decode("utf-8").strip() for line in uploaded_file]
else:
    log_lines = get_log_lines()

# List usernames
counter = count_user_msg(log_lines)
user_list = [""] + sorted(counter.keys())
selected_user = st.selectbox("Select user", user_list)

# comments filter
filtered_data = filter_by_user(log_lines, selected_user)
df = pd.DataFrame(filtered_data)

st.subheader("List of comments")
st.dataframe(df)

# Comments rank
st.subheader("Comment Rank")
ranking_df = pd.DataFrame(counter.items(), columns=["username", "message_count"])
ranking_df = ranking_df.sort_values(by="message_count", ascending=False)
st.dataframe(ranking_df)

# usernameで棒グラフ化
st.bar_chart(ranking_df.set_index("username"))

# Download CSV
csv_data = ranking_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download the ranking by CSV",
    data=csv_data,
    file_name="output.csv",
    mime="text/csv"
)