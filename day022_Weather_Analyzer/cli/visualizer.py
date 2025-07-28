# visualizer.py

import matplotlib.pyplot as plt

def plot_temperature_trend(df):
    plt.figure(figsize=(10, 4))
    plt.plot(df["Date"], df["Temperature"], marker="o", linestyle="-")
    plt.title("Temperature trend")
    plt.xlabel("Date")
    plt.ylabel("Temperature(C)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()