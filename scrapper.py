from playwright.sync_api import sync_playwright
from config import TARGET_USERNAMES
from anti_detect import apply_anti_detection
import logging
import time

logger = logging.getLogger(__name__)

def scrape_profile(page, username):
    try:
        logger.info(f"🔍 Navigating to {username}'s profile")
        page.goto(f"https://www.instagram.com/{username}/", timeout=60000)
        
        # Wait for critical elements to load
        page.wait_for_selector("header section", timeout=30000)
        time.sleep(2)  # Additional buffer for JS execution

        # Extract profile name using official class names
        name_element = page.locator("h1._ap3a._aaco._aacu._aacx._aad6._aade").first
        name = name_element.inner_text() if name_element.count() else "N/A"

        # Extract bio using specific class combination
        bio_element = page.locator("div._aacl._aaco._aacu._aacx._aad6._aade").first
        bio = bio_element.inner_text() if bio_element.count() else "N/A"

        # Extract stats using XPath for better reliability
        stats = {
            "posts": page.locator("//header//ul/li[1]//span//span").first.inner_text(),
            "followers": page.locator("//header//ul/li[2]//span//span").first.inner_text(),
            "following": page.locator("//header//ul/li[3]//span//span").first.inner_text()
        }

        profile_data = {
            "Username": username,
            "Name": name,
            "Bio": bio,
            "Posts": stats.get("posts", "N/A"),
            "Followers": stats.get("followers", "N/A"),
            "Following": stats.get("following", "N/A")
        }

        logger.info(f"✅ Successfully scraped {username}")
        return profile_data
    except Exception as e:
        logger.error(f"❌ Error scraping {username}: {str(e)}")
        return None

def scrape_instagram_profile(username, context):
    try:
        page = context.new_page()
        apply_anti_detection(page)
        return scrape_profile(page, username)
    except Exception as e:
        logger.error(f"❌ Browser error: {str(e)}")
        return None
    finally:
        page.close()