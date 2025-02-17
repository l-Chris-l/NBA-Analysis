import requests
from dotenv import load_dotenv
import os
import json
import time

# Load environment variables from the .env file
load_dotenv()

# Get the API key, base URL, and stats endpoint from environment variables
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
ENDPOINT_SEASON_STATS = os.getenv("ENDPOINT_SEASON_STATS")  # This is the format you have in the .env

# Path to the teams data JSON file
json_file_path = "data/teams_data.json"

# Load team data
with open(json_file_path, "r") as json_file:
    teams_info = json.load(json_file)

# Define the list of season years and types you want to collect
season_years = ["2021", "2022", "2023", "2024"]  # Add as many years as needed
season_types = ["PRE", "REG", "PIT", "IST", "PST"]  # Updated season types

# Fetch stats for each team and season/year/type combination
for team in teams_info["teams"]:
    team_id = team["id"]  # Get the team ID from the data loaded

    # Loop through each season year and season type
    for season_year in season_years:
        for season_type in season_types:
            # Format the endpoint with the season_year, season_type, and team_id
            url_stats = f"{BASE_URL}{ENDPOINT_SEASON_STATS}".format(
                season_year=season_year,
                season_type=season_type,
                team_id=team_id
            ) + f"?api_key={API_KEY}"

            # Debugging: Print the URL to check if it's correctly formatted
            print(f"Fetching stats for {team['name']} ({season_year} {season_type}): {url_stats}")

            response_stats = requests.get(url_stats)

            # Check the status code and response
            if response_stats.status_code == 200:
                stats_data = response_stats.json()
                # You can save stats for each season/year/type combination separately or merge them
                # For now, adding them to 'additional_info' to organize it better
                team["additional_info"][f"{season_year}_{season_type}"] = stats_data  # Add stats for specific season/year/type combination
            elif response_stats.status_code == 429:
                print(f"Rate limit exceeded. Retrying in 5 seconds...")
                time.sleep(5)  # Wait for 5 seconds before retrying
                response_stats = requests.get(url_stats)  # Retry the request
                if response_stats.status_code == 200:
                    stats_data = response_stats.json()
                    team["additional_info"][f"{season_year}_{season_type}"] = stats_data
            else:
                print(f"Failed to fetch stats for {team['name']} for season {season_year} {season_type}. Status code: {response_stats.status_code}")
                print(f"Response: {response_stats.text}")

# Save the updated team data with stats to the JSON file
with open(json_file_path, "w") as json_file:
    json.dump(teams_info, json_file, indent=4)

print(f"Updated team data with stats saved to '{json_file_path}'.")
