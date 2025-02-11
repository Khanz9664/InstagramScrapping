from playwright.sync_api import sync_playwright
from config import TARGET_USERNAMES, get_random_user_agent
import json
import time

def scrape_instagram_profile(username):
    with sync_playwright() as p:
        print("🚀 Launching browser...")
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state="session.json")
        page = context.new_page()

        # Open User Profile
        url = f"https://www.instagram.com/{username}/"
        print(f"🔍 Navigating to {url}")
        page.goto(url)
        time.sleep(5)

        # Extract Profile Data
        try:
            print("📊 Extracting profile details...")
            elements = page.locator("header section div").all_inner_texts()
            name = elements[1] if len(elements) > 1 else "N/A"
            bio = elements[18] if len(elements) > 18 else "N/A"
            posts = elements[14] if len(elements) > 14 else "N/A"
            followers = elements[15] if len(elements) > 15 else "N/A"
            following = elements[16] if len(elements) > 16 else "N/A"


            profile_data = {
                "Username": username,
                "Name": name,
                "Bio": bio,
                "Posts": posts,
                "Followers": followers,
                "Following": following
            }

            print("✅ Successfully extracted profile details!")
            print(json.dumps(profile_data, indent=4))  # Pretty-print output

        except Exception as e:
            print(f"❌ Error extracting profile: {e}")

        # Close Browser
        browser.close()
        print("🚀 Browser closed.")

# Run Scraper
if __name__ == "__main__":
    username = "virat.kohli"  # Change to any username you want to scrape
    scrape_instagram_profile(username)
