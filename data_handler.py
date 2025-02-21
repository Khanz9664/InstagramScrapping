import pandas as pd
import logging
from datetime import datetime
from config import OUTPUT_CONFIG, FILE_EXTENSIONS
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

def save_to_file(profiles: List[Dict], posts: List[Dict], filename: str = None) -> None:
    """
    Saves scraped data to file with separate storage for profiles and posts
    - Excel: Single file with two sheets
    - CSV/JSON: Separate files for profiles and posts
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

        # Handle different file formats
        file_format = OUTPUT_CONFIG['format']
        extension = FILE_EXTENSIONS.get(file_format, '.xlsx')

        if file_format == 'excel':
            filename = f"{base_name}{extension}"
            with pd.ExcelWriter(filename) as writer:
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
            logger.info(f"✅ Saved data to Excel file: {filename}")

        elif file_format in ['csv', 'json']:
            # Save as separate files for profiles and posts
            if profiles:
                profile_filename = f"{base_name}_profiles{extension}"
                df_profile = pd.DataFrame(profiles)
                if file_format == 'csv':
                    df_profile.to_csv(profile_filename, index=False)
                else:
                    df_profile.to_json(profile_filename, orient='records')
                logger.info(f"✅ Saved profile data to {profile_filename}")

            if posts:
                post_filename = f"{base_name}_posts{extension}"
                df_post = pd.DataFrame(posts)
                if file_format == 'csv':
                    df_post.to_csv(post_filename, index=False)
                else:
                    df_post.to_json(post_filename, orient='records')
                logger.info(f"✅ Saved post data to {post_filename}")

        else:
            logger.error(f"❌ Unsupported file format: {file_format}")
            raise ValueError(f"Unsupported format: {file_format}")

    except Exception as e:
        logger.error(f"❌ Failed to save data: {str(e)}")
        raise
