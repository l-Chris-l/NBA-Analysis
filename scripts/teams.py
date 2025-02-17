import requests
from dotenv import load_dotenv
import os

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

# Make the GET request for teams
response_teams = requests.get(url_teams, headers=headers)

# Print the responses
print("Teams Response:", response_teams.text)
