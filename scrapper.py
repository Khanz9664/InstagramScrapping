from playwright.sync_api import sync_playwright
from config import TARGET_USERNAMES, get_random_user_agent
import json
import time

def scrape_instagram_profile(username):
    with sync_playwright() as p:
        print("Launching browser...")
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state="session.json")
        page = context.new_page()

        # Open User Profile
        url = f"https://www.instagram.com/{username}/"
        print(f"Navigating to {url}")
        page.goto(url)
        time.sleep(5)

        # Extract Profile Data
        try:
            print(" Extracting profile details...")
            elements = page.locator("header section div").all_inner_texts()
            name = elements[1] if len(elements) > 1 else "N/A"
            bio = elements[18] if len(elements) > 18 else "N/A"
            posts = elements[14] if len(elements) > 14 else "N/A"
            followers = elements[15] if len(elements) > 15 else "N/A"
            following = elements[16] if len(elements) > 16 else "N/A"


            profile_data = {
                "Name": name,
                "Bio": bio,
                "Posts": posts,
                "Followers": followers,
                "Following": following
            }

            print("Successfully extracted profile details!")
            print(json.dumps(profile_data, indent=4))  

        except Exception as e:
            print(f" Error extracting profile: {e}")
        
        for _ in range(5):
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(3)

        posts = page.locator("a.x1i10hfl").all()  
        # posts = page.locator("article a[href]").all()
        post_links = [post.get_attribute("href") for post in posts if post.get_attribute("href")]
        
        if not post_links:
            print("No posts found.")
            browser.close()
            return []

        post_data=[]

        for link in post_links[:5]: 
            try:
                page.goto(f"https://www.instagram.com{link}",   timeout=60000)
                time.sleep(3)

        
                try:
                    caption_element = page.locator("h1").first
                    caption = caption_element.inner_text() if caption_element else "No Caption"
                except:
                    caption = "No Caption"

                try:
                    likes_element = page.locator("span[role='button']").first
                    likes = likes_element.inner_text() if likes_element else "Likes not found"
                except:
                    likes = "Likes not found"

                try:
                    likes_element = page.locator("span[role='button']").first
                    likes = likes_element.inner_text() if likes_element else "Likes not found"
                except:
                    likes = "Likes not found"

                try:
                    comments_elements = page.locator("ul li").all()
                    comments = [comment.inner_text() for comment in comments_elements[:5]]  # Limit to 5 comments
                except:
                    comments = []

                hashtags = [word for word in caption.split() if word.startswith("#")]
                
                try:
                    image_element = page.locator("article img").first
                    image_url = image_element.get_attribute("src") if image_element else "No Image"
                except:
                    image_url = "No Image"
                    
                post_data.append({
                    "post_url": f"https://www.instagram.com{link}",
                    "caption": caption,
                    "likes": likes,
                    "comments": comments,
                    "hashtags": hashtags,
                    "image_url": image_url
                })
            except Exception as e:
                print(f"Error scraping {link}: {e}")
        # Close Browser
        browser.close()
        print("🚀 Browser closed.")
        return post_data

# Run Scraper
if __name__ == "__main__":
    username = "virat.kohli"  # Change to any username you want to scrape
    data=scrape_instagram_profile(username)
    for post in data:
        print(post)
