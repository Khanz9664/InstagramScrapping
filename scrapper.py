import json
from playwright.sync_api import sync_playwright
from config import TARGET_USERNAMES
from anti_detect import apply_anti_detection
import logging
import time
import re

# Setting up the logger for the script
logger = logging.getLogger(__name__)

# Function to convert Instagram number strings (followers, posts, etc.) into integer values
def convert_insta_number(num_str):
    try:
        # Cleaning the number string by removing irrelevant words like 'followers', 'following', and 'posts'
        clean = num_str.lower().replace('followers', '').replace('following', '').replace('posts', '').strip()
        
        # Convert numbers with 'm' for millions or 'k' for thousands into actual integers
        if 'm' in clean:
            return int(float(clean.replace('m', '')) * 1_000_000)
        if 'k' in clean:
            return int(float(clean.replace('k', '')) * 1_000)
        
        # Return the number after removing commas
        return int(clean.replace(',', ''))
    except:
        # In case of any error, return the original string
        return num_str

# Function to scrape Instagram profile data
def scrape_profile(page, username):
    url = f"https://www.instagram.com/{username}/"
    print(f"Navigating to {url}")
    page.goto(url)  # Go to the Instagram profile URL
    page.wait_for_timeout(5000)  # Wait for page to load

    popup_closed = False
    try:
        # Attempt to close any login popups
        close_button = page.locator('svg[aria-label="Close"]').first
        if close_button.is_visible(timeout=5000):
            close_button.click()  # Close the popup if found
            print("Closed login popup via SVG close button")
            popup_closed = True
            page.wait_for_timeout(2000)  # Wait after closing the popup
    except Exception as e:
        print("Popup close error:", e)

    # Extract profile details such as name, bio, and stats
    try:
        print("Extracting profile details...")
        name_element = page.locator("header h2").first
        name = name_element.inner_text() if name_element else "N/A"
        
        # Fallback selector for bio
        bio_element = page.locator("header section div").nth(1)
        bio = bio_element.inner_text() if bio_element else "N/A"
        
        # Extract stats (posts, followers, following)
        stats_elements = page.locator("header section ul li").all()
        posts = convert_insta_number(stats_elements[0].inner_text()) if len(stats_elements) > 0 else "N/A"
        followers = convert_insta_number(stats_elements[1].inner_text()) if len(stats_elements) > 1 else "N/A"
        following = convert_insta_number(stats_elements[2].inner_text()) if len(stats_elements) > 2 else "N/A"

        # Store extracted data in a dictionary
        profile_data = {
            "Name": name,
            "Bio": bio,
            "Posts": posts,
            "Followers": followers,
            "Following": following
        }
        print("Successfully extracted profile details!")
        print(json.dumps(profile_data, indent=4))  # Print profile data in JSON format
    except Exception as e:
        print(f"Error extracting profile: {e}")

    # Parameters for post extraction (desired post count and scroll attempts)
    desired_post_count = 20
    max_scroll_attempts = 3
    scroll_attempts = 0

    # Scroll and try to find enough posts (maximum attempts)
    while scroll_attempts < max_scroll_attempts:
        post_elements = page.locator("a[href*='/p/'], a[href*='/reel/']").all()
        current_count = len(post_elements)
        print(f"Scrolling attempt {scroll_attempts+1}: found {current_count} links")
        if current_count >= desired_post_count:
            break
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")  # Scroll to the bottom of the page
        page.wait_for_timeout(5000)  # Wait for the page to load more posts
        scroll_attempts += 1

    try:
        # Click 'Show more' button if it exists
        show_more_button = page.locator("button:has-text('more')")
        if show_more_button.is_visible(timeout=3000):
            print("Found 'Show more' button. Clicking it...")
            show_more_button.click()
            page.wait_for_timeout(5000)
    except Exception as e:
        print("No 'Show more' button found or error:", e)

    # Final scroll attempt
    scroll_attempts = 0
    while scroll_attempts < max_scroll_attempts:
        post_elements = page.locator("a[href*='/p/'], a[href*='/reel/']").all()
        current_count = len(post_elements)
        print(f"Scrolling attempt {scroll_attempts+1}: found {current_count} links")
        if current_count >= desired_post_count:
            break
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(5000)
        scroll_attempts += 1
        
    # Get the final count of post links
    post_elements = page.locator("a[href*='/p/'], a[href*='/reel/']").all()
    final_count = len(post_elements)
    print(f"Final count of links on the page: {final_count}")

    # Filter the post links and construct the full URL for each post
    post_links = [post.get_attribute('href') for post in post_elements if post.get_attribute('href')]
    post_links = [f"https://www.instagram.com{link}" if link.startswith('/') else link for link in post_links]
    print(f"Filtered to {len(post_links)} post links")

    if not post_links:
        print("No posts found.")
        return []  # Return empty if no posts are found

    post_data = []

    # Scrape data for each post
    for link in post_links[:desired_post_count]:
        try:
            print(f"Scraping post: {link}")
            page.goto(link, timeout=60000)  # Navigate to each post
            page.wait_for_timeout(5000)  # Wait for the page to load

            # Extract post caption, stripping out hashtags
            try:
                caption_element = page.locator("div.xt0psk2 h1").first
                raw_caption = caption_element.inner_text() if caption_element else ""
                caption = ' '.join(word for word in raw_caption.split() if not word.startswith('#'))
            except Exception as e:
                print(f"Caption error for {link}: {e}")
                caption = "No Caption"

            # Extract likes count for the post
            try:
                likes_element = page.locator("section span:has-text('likes')").first
                raw_likes = likes_element.inner_text() if likes_element else "0"
                likes = int(raw_likes.replace(',', '').split()[0]) if 'likes' in raw_likes else 0
            except Exception as e:
                print(f"Likes error for {link}: {e}")
                likes = 0

            # Extract commenters (top 20)
            try:
                commenters = []
                comments_elements = page.locator("ul li").all()
                for comment in comments_elements[:]:
                    raw_comment = comment.inner_text()
                    cleaned = ' '.join(
                        part.strip()
                        for part in raw_comment.split('\n')[0].split()
                        if not part.startswith(('#')) and not part.isdigit()
                    ).replace('Reply', ' ').strip()
                    if cleaned and len(cleaned) > 3:
                        commenters.append(cleaned)
            except Exception as e:
                print(f"Commenters error for {link}: {e}")
                commenters = []

            # Extract hashtags used in the post
            try:
                hashtags = []
                hashtag_links = page.locator("a[href*='/explore/tags/']").all()
                hashtags += [link.inner_text() for link in hashtag_links if link.inner_text().startswith('#')]
                hashtags = list(set(hashtags))  # Remove duplicates
            except Exception as e:
                print(f"Hashtags error for {link}: {e}")
                hashtags = []

            # Extract image URL from the post
            try:
                image_element = page.locator("article img").first
                image_url = image_element.get_attribute("src") if image_element else "No Image"
            except Exception as e:
                print(f"Image URL error for {link}: {e}")
                image_url = "No Image"

            # Append the post data to the list
            post_data.append({
                "post_url": link,
                "caption": caption,
                "likes": likes,
                "commenters": commenters[:30],
                "hashtags": hashtags,
                "image_url": image_url
            })
        except Exception as e:
            print(f"Error scraping {link}: {e}")

    return {
        "profile": profile_data,
        "posts": post_data
    }

# Function to scrape an Instagram profile by username using the provided context
def scrape_instagram_profile(username, context):
    try:
        # Create a new page in the browser context and apply anti-detection techniques
        page = context.new_page()
        apply_anti_detection(page)
        return scrape_profile(page, username)  # Scrape the profile using the page
    except Exception as e:
        logger.error(f"❌ Browser error: {str(e)}")
        return None  # Return None in case of any error
    finally:
        page.close()  # Ensure the page is closed after scraping

