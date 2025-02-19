from playwright.sync_api import sync_playwright
from scrapper import scrape_instagram_profile
from data_handler import save_to_excel
from anti_detect import apply_anti_detection
from config import (
    TARGET_USERNAMES,
    BROWSER_CONFIG,
    VIEWPORT_CONFIG,
    get_random_user_agent
)
import random

def main():
    print("🚀 Starting Instagram Scraper (No Login Required)...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(**BROWSER_CONFIG)
        context = browser.new_context(
            user_agent=get_random_user_agent(),
            viewport=random.choice(VIEWPORT_CONFIG['presets'])
        )
        
        page = context.new_page()
        apply_anti_detection(page)  # Strengthened anti-detection
        
        scraped_data = []
        for username in TARGET_USERNAMES:
            print(f"🔍 Scraping profile: {username}")
            if data := scrape_instagram_profile(username, context):
                scraped_data.append(data)
        
        if scraped_data:
            save_to_excel(scraped_data)
            print(f"✅ Saved {len(scraped_data)} profiles")
        
        browser.close()

if __name__ == "__main__":
    main()

