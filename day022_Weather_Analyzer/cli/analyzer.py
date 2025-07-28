# analyzer.py

def show_summary(df):
    print("Data summary:")
    print(df.describe())

def analyze_temperature_trend(df):
    print("Temperature trend")
    print(df[["Date", "Temperature"]].head())