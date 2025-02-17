import requests
from dotenv import load_dotenv
import os
import json

# Load environment variables from the .env file
load_dotenv()

# Get the API key and base URL from environment variables
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
ENDPOINT_TEAMS = os.getenv("ENDPOINT_TEAMS")  # Get the teams endpoint

# Construct the full URL with the API key
url_teams = f"{BASE_URL}{ENDPOINT_TEAMS}?api_key={API_KEY}"

# Set the headers for the request
headers = {"accept": "application/json"}

# Path to the teams data JSON file
json_file_path = "data/teams_data.json"

# Check if the old JSON file exists and delete it
if os.path.exists(json_file_path):
    os.remove(json_file_path)
    print(f"Old JSON file '{json_file_path}' deleted.")

# Make the GET request for teams
response_teams = requests.get(url_teams, headers=headers)

# Check if the response was successful
if response_teams.status_code == 200:
    # Parse the JSON response
    try:
        teams_data = response_teams.json()
        teams = teams_data.get('teams', [])
    except ValueError as e:
        print(f"Error parsing JSON: {e}")
        teams = []

    # Set of markets corresponding to NBA teams (U.S. and Canada)
    nba_markets = {
        "Atlanta", "Boston", "Brooklyn", "Charlotte", "Chicago",
        "Cleveland", "Dallas", "Denver", "Detroit", "Golden State",
        "Houston", "Indiana", "Los Angeles", "Memphis", "Miami",
        "Milwaukee", "Minnesota", "New Orleans", "New York", 
        "Oklahoma City", "Orlando", "Philadelphia", "Phoenix", 
        "Portland", "Sacramento", "San Antonio", "Toronto", "Utah", "Washington"
    }

    # Filter teams to only keep NBA teams based on the market value
    nba_teams = [team for team in teams if team.get('market') in nba_markets]

    # Prepare data structure for saving
    teams_info = {"teams": []}

    for team in nba_teams:
        team_info = {
            "id": team.get("id", "Unknown"),  # Include the team ID
            "name": team.get("name", "Unknown"),
            "market": team.get("market", "Unknown"),
            "alias": team.get("alias", "Unknown"),
            "additional_info": {}  # Placeholder for future performance stats
        }
        teams_info["teams"].append(team_info)

    # Save the team data to a new JSON file in the data directory
    with open(json_file_path, "w") as json_file:
        json.dump(teams_info, json_file, indent=4)

    print(f"Team data saved to '{json_file_path}'.")

else:
    print(f"Failed to fetch teams. Status code: {response_teams.status_code}")
