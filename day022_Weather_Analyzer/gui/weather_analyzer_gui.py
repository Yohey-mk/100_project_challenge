# weather_analyzer_gui.py

### === Imports ===
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from data_loader import load_data
from analyzers import filter_date

### === Helper Functions ===


### === App Logics ===
st.title("Weather Analyzer")
df = load_data()
if df is not None:
    filter_date(df)

### === UI Components ===


### === Run App ===

