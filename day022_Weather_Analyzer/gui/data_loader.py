# data_loader.py

import streamlit as st
import pandas as pd
def load_data():
    uploaded_file = st.file_uploader("Uplaod CSV", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write("Data Preview", df.head())
        return df
    return None