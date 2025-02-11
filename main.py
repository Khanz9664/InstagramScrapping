from auth import login_instagram
from scrapper import scrape_instagram_profile
from data_handler import save_to_excel
from config import TARGET_USERNAMES
from playwright.sync_api import sync_playwright

def main():
    print("🚀 Starting Instagram Scraper...")
    
    if not login_instagram():
        print("❌ Aborting due to login failure")
        return

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state="session.json")
        
        scraped_data = []
        for username in TARGET_USERNAMES:
            print(f"🔍 Scraping profile: {username}")
            # Pass both username AND context to the function
            data = scrape_instagram_profile(username, context)
            if data:
                scraped_data.append(data)
        
        browser.close()
        
        if scraped_data:
            save_to_excel(scraped_data)
            print("✅ Data saved successfully")
        else:
            print("⚠️ No data collected")

if __name__ == "__main__":
    main()