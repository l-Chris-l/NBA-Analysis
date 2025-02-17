import os
import pandas as pd
import json

# Path to the old Excel file
excel_file_path = "teams_stats.xlsx"

# Check if the old Excel file exists and delete it
if os.path.exists(excel_file_path):
    os.remove(excel_file_path)
    print(f"Old Excel file '{excel_file_path}' deleted.")

# Load the team data with stats
json_file_path = "data/teams_data.json"

with open(json_file_path, "r") as json_file:
    teams_info = json.load(json_file)

# Prepare the data for Excel
excel_data = []

# Loop through each team and their stats
for team in teams_info["teams"]:
    team_data = {
        "Team Name": team["name"],
        "Market": team["market"],
        "Alias": team["alias"]
    }

    # Flatten the additional_info dictionary (season stats)
    for season_key, stats in team["additional_info"].items():
        # Flatten each season's stats into the team_data
        for stat_key, stat_value in stats.get('statistics', {}).items():
            team_data[f"{season_key}_{stat_key}"] = stat_value

    excel_data.append(team_data)

# Convert the data to a pandas DataFrame
df = pd.DataFrame(excel_data)

# Save to Excel
df.to_excel(excel_file_path, index=False)

print(f"Updated data saved to '{excel_file_path}'.")
