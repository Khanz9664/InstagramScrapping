from playwright.sync_api import sync_playwright
from scrapper import scrape_instagram_profile
from data_handler import save_to_file  # Changed import
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
        apply_anti_detection(page)
        
        all_profiles = []
        all_posts = []
        for username in TARGET_USERNAMES:
            print(f"🔍 Scraping profile: {username}")
            if scraped_data := scrape_instagram_profile(username, context):
                if 'profile' in scraped_data:
                    all_profiles.append(scraped_data['profile'])
                if 'posts' in scraped_data:
                    all_posts.extend(scraped_data['posts'])
        
        if all_profiles or all_posts:
            save_to_file(all_profiles, all_posts)  # Updated call
            print(f"✅ Saved {len(all_profiles)} profiles and {len(all_posts)} posts")
        
        browser.close()

if __name__ == "__main__":
    main()
