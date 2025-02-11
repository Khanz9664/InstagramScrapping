import random
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Instagram Credentials (Now stored in .env)
USERNAME = os.getenv("INSTAGRAM_USERNAME")
PASSWORD = os.getenv("INSTAGRAM_PASSWORD")

# Proxy Settings
PROXY = os.getenv("PROXY")

# Scraping Parameters
TARGET_USERNAMES = ["virat.kohli", "instagram"]  # List of usernames to scrape
POST_LIMIT = 5  # Number of posts per profile

# User-Agent Rotation
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
]

def get_random_user_agent():
    return random.choice(USER_AGENTS)
