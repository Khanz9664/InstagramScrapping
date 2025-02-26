from playwright.sync_api import sync_playwright
from scrapper import scrape_instagram_profile
from data_handler import save_to_file  # Changed import for saving data
from anti_detect import apply_anti_detection
from config import (
    TARGET_USERNAMES,
    BROWSER_CONFIG,
    VIEWPORT_CONFIG,
    get_random_user_agent
)
import random

def main():
    # Print a message to indicate the scraper is starting
    print("🚀 Starting Instagram Scraper (No Login Required)...")
    
    # Launch Playwright and use a synchronous context
    with sync_playwright() as p:
        # Launch the Chromium browser with the specified configuration
        browser = p.chromium.launch(**BROWSER_CONFIG)
        
        # Create a new browser context with a random user-agent and viewport
        context = browser.new_context(
            user_agent=get_random_user_agent(),  # Get a random user-agent for this session
            viewport=random.choice(VIEWPORT_CONFIG['presets'])  # Pick a random viewport size
        )
        
        # Open a new page in the created context
        page = context.new_page()
        
        # Apply anti-detection measures to avoid bot detection
        apply_anti_detection(page)
        
        # Initialize lists to store the scraped profile and post data
        all_profiles = []
        all_posts = []
        
        # Loop through the target Instagram usernames
        for username in TARGET_USERNAMES:
            print(f"🔍 Scraping profile: {username}")
            
            # Call the function to scrape data from the Instagram profile
            # It returns a dictionary with 'profile' and 'posts' data
            if scraped_data := scrape_instagram_profile(username, context):
                
                # If profile data is found, append it to the all_profiles list
                if 'profile' in scraped_data:
                    all_profiles.append(scraped_data['profile'])
                
                # If post data is found, extend the all_posts list
                if 'posts' in scraped_data:
                    all_posts.extend(scraped_data['posts'])
        
        # Check if there is any data to save (either profiles or posts)
        if all_profiles or all_posts:
            # Save the scraped data to a file
            save_to_file(all_profiles, all_posts)  # Updated call for saving data
            # Print a message indicating how many profiles and posts were saved
            print(f"✅ Saved {len(all_profiles)} profiles and {len(all_posts)} posts")
        
        # Close the browser once the scraping process is done
        browser.close()

# The entry point of the script
if __name__ == "__main__":
    # Call the main function to start the scraping process
    main()

