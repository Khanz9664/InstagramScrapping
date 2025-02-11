import time
from playwright.sync_api import sync_playwright
from config import USERNAME, PASSWORD
from anti_detect import apply_anti_detection  # Add anti-detection

def login_instagram():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Apply anti-detection before login
        apply_anti_detection(page)
        
        page.goto("https://www.instagram.com/accounts/login/")
        page.wait_for_selector("input[name='username']", timeout=15000)
        
        page.fill("input[name='username']", USERNAME)
        page.fill("input[name='password']", PASSWORD)
        page.click("button[type='submit']")
        
        # Wait for navigation
        try:
            page.wait_for_url("**/accounts/login/**", timeout=7000, state="domcontentloaded")
        except:
            pass

        # Check login status
        if "/challenge/" in page.url:
            print("⚠️ Login requires verification!")
            browser.close()
            return False
        elif page.url == "https://www.instagram.com/" or "instagram.com" in page.url:
            print("✅ Successfully Logged In!")
            context.storage_state(path="session.json")
            browser.close()
            return True
        else:
            print("❌ Login Failed!")
            browser.close()
            return False