import json
from playwright.sync_api import sync_playwright
from config import TARGET_USERNAMES
from anti_detect import apply_anti_detection
import logging
import time

# def scrape_instagram_profile(username):
#     with sync_playwright() as p:
#         print("Launching browser...")
#         browser = p.chromium.launch(headless=False)
#         context = browser.new_context(storage_state="session.json")
#         page = context.new_page()

#         # Open User Profile
#         url = f"https://www.instagram.com/{username}/"
#         print(f"Navigating to {url}")
#         page.goto(url)
#         time.sleep(5)

#         # Extract Profile Data
#         try:
#             print(" Extracting profile details...")
#             elements = page.locator("header section div").all_inner_texts()
#             name = elements[1] if len(elements) > 1 else "N/A"
#             bio = elements[18] if len(elements) > 18 else "N/A"
#             posts = elements[14] if len(elements) > 14 else "N/A"
#             followers = elements[15] if len(elements) > 15 else "N/A"
#             following = elements[16] if len(elements) > 16 else "N/A"


#             profile_data = {
#                 "Name": name,
#                 "Bio": bio,
#                 "Posts": posts,
#                 "Followers": followers,
#                 "Following": following
#             }

#             print("Successfully extracted profile details!")
#             print(json.dumps(profile_data, indent=4))  

#         except Exception as e:
#             print(f" Error extracting profile: {e}")
        
#         for _ in range(5):
#             page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
#             time.sleep(3)

#         posts = page.locator("a.x1i10hfl").all()  
#         # posts = page.locator("article a[href]").all()
#         post_links = [post.get_attribute("href") for post in posts if post.get_attribute("href")]
        
#         if not post_links:
#             print("No posts found.")
#             browser.close()
#             return []

#         post_data=[]

#         for link in post_links[:5]: 
#             try:
#                 page.goto(f"https://www.instagram.com{link}",   timeout=60000)
#                 time.sleep(3)

        
#                 try:
#                     caption_element = page.locator("div.xt0psk2 h1").first
#                     caption = caption_element.inner_text() if caption_element else "No Caption"
#                 except:
#                     caption = "No Caption"

#                 try:
#                     likes_element = page.locator("span[role='button']").first
#                     likes = likes_element.inner_text() if likes_element else "Likes not found"
#                 except:
#                     likes = "Likes not found"

#                 try:
#                     comments_elements = page.locator("ul li").all()
#                     comments = [comment.inner_text() for comment in comments_elements[:5]]  # Limit to 5 comments
#                 except:
#                     comments = []

#                 try:
#                     hashtags_elements = page.locator("a[href*='/explore/tags/']").all()
#                     hashtags = [hashtag.inner_text() for hashtag in hashtags_elements if hashtag.inner_text()]
#                 except:
#                     hashtags = []
                
#                 try:
#                     image_element = page.locator("article img").first
#                     image_url = image_element.get_attribute("src") if image_element else "No Image"
#                 except:
#                     image_url = "No Image"
                    
#                 post_data.append({
#                     "post_url": f"https://www.instagram.com{link}",
#                     "caption": caption,
#                     "likes": likes,
#                     "comments": comments,
#                     "hashtags": hashtags,
#                     "image_url": image_url
#                 })
#             except Exception as e:
#                 print(f"Error scraping {link}: {e}")
#         # Close Browser
#         browser.close()
#         print("🚀 Browser closed.")
#         return post_data

# # Run Scraper
# if __name__ == "__main__":
#     username = "virat.kohli"  # Change to any username you want to scrape
#     data=scrape_instagram_profile(username)
#     for post in data:
#         print(post)

logger = logging.getLogger(__name__)

def scrape_profile(page, username):
    #  Open User Profile
        url = f"https://www.instagram.com/{username}/"
        print(f"Navigating to {url}")
        page.goto(url)
        time.sleep(5)

        # Extract Profile Data  
        try:
            print(" Extracting profile details...")
            # elements = page.locator("header section div").all_inner_texts()
            # name = elements[1] if len(elements) > 1 else "N/A"
            # bio = elements[18] if len(elements) > 18 else "N/A"
            # posts = elements[14] if len(elements) > 14 else "N/A"
            # followers = elements[15] if len(elements) > 15 else "N/A"
            # following = elements[16] if len(elements) > 16 else "N/A"
            name_element = page.locator("header h2").first
            name = name_element.inner_text() if name_element else "N/A"

            bio_element = page.locator("header section div").nth(1)
            bio = bio_element.inner_text() if bio_element else "N/A"

            stats_elements = page.locator("header section ul li").all()
            posts = stats_elements[0].inner_text() if len(stats_elements) > 0 else "N/A"
            followers = stats_elements[1].inner_text() if len(stats_elements) > 1 else "N/A"
            following = stats_elements[2].inner_text() if len(stats_elements) > 2 else "N/A"

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
        
        previous_height = page.evaluate("document.body.scrollHeight")
        for _ in range(5):
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(3)
            
            new_height = page.evaluate("document.body.scrollHeight")
            if new_height == previous_height:
              break
            previous_height = new_height

        # posts = page.locator("a.x1i10hfl").all()  
        posts = page.locator("a").all()
        print(f"Found {len(posts)} links on the page")
        # Extract only Instagram post links (filtering by "/p/")
        post_links = [
        post.get_attribute("href") 
        for post in posts 
        if post.get_attribute("href") and "/p/" in post.get_attribute("href")]

        if not post_links:
          print("No posts found.")
          return []

        post_data=[]

        for link in post_links[:5]: 
            try:
                page.goto(link, timeout=60000)
                time.sleep(3)

        
                try:
                    caption_element = page.locator("div.xt0psk2 h1").first
                    caption = caption_element.inner_text() if caption_element else "No Caption"
                except:
                    caption = "No Caption"

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

                try:
                    hashtags_elements = page.locator("a[href*='/explore/tags/']").all()
                    hashtags = [hashtag.inner_text() for hashtag in hashtags_elements if hashtag.inner_text()]
                except:
                    hashtags = []
                
                try:
                    image_element = page.locator("article img").first
                    image_url = image_element.get_attribute("src") if image_element else "No Image"
                except:
                    image_url = "No Image"
                    
                post_data.append({
                    "post_url": link,
                    "caption": caption,
                    "likes": likes,
                    "comments": comments,
                    "hashtags": hashtags,
                    "image_url": image_url
                })
            except Exception as e:
                print(f"Error scraping {link}: {e}")
        # Close Browser
        print("🚀 Browser closed")
        return post_data

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
