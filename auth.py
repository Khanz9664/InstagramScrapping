import time
from playwright.sync_api import sync_playwright
from config import USERNAME, PASSWORD

def login_instagram():
    with sync_playwright() as p:
        # Launch Browser (Headless=False for debugging)
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Go to Instagram Login Page
        page.goto("https://www.instagram.com/accounts/login/")
        time.sleep(5)  # Wait for page to load

        # Enter Username & Password
        page.fill("input[name='username']", USERNAME)
        page.fill("input[name='password']", PASSWORD)

        # Click Login Button
        page.click("button[type='submit']")
        time.sleep(5)  # Wait for login to process

        # Check if login was successful
        if "/challenge/" in page.url:
            print("⚠️ Login requires verification!")
        elif "instagram.com" in page.url:
            print("✅ Successfully Logged In!")
        else:
            print("❌ Login Failed!")

        # Save Cookies for Future Sessions
        context.storage_state(path="session.json")
        print("✅ Session saved to session.json")

        # Close Browser
        browser.close()

if __name__ == "__main__":
    login_instagram()
