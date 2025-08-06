# Configuration file for Cricket Analytics System
import os

# Data directories
DATA_DIR = "data"
SCRAPED_DATA_DIR = os.path.join(DATA_DIR, "scraped")
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")
OUTPUTS_DIR = os.path.join(DATA_DIR, "outputs")

# Create directories if they don't exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(SCRAPED_DATA_DIR, exist_ok=True)
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
os.makedirs(OUTPUTS_DIR, exist_ok=True)

# File paths
SCHEDULE_FILE = os.path.join(DATA_DIR, "schedule_2025.csv")
SQUADS_FILE = os.path.join(DATA_DIR, "squads_2025.csv")
VENUE_STATS_FILE = os.path.join(SCRAPED_DATA_DIR, "venue_stats.csv")
PLAYER_STATS_FILE = os.path.join(SCRAPED_DATA_DIR, "player_stats.csv")
TEAM_RATINGS_FILE = os.path.join(PROCESSED_DATA_DIR, "team_ratings.csv")
TOURNAMENT_PREDICTIONS_FILE = os.path.join(OUTPUTS_DIR, "tournament_predictions.csv")

# Venues mapping
VENUES = {
    "Lord's, London": "London Spirit Men",
    "Emirates Old Trafford, Manchester": "Manchester Originals Men", 
    "Headingley, Leeds": "Northern Superchargers Men",
    "Edgbaston, Birmingham": "Birmingham Phoenix Men",
    "Kennington Oval, London": "Oval Invincibles Men",
    "The Rose Bowl, Southampton": "Southern Brave Men",
    "Trent Bridge, Nottingham": "Trent Rockets Men",
    "Sophia Gardens, Cardiff": "Welsh Fire Men"
}

# ESPN CricInfo base URLs
CRICINFO_BASE_URL = "https://www.espncricinfo.com"
CRICINFO_HUNDRED_URL = "https://www.espncricinfo.com/series/the-hundred-mens-2024-1417778"