
import os
import csv
import math

# List of all months in CSV file
MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]
# List of Australian Seasons with months
SEASONS = {
    "Summer": ["December", "January", "February"],
    "Autumn": ["March", "April", "May"],
    "Winter": ["June", "July", "August"],
    "Spring": ["September", "October", "November"],
}

STATION_COL = "STATION_NAME"

# Check to see whether a CSV value is missing
def is_missing(value_str):
    """Return True if the CSV value is missing/NaN/empty."""
    if value_str is None:
        return True
    s = str(value_str).strip()
    if s == "":
        return True
    if s.lower() == "nan":
        return True
    return False


def to_float_or_none(value_str):
   
    if is_missing(value_str):
        return None
    try:
        return float(value_str)
    except ValueError:
        return None

# Calculate the mean(Average)
def mean(values):

    return sum(values) / len(values)

# Calculate the S.D
#If only one value exists, the deviation is zero
def pop_stddev(values):

    if len(values) <= 1:
        return 0.0
    m = mean(values)
    var = sum((x - m) ** 2 for x in values) / len(values)
    return math.sqrt(var)

# Find all CSV files in the folder named "temperatures"
def find_csv_files():
    folder = "temperatures"
    if os.path.isdir(folder):
        base = folder
    else:
        base = "."  

    csv_files = []
    for name in os.listdir(base):
        if name.lower().endswith(".csv"):
            csv_files.append(os.path.join(base, name))

    csv_files.sort()
    return csv_files

# To process all csv files and collect required data
def process_all_files(csv_files):
    
    season_values = {s: [] for s in SEASONS.keys()}


    station_temps = {}

    for path in csv_files:
        with open(path, "r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)

            if STATION_COL not in reader.fieldnames:
                raise ValueError("Missing required column: " + STATION_COL)

            for m in MONTHS:
                if m not in reader.fieldnames:
                    raise ValueError("Missing month column: " + m + " in file " + path)
            
            # Process each row in CSV file
            for row in reader:
                station = (row.get(STATION_COL) or "").strip()
                if station == "":
                    continue

                if station not in station_temps:
                    station_temps[station] = []

                month_value = {}
                for m in MONTHS:
                    v = to_float_or_none(row.get(m))
                    month_value[m] = v
                    if v is not None:
                        station_temps[station].append(v)

                for season_name, season_months in SEASONS.items():
                    for sm in season_months:
                        v = month_value.get(sm)
                        if v is not None:
                            season_values[season_name].append(v)

    return season_values, station_temps

# Write seasonal average temperature in the file
def write_seasonal_averages(season_values):

    with open("average_temp.txt", "w", encoding="utf-8") as out:
        for season_name in ["Summer", "Autumn", "Winter", "Spring"]:
            vals = season_values[season_name]
            if len(vals) == 0:
                out.write(season_name + ": No data\n")
            else:
                avg = mean(vals)
                out.write(f"{season_name}: {avg:.2f}C\n")

# write station with largest temperature range
def write_largest_range(station_temps):

    best_range = None
    best_list = []

    station_stats = {}  # station -> (min, max, range)
    for station, temps in station_temps.items():
        if len(temps) == 0:
            continue
        mn = min(temps)
        mx = max(temps)
        r = mx - mn
        station_stats[station] = (mn, mx, r)

        if best_range is None or r > best_range + 1e-12:
            best_range = r
            best_list = [station]
        elif abs(r - best_range) <= 1e-12:
            best_list.append(station)

    with open("largest_temp_range_station.txt", "w", encoding="utf-8") as out:
        if best_range is None:
            out.write("No data available.\n")
            return

        best_list.sort()
        for station in best_list:
            mn, mx, r = station_stats[station]
            out.write(f"{station}: Range {r:.2f}C (Max: {mx:.2f}C, Min: {mn:.2f}C)\n")

# Write temperature stability result in the file
def write_stability(station_temps):
    station_sd = []

    # Calculate S.D for each station
    for station, temps in station_temps.items():
        if len(temps) == 0:
            continue
        sd = pop_stddev(temps)
        station_sd.append((station, sd))

    if len(station_sd) == 0:
        with open("temperature_stability_stations.txt", "w", encoding="utf-8") as out:
            out.write("No data available.\n")
        return

    min_sd = min(sd for _, sd in station_sd)
    max_sd = max(sd for _, sd in station_sd)

    most_stable = sorted([s for s, sd in station_sd if abs(sd - min_sd) <= 1e-12])
    most_variable = sorted([s for s, sd in station_sd if abs(sd - max_sd) <= 1e-12])

    with open("temperature_stability_stations.txt", "w", encoding="utf-8") as out:
        # List all ties
        for s in most_stable:
            out.write(f"Most Stable: {s}: StdDev {min_sd:.2f}C\n")
        for s in most_variable:
            out.write(f"Most Variable: {s}: StdDev {max_sd:.2f}C\n")

# For main programm execution 
def main():
    csv_files = find_csv_files()
    if len(csv_files) == 0:
        print("No CSV files found.")
        print('Put all year CSV files into a folder named "temperatures", or in this folder.')
        return

    season_values, station_temps = process_all_files(csv_files)

    write_seasonal_averages(season_values)
    write_largest_range(station_temps)
    write_stability(station_temps)

    print("Done")
    print("Created: average_temp.txt")
    print("Created: largest_temp_range_station.txt")
    print("Created: temperature_stability_stations.txt")


main()
