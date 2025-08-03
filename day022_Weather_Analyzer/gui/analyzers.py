# analyzers.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def filter_date(df):
    st.subheader("Data summary")
    st.write(df.describe())

    # ここでオプション選択できるように分岐
    option = st.selectbox(
        "Choose your option",
        ("Filter by date", "Hot Days", "Compare highest temp by month", "Compare lowest temp by month")
    )

    if option == "Filter by date":
        start_date = st.date_input("Start date")
        end_date = st.date_input("End date")

        # 型を揃える
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        df["Date"] = pd.to_datetime(df["Date"])

        filtered_df = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]

        st.write(filtered_df)

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(filtered_df["Date"], filtered_df["Temperature"])
        ax.set_title("Temperature Trend")
        ax.set_xlabel("Date")
        ax.set_ylabel("Temperature")
        plt.xticks(rotation=90)
        st.pyplot(fig)

    elif option == "Hot Days":
        hot_days = df[df["Max Temperature"] > 30]
        st.write(hot_days)
        fig, ax = plt.subplots()
        ax.plot(hot_days["Date"], hot_days["Max Temperature"])
        ax.set_xlabel("Date")
        ax.set_ylabel("Temperature")
        st.pyplot(fig)


    elif option == "Compare highest temp by month":
        df["Date"] = pd.to_datetime(df["Date"])
        # 月ごとの最高気温の行番号を取得
        monthly_max_idx = df.groupby(df["Date"].dt.month)["Max Temperature"].idxmax()
        # 実際のデータ行を取得する
        monthly_max_df = df.loc[monthly_max_idx].sort_values(by="Date")

        st.dataframe(monthly_max_df)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(monthly_max_df["Date"], monthly_max_df["Max Temperature"], marker="o")
        ax.set_xlabel("Month")
        ax.set_ylabel("Max Temp")
        ax.set_title("Monthly Highest Temperature")
        plt.xticks(rotation=75)
        plt.tight_layout()
        st.pyplot(fig)

    elif option == "Compare lowest temp by month":
        df["Date"] = pd.to_datetime(df["Date"])

        monthly_min_idx = df.groupby(df["Date"].dt.month)["Lowest Temperature"].idxmin()
        
        monthly_min_df = df.loc[monthly_min_idx].sort_values(by="Date")
        monthly_min_df["MonthStr"] = monthly_min_df["Date"].dt.strftime("%Y-%m")

        st.dataframe(monthly_min_df)

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(monthly_min_df["MonthStr"], monthly_min_df["Lowest Temperature"], marker="o")
        ax.set_xlabel("Month")
        ax.set_ylabel("Min Temp")
        ax.set_title("Monthly Lowest Temperature")
        plt.xticks(rotation=90)
        #plt.tight_layout()
        st.pyplot(fig)