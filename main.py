from flask import Flask, request, jsonify, send_from_directory
from playwright.sync_api import sync_playwright
from scrapper import scrape_instagram_profile
from data_handler import save_to_file
from anti_detect import apply_anti_detection
from config import BROWSER_CONFIG, VIEWPORT_CONFIG, get_random_user_agent
import random
import logging
import os

# Initialize Flask application
app = Flask(__name__, static_folder='static', static_url_path='')

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.ERROR)

# Serve the index.html file
@app.route('/')
def index():
    return app.send_static_file('index.html')

# Scrape data from Instagram profile
@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.get_json()
    username = data.get('username')

    if not username:
        return jsonify({'error': 'Username is required'}), 400

    logger.info(f"🚀 Scraping Instagram profile: {username}")

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(**BROWSER_CONFIG)
            context = browser.new_context(
                user_agent=get_random_user_agent(),
                viewport=random.choice(VIEWPORT_CONFIG['presets'])
            )
            page = context.new_page()
            apply_anti_detection(page)

            scraped_data = scrape_instagram_profile(username, context)

            browser.close()

        if not scraped_data:
            return jsonify({'error': 'Failed to scrape data'}), 500

        # Save the scraped data to files
        try:
            save_to_file([scraped_data['profile']], scraped_data['posts'], filename=username)
            logger.info(f"✅ Saved data for {username}")
        except Exception as e:
            logger.error(f"❌ Failed to save data for {username}: {str(e)}")
            # Continue to return data even if saving fails

        return jsonify(scraped_data)

    except Exception as e:
        logger.error(f"Error occurred while scraping {username}: {str(e)}")
        return jsonify({'error': 'An error occurred while processing your request'}), 500

# Serve the favicon.ico file
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

# General error handler
@app.errorhandler(Exception)
def handle_exception(error):
    logger.error(f"An unexpected error occurred: {str(error)}")
    return jsonify({'error': 'An unexpected error occurred'}), 500

# Specific error handler for 400 Bad Request
@app.errorhandler(400)
def handle_bad_request(error):
    return jsonify({'error': 'Bad request: ' + str(error)}), 400

# Remove the existing __main__ block and replace with:
application = app  # Required for Gunicorn compatibility

if __name__ == "__main__":
    # This block should ONLY be used for local development
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)  # Always debug=False in container
