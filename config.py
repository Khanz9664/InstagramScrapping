import random
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Proxy Settings (if needed) - You can configure a proxy by setting the PROXY environment variable
PROXY = os.getenv("PROXY")

# Scraping Parameters
TARGET_USERNAMES = ["virat.kohli"]  # List of Instagram usernames to scrape
POST_LIMIT = 5  # Number of posts to scrape per profile

# Anti-detection Configuration
DELAY_CONFIG = {
    'range': (3, 7),  # The minimum and maximum delay (in seconds) between actions
    'type': 'normal'  # Type of delay distribution ('uniform' or 'normal')
}

# Browser Configuration for Playwright
BROWSER_CONFIG = {
    "headless": False,  # Whether to run the browser in headless mode (True = no UI, False = with UI)
    "slow_mo": 150,  # Slowdown factor for human-like delays between browser actions (milliseconds)
    "args": [
        "--disable-blink-features=AutomationControlled",  # Disable browser automation detection
        "--no-sandbox",  # Disable sandboxing (may be needed on some systems)
        "--disable-web-security"  # Disable certain web security features (for scraping purposes)
    ]
}

# Viewport Configuration: Simulate different screen sizes for scraping
VIEWPORT_CONFIG = {
    'presets': [
        {'width': 1920, 'height': 1080, 'device_scale_factor': 1},  # Full HD resolution
        {'width': 1366, 'height': 768, 'device_scale_factor': 1},   # HD resolution
        {'width': 1440, 'height': 900, 'device_scale_factor': 2}    # 900p resolution with higher DPI
    ]
}

# WebGL Spoofing: Mimic a real browser's hardware to avoid detection
WEBGL_SPOOFING = {
    'enabled': True,  # Enable or disable WebGL spoofing
    'vendor': 'Google Inc. (NVIDIA)',  # Fake WebGL vendor name
    'renderer': 'ANGLE (NVIDIA, NVIDIA GeForce RTX 3080 Direct3D11 vs_5_0 ps_5_0, D3D11)'  # Fake WebGL renderer string
}

# Browser Features: Disable features to prevent detection as a bot
BROWSER_FEATURES = {
    'disable_webdriver': True,  # Disable the webdriver flag (common bot detection method)
    'disable_webrtc': True,  # Disable WebRTC (prevents leaking IP address)
    'disable_geolocation': True,  # Disable geolocation API
    'disable_canvas_fingerprint': True,  # Disable canvas fingerprinting
    'disable_audio_fingerprint': True  # Disable audio fingerprinting
}

# User-Agent Rotation: A list of User-Agent strings for random rotation
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15"
]

# Function to get a random User-Agent from the list
def get_random_user_agent():
    return random.choice(USER_AGENTS)

# Instagram Selectors: CSS or XPath selectors to extract profile data
INSTAGRAM_SELECTORS = {
    "name": "h1._ap3a._aaco._aacu._aacx._aad6._aade",  # Selector for the profile name
    "bio": "div._aacl._aaco._aacu._aacx._aad6._aade",  # Selector for the profile bio
    "stats_xpath": "//header//ul/li[{}]//span//span"  # XPath to extract profile stats (e.g., followers, posts)
}

# File Output Configuration: Settings for how the data is saved to files
OUTPUT_CONFIG = {
    'default_filename': 'instagram_data',  # Default name for the output file
    'format': 'excel',  # Output file format: 'excel', 'csv', or 'json'
    'timestamp': True,  # Add a timestamp to the filename
    'profile_sheet': 'Profiles',  # Name of the sheet for profile data
    'posts_sheet': 'Posts'  # Name of the sheet for posts data
}

# File extensions based on the output format
FILE_EXTENSIONS = {
    'excel': '.xlsx',  # Excel file extension
    'csv': '.csv',  # CSV file extension
    'json': '.json'  # JSON file extension
}

# Anti-detection delay range (min, max) in seconds for simulating real user behavior
DELAY_RANGE = (2, 5)

# Human Typing Simulation: Simulate delays between keystrokes
HUMAN_TYPING = {
    "min_delay": 0.08,  # Minimum delay between keystrokes (seconds)
    "max_delay": 0.15  # Maximum delay between keystrokes (seconds)
}

