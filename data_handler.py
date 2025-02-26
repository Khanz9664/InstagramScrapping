import pandas as pd
import logging
from datetime import datetime
from config import OUTPUT_CONFIG, FILE_EXTENSIONS
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

def save_to_file(profiles: List[Dict], posts: List[Dict], filename: str = None) -> None:
    """
    Saves scraped data to files in Excel, CSV, and JSON formats.
    - Excel: Single file with two sheets (Profiles and Posts)
    - CSV: Separate files for profiles and posts
    - JSON: Separate files for profiles and posts
    """
    try:
        if not profiles and not posts:
            logger.warning("⚠️ No data to save")
            return

        # Generate base filename with timestamp if enabled
        base_name = filename or OUTPUT_CONFIG['default_filename']
        if OUTPUT_CONFIG['timestamp']:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            base_name = f"{base_name}_{timestamp}"

        # Save Excel: Single file with two sheets
        excel_filename = f"{base_name}.xlsx"
        with pd.ExcelWriter(excel_filename) as writer:
            if profiles:
                pd.DataFrame(profiles).to_excel(
                    writer, 
                    sheet_name=OUTPUT_CONFIG.get('profile_sheet', 'Profiles'), 
                    index=False
                )
            if posts:
                pd.DataFrame(posts).to_excel(
                    writer, 
                    sheet_name=OUTPUT_CONFIG.get('posts_sheet', 'Posts'), 
                    index=False
                )
        logger.info(f"✅ Saved data to Excel file: {excel_filename}")

        # Save CSV: Separate files for profiles and posts
        if profiles:
            profile_csv_filename = f"{base_name}_profiles.csv"
            pd.DataFrame(profiles).to_csv(profile_csv_filename, index=False)
            logger.info(f"✅ Saved profile data to CSV file: {profile_csv_filename}")
        if posts:
            post_csv_filename = f"{base_name}_posts.csv"
            pd.DataFrame(posts).to_csv(post_csv_filename, index=False)
            logger.info(f"✅ Saved post data to CSV file: {post_csv_filename}")

        # Save JSON: Separate files for profiles and posts
        if profiles:
            profile_json_filename = f"{base_name}_profiles.json"
            pd.DataFrame(profiles).to_json(profile_json_filename, orient='records')
            logger.info(f"✅ Saved profile data to JSON file: {profile_json_filename}")
        if posts:
            post_json_filename = f"{base_name}_posts.json"
            pd.DataFrame(posts).to_json(post_json_filename, orient='records')
            logger.info(f"✅ Saved post data to JSON file: {post_json_filename}")

    except Exception as e:
        logger.error(f"❌ Failed to save data: {str(e)}")
        raise

