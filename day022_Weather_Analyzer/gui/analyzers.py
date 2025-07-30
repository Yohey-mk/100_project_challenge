# analyzers.py

import streamlit as st
import pandas as pd

def filter_date(df):
    st.subheader("Data summary")
    st.write(df.describe())