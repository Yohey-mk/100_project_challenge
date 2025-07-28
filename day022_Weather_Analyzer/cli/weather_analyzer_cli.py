# weather_analyzer_cli.py

### === Imports ===
from data_loader import load_weather_data
from analyzer import show_summary, analyze_temperature_trend
from visualizer import plot_temperature_trend

### === Helper Functions ===


### === App Logics ===
def main():
    print("Welcome to Weather Data Analyzer!")
    file_path = input("Enter CSV path: ")
    df = load_weather_data(file_path)

    print("\n1. Show data summary\n2. Show temeperature trend")
    choice = input("Enter your choice(1 or 2): ")

    if choice == "1":
        show_summary(df)
    elif choice == "2":
        analyze_temperature_trend(df)
        plot_temperature_trend(df)
    else:
        print("Invalid input")

### === Run App ===
if __name__ == "__main__":
    main()




### Notes
# CLIの起点。メニュー表示、ファイル指定、分析の選択などを担当。