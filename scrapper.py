import json
from playwright.sync_api import sync_playwright
from config import TARGET_USERNAMES
from anti_detect import apply_anti_detection
import logging
import time

logger = logging.getLogger(__name__)

def scrape_profile(page, username):
    # Open User Profile
    url = f"https://www.instagram.com/{username}/"
    print(f"Navigating to {url}")
    page.goto(url)
    time.sleep(5)

    # Extract Profile Data  
    try:
        print("Extracting profile details...")
        
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
        print(f"Error extracting profile: {e}")

    # Scroll to load more posts
    previous_height = page.evaluate("document.body.scrollHeight")
    for _ in range(5):
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(3)

        new_height = page.evaluate("document.body.scrollHeight")
        if new_height == previous_height:
            break
        previous_height = new_height

    posts = page.locator("article a").all()
    print(f"Found {len(posts)} links on the page")

    post_links = [
        f"https://www.instagram.com{post.get_attribute('href')}" 
        for post in posts 
        if post.get_attribute("href") and "/p/" in post.get_attribute("href")
    ]

    if not post_links:
        print("No posts found.")
        return []

    post_data = []

    for link in post_links[:5]:
        try:
            page.goto(link, timeout=60000)
            time.sleep(3)

            # Clean caption (remove hashtags)
            try:
                caption_element = page.locator("div.xt0psk2 h1").first
                raw_caption = caption_element.inner_text() if caption_element else ""
                caption = ' '.join([word for word in raw_caption.split() if not word.startswith('#')])
            except:
                caption = "No Caption"

            # Clean likes (convert to integer)
            try:
                likes_element = page.locator("section span:has-text('likes')").first
                raw_likes = likes_element.inner_text() if likes_element else "0"
                likes = int(raw_likes.replace(',', '').split()[0]) if 'likes' in raw_likes else 0
            except:
                likes = 0

            # Clean comments
            page.wait_for_selector("ul li", timeout=10000)
            comments = []
            try:
               comment_elements = page.locator("ul li").all()
               comm_count=len(comment_elements)
               print(f"The comments count are:{comm_count}")
               for comment in comment_elements[:20]:  
                  try:
                        username_element = comment.locator("h3 a").first()
                        username = username_element.inner_text().strip() if username_element else             "Unknown"
            
                        # Extract comment text
                        comment_text_element = comment.locator("span").first()
                        comment_text = comment_text_element.inner_text().strip() if comment_text_element else ""

                        # Ensure valid comment data
                        if comment_text and not comment_text.startswith(("Reply", "#", "@")):
                         comments.append({"username": username, "comment": comment_text})
                  except Exception as inner_e:
                        print(f"Error extracting a comment: {inner_e}")

               print("Extracted Comments:", comments)
            except Exception as e:
                print(f"Error extracting comments: {e}")
                comments = []

            try:
                comments_count_element = page.locator("div[role='button'] span").nth(1)

                if comments_count_element:
                    comments_count_text = comments_count_element.inner_text().strip()
                    print(f"Raw Comments Count Text: {comments_count_text}")  
        
                    # Extract only digits
                    comment_count_digits = ''.join(filter(str.isdigit, comments_count_text))

                    if comment_count_digits:
                        comments_count = int(comment_count_digits)
                        print(f"Total number of comments: {comments_count}")
                    else:
                        print("Comments count text is empty or non-numeric.")
                        comments_count = 0
                else:
                    print("Comments count element not found.")
                    comments_count = 0

            except Exception as e:
                print(f"Error extracting comments count: {e}")

            # Hashtags
            try:
                hashtags = []
                hashtag_links = page.locator("a[href*='/explore/tags/']").all()
                hashtags += [link.inner_text() for link in hashtag_links if link.inner_text().startswith('#')]
                hashtags = list(set(hashtags))
            except:
                hashtags = []

            # Image URL
            try:
                image_element = page.locator("article img").first
                image_url = image_element.get_attribute("src") if image_element else "No Image"
            except:
                image_url = "No Image"

            post_data.append({
                "post_url": link,
                "caption": caption,
                "likes": likes,
                "comments": comments[:20],
                "hashtags": hashtags,
                "image_url": image_url
            })

        except Exception as e:
            print(f"Error scraping {link}: {e}")

    return {
        "profile": profile_data,
        "posts": post_data
    }


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

