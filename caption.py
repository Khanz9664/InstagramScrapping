import os
import instaloader
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

USERNAME = "hehemew3"
PASSWORD = os.getenv("PASSWORD")

L = instaloader.Instaloader()

def login():
    """Authenticate and load session"""
    L.context._session.headers.update(
        {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    )

    try:
        L.load_session_from_file(USERNAME)
        print("[✅] Session loaded!")
    except FileNotFoundError:
        print("[⚠️] Session not found. Logging in manually...")
        L.login(USERNAME, PASSWORD)
        L.save_session_to_file()
        print("[🔒] Session saved!")



def fetch_post_details(post_shortcode):
    """Fetch likes & comments from a post"""
    try:
        post = instaloader.Post.from_shortcode(L.context, post_shortcode)
        print(f"\n[📌] Post Details ({post_shortcode}):")
        print(f"🔹 Likes: {post.likes}")
        print(f"🔹 Comments Count: {post.comments}")
        profile = instaloader.Profile.from_username(L.context, USERNAME)
        print(f"[✅] Logged in as: {profile.username}")

        comments = []
        for comment in post.get_comments():
          print(f"💬 {comment.owner.username}: {comment.text}")

    except instaloader.exceptions.InstaloaderException as e:
        print(f"[❌] Error fetching post: {e}")

if __name__ == "__main__":
    login()
    fetch_post_details("DFpgUj3tNIq") 
