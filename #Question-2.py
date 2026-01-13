import os
import pandas as pd
import numpy as np
from pathlib import Path

def load_all_temperature_data(folder_path="temperatures"):
    """
    Load all CSV files from the temperatures folder and combine them.
    Returns a combined DataFrame with all temperature data.
    """
    all_data = []
    
    # Check if folder exists
    if not os.path.exists(folder_path):
        print(f"Error: '{folder_path}' folder not found!")
        return pd.DataFrame()
    
    # Get all CSV files in the folder
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    
    if not csv_files:
        print(f"No CSV files found in '{folder_path}' folder!")
        return pd.DataFrame()
    
    print(f"Found {len(csv_files)} CSV file(s) to process...")
    
    # Load each CSV file
    for file in csv_files:
        file_path = os.path.join(folder_path, file)
        try:
            df = pd.read_csv(file_path)
            all_data.append(df)
            print(f"Loaded: {file}")
        except Exception as e:
            print(f"Error loading {file}: {e}")
    
    # Combine all dataframes
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        print(f"\nTotal records loaded: {len(combined_df)}")
        return combined_df
    else:
        return pd.DataFrame()

def get_season(month):
    """
    Determine the Australian season based on month number.
    Summer: Dec-Feb (12, 1, 2)
    Autumn: Mar-May (3, 4, 5)
    Winter: Jun-Aug (6, 7, 8)
    Spring: Sep-Nov (9, 10, 11)
    """
    if month in [12, 1, 2]:
        return 'Summer'
    elif month in [3, 4, 5]:
        return 'Autumn'
    elif month in [6, 7, 8]:
        return 'Winter'
    elif month in [9, 10, 11]:
        return 'Spring'
    else:
        return None

def calculate_seasonal_averages(df):
    """
    Calculate average temperature for each season across all stations and years.
    Saves results to 'average_temp.txt'.
    """
    print("\n=== Calculating Seasonal Averages ===")
    
    # Ensure we have a date column (adjust column name as needed)
    # Common column names: 'Date', 'date', 'DATE', 'Month', 'month'
    date_col = None
    temp_col = None
    
    # Find date and temperature columns
    for col in df.columns:
        if 'date' in col.lower():
            date_col = col
        if 'temp' in col.lower() and 'station' not in col.lower():
            temp_col = col
    
    if date_col is None or temp_col is None:
        print("Error: Could not find date or temperature columns!")
        print(f"Available columns: {df.columns.tolist()}")
        return
    
    # Convert date column to datetime
    df['date_parsed'] = pd.to_datetime(df[date_col], errors='coerce')
    df['month'] = df['date_parsed'].dt.month
    df['season'] = df['month'].apply(get_season)
    
    # Calculate seasonal averages (ignoring NaN values)
    seasonal_avg = df.groupby('season')[temp_col].mean()
    
    # Sort by season order
    season_order = ['Summer', 'Autumn', 'Winter', 'Spring']
    seasonal_avg = seasonal_avg.reindex(season_order)
    
    # Save to file
    with open('average_temp.txt', 'w') as f:
        f.write("Seasonal Average Temperatures (All Stations, All Years)\n")
        f.write("=" * 60 + "\n\n")
        for season, avg_temp in seasonal_avg.items():
            if not pd.isna(avg_temp):
                line = f"{season}: {avg_temp:.1f}°C\n"
                f.write(line)
                print(line.strip())
    
    print("\nResults saved to 'average_temp.txt'")

def find_largest_temperature_range(df):
    """
    Find station(s) with the largest temperature range.
    Saves results to 'largest_temp_range_station.txt'.
    """
    print("\n=== Finding Largest Temperature Range ===")
    
    # Find station and temperature columns
    station_col = None
    temp_col = None
    
    for col in df.columns:
        if 'station' in col.lower():
            station_col = col
        if 'temp' in col.lower() and 'station' not in col.lower():
            temp_col = col
    
    if station_col is None or temp_col is None:
        print("Error: Could not find station or temperature columns!")
        return
    
    # Calculate min, max, and range for each station
    station_stats = df.groupby(station_col)[temp_col].agg(['min', 'max'])
    station_stats['range'] = station_stats['max'] - station_stats['min']
    
    # Find the maximum range
    max_range = station_stats['range'].max()
    
    # Find all stations with the maximum range
    stations_with_max_range = station_stats[station_stats['range'] == max_range]
    
    # Save to file
    with open('largest_temp_range_station.txt', 'w') as f:
        f.write("Station(s) with Largest Temperature Range\n")
        f.write("=" * 60 + "\n\n")
        for station, row in stations_with_max_range.iterrows():
            line = f"Station {station}: Range {row['range']:.1f}°C (Max: {row['max']:.1f}°C, Min: {row['min']:.1f}°C)\n"
            f.write(line)
            print(line.strip())
    
    print("\nResults saved to 'largest_temp_range_station.txt'")

def find_temperature_stability(df):
    """
    Find station(s) with most stable and most variable temperatures.
    Saves results to 'temperature_stability_stations.txt'.
    """
    print("\n=== Finding Temperature Stability ===")
    
    # Find station and temperature columns
    station_col = None
    temp_col = None
    
    for col in df.columns:
        if 'station' in col.lower():
            station_col = col
        if 'temp' in col.lower() and 'station' not in col.lower():
            temp_col = col
    
    if station_col is None or temp_col is None:
        print("Error: Could not find station or temperature columns!")
        return
    
    # Calculate standard deviation for each station
    station_std = df.groupby(station_col)[temp_col].std()
    
    # Find minimum and maximum standard deviation
    min_std = station_std.min()
    max_std = station_std.max()
    
    # Find all stations with min and max std
    most_stable = station_std[station_std == min_std]
    most_variable = station_std[station_std == max_std]
    
    # Save to file
    with open('temperature_stability_stations.txt', 'w') as f:
        f.write("Temperature Stability Analysis\n")
        f.write("=" * 60 + "\n\n")
        
        f.write("Most Stable Station(s):\n")
        for station, std_val in most_stable.items():
            line = f"Station {station}: StdDev {std_val:.1f}°C\n"
            f.write(line)
            print(f"Most Stable: {line.strip()}")
        
        f.write("\nMost Variable Station(s):\n")
        for station, std_val in most_variable.items():
            line = f"Station {station}: StdDev {std_val:.1f}°C\n"
            f.write(line)
            print(f"Most Variable: {line.strip()}")
    
    print("\nResults saved to 'temperature_stability_stations.txt'")

def main():
    """
    Main function to run all temperature data analyses.
    """
    print("=" * 60)
    print("Temperature Data Analysis Program")
    print("=" * 60)
    
    # Load all temperature data
    df = load_all_temperature_data()
    
    if df.empty:
        print("\nNo data loaded. Please ensure CSV files are in the 'temperatures' folder.")
        return
    
    print(f"\nDataFrame shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    
    # Run all analyses
    try:
        calculate_seasonal_averages(df)
        find_largest_temperature_range(df)
        find_temperature_stability(df)
        
        print("\n" + "=" * 60)
        print("Analysis complete! Check the output files:")
        print("  - average_temp.txt")
        print("  - largest_temp_range_station.txt")
        print("  - temperature_stability_stations.txt")
        print("=" * 60)
        
    except Exception as e:
        print(f"\nError during analysis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
