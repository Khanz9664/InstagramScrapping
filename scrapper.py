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

    # Extract only Instagram post links (filtering by "/p/")
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
            try:
                comments = []
                comments_elements = page.locator("ul li").all()
                for comment in comments_elements[:20]:  # Get top 20 comments
                    raw_comment = comment.inner_text()
                    cleaned = ' '.join([
                        part.strip()
                        for part in raw_comment.split('\n')[0].split()
                        if not part.startswith(('#', '@')) and not part.isdigit()
                    ]).replace('Reply', '').strip()

                    if cleaned and len(cleaned) > 3:
                        comments.append(cleaned)
            except:
                comments = []

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
                "comments": comments[:20],  # Ensure max 20 comments
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

