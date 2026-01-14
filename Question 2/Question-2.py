import os
import pandas as pd


def load_all_temperature_data(folder_path="temperatures"):
    """
    Load all CSV files from the temperatures folder and combine them
    into a single DataFrame.
    """
    all_data = []

    if not os.path.exists(folder_path):
        print(f"Error: '{folder_path}' folder not found!")
        return pd.DataFrame()

    csv_files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]

    if not csv_files:
        print(f"No CSV files found in '{folder_path}' folder!")
        return pd.DataFrame()

    print(f"Found {len(csv_files)} CSV file(s). Loading data...")

    for file in csv_files:
        file_path = os.path.join(folder_path, file)
        try:
            df = pd.read_csv(file_path)
            all_data.append(df)
            print(f"Loaded: {file}")
        except Exception as e:
            print(f"Error loading {file}: {e}")

    combined_df = pd.concat(all_data, ignore_index=True)
    print(f"Total records loaded: {len(combined_df)}")
    return combined_df


def get_season(month):
    """
    Return Australian season based on month number.
    """
    if month in [12, 1, 2]:
        return "Summer"
    elif month in [3, 4, 5]:
        return "Autumn"
    elif month in [6, 7, 8]:
        return "Winter"
    elif month in [9, 10, 11]:
        return "Spring"
    return None


def calculate_seasonal_averages(df):
    """
    Calculate average temperature for each season across
    all stations and all years.
    Results saved to 'average_temp.txt'.
    """
    print("\nCalculating Seasonal Average Temperatures...")

    date_col = None
    temp_col = None

    for col in df.columns:
        if "date" in col.lower():
            date_col = col
        if "temp" in col.lower() and "station" not in col.lower():
            temp_col = col

    if date_col is None or temp_col is None:
        print("Error: Date or temperature column not found.")
        print("Available columns:", df.columns.tolist())
        return

    df["date_parsed"] = pd.to_datetime(df[date_col], errors="coerce")
    df["month"] = df["date_parsed"].dt.month
    df["season"] = df["month"].apply(get_season)

    seasonal_avg = df.groupby("season")[temp_col].mean()

    season_order = ["Summer", "Autumn", "Winter", "Spring"]
    seasonal_avg = seasonal_avg.reindex(season_order)

    with open("average_temp.txt", "w") as f:
        f.write("Seasonal Average Temperatures (All Stations, All Years)\n")
        f.write("=" * 60 + "\n\n")
        for season, avg in seasonal_avg.items():
            if not pd.isna(avg):
                line = f"{season}: {avg:.1f}°C\n"
                f.write(line)
                print(line.strip())

    print("Saved results to 'average_temp.txt'")


def find_largest_temperature_range(df):
    """
    Find station(s) with the largest temperature range.
    Results saved to 'largest_temp_range_station.txt'.
    """
    print("\nFinding Largest Temperature Range...")

    station_col = None
    temp_col = None

    for col in df.columns:
        if "station" in col.lower():
            station_col = col
        if "temp" in col.lower() and "station" not in col.lower():
            temp_col = col

    if station_col is None or temp_col is None:
        print("Error: Station or temperature column not found.")
        return

    stats = df.groupby(station_col)[temp_col].agg(["min", "max"])
    stats["range"] = stats["max"] - stats["min"]

    max_range = stats["range"].max()
    top_stations = stats[stats["range"] == max_range]

    with open("largest_temp_range_station.txt", "w") as f:
        f.write("Station(s) with Largest Temperature Range\n")
        f.write("=" * 60 + "\n\n")
        for station, row in top_stations.iterrows():
            line = (
                f"Station {station}: Range {row['range']:.1f}°C "
                f"(Max: {row['max']:.1f}°C, Min: {row['min']:.1f}°C)\n"
            )
            f.write(line)
            print(line.strip())

    print("Saved results to 'largest_temp_range_station.txt'")


def find_temperature_stability(df):
    """
    Identify the most stable and most variable stations based on
    standard deviation of temperature.
    Results saved to 'temperature_stability_stations.txt'.
    """
    print("\nFinding Temperature Stability...")

    station_col = None
    temp_col = None

    for col in df.columns:
        if "station" in col.lower():
            station_col = col
        if "temp" in col.lower() and "station" not in col.lower():
            temp_col = col

    if station_col is None or temp_col is None:
        print("Error: Station or temperature column not found.")
        return

    std_dev = df.groupby(station_col)[temp_col].std()

    min_std = std_dev.min()
    max_std = std_dev.max()

    most_stable = std_dev[std_dev == min_std]
    most_variable = std_dev[std_dev == max_std]

    with open("temperature_stability_stations.txt", "w") as f:
        f.write("Temperature Stability Analysis\n")
        f.write("=" * 60 + "\n\n")

        f.write("Most Stable Station(s):\n")
        for station, val in most_stable.items():
            line = f"Station {station}: StdDev {val:.1f}°C\n"
            f.write(line)
            print("Most Stable:", line.strip())

        f.write("\nMost Variable Station(s):\n")
        for station, val in most_variable.items():
            line = f"Station {station}: StdDev {val:.1f}°C\n"
            f.write(line)
            print("Most Variable:", line.strip())

    print("Saved results to 'temperature_stability_stations.txt'")


def main():
    """
    Main program execution.
    """
    print("=" * 60)
    print("Temperature Data Analysis Program")
    print("=" * 60)

    df = load_all_temperature_data()

    if df.empty:
        print("No data loaded. Please check the temperatures folder.")
        return

    print("Columns found:", df.columns.tolist())

    calculate_seasonal_averages(df)
    find_largest_temperature_range(df)
    find_temperature_stability(df)

    print("\nAnalysis complete!")
    print("Output files created:")
    print(" - average_temp.txt")
    print(" - largest_temp_range_station.txt")
    print(" - temperature_stability_stations.txt")
    print("=" * 60)


if __name__ == "__main__":
    main()
