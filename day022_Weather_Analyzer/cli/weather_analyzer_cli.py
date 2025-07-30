# weather_analyzer_cli.py

### === Imports ===
from data_loader import load_weather_data
from analyzer import show_summary, analyze_temperature_trend, show_specific_trend
from visualizer import plot_temperature_trend, plot_specific_trend

### === App Logics ===
def main():
    print("Welcome to Weather Data Analyzer!")
    file_path = input("Enter CSV path: ")
    df = load_weather_data(file_path)

    while True:
        print("\n1. Show data summary\n2. Show temeperature trend\n3. Show specific periods\n4. Quit")
        choice = input("Enter your choice(1 - 4): ")

        if choice == "1":
            show_summary(df)
        elif choice == "2":
            analyze_temperature_trend(df)
            plot_temperature_trend(df)
        elif choice == "3":
            filtered_df = show_specific_trend(df)
            plot_specific_trend(filtered_df)
        elif choice == "4":
            break
        else:
            print("Invalid input")

### === Run App ===
if __name__ == "__main__":
    main()




### Notes
# CLIの起点。メニュー表示、ファイル指定、分析の選択などを担当。