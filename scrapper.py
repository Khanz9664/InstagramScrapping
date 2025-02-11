# from playwright.sync_api import sync_playwright
# import time
# import json
# from auth import load_cookies

# def scrape_instagram_profile(username):
#     with sync_playwright() as p:
#         print("🚀 Launching browser...")
#         browser = p.chromium.launch(headless=False)
#         context = browser.new_context(storage_state="session.json")
#         page = context.new_page()

#         # Load saved cookies for session
#         load_cookies(context)
        
#         # Open Instagram Profile
#         profile_url = f"https://www.instagram.com/{username}/"
#         print(f"🔍 Navigating to {profile_url}")
#         page.goto(profile_url)
#         time.sleep(5)

#         # Extract Profile Info
#         profile_data = {}
#         profile_data["username"] = username
#         profile_data["bio"] = page.locator("div.-vDIg span").inner_text()
#         profile_data["followers"] = page.locator("a[href*='followers']").inner_text()
#         profile_data["following"] = page.locator("a[href*='following']").inner_text()
#         profile_data["posts"] = page.locator("span.g47SY").inner_text()
        
#         # Extract Post Details
#         post_elements = page.locator("article div img").all()
#         post_links = [post.get_attribute("src") for post in post_elements[:5]]

#         profile_data["latest_posts"] = post_links

#         # Save Data
#         with open(f"{username}_profile.json", "w") as f:
#             json.dump(profile_data, f, indent=4)
        
#         print(f"✅ Data saved for {username}")
#         browser.close()

# # Run scraper for all target usernames
# for user in TARGET_USERNAMES:
#     scrape_instagram_profile(user)


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
    username = "instagram"  # Change to any username you want to scrape
    scrape_instagram_profile(username)
