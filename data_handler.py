import pandas as pd
import logging
from datetime import datetime
from config import OUTPUT_CONFIG, FILE_EXTENSIONS
from typing import List, Dict

# Configure logging
logger = logging.getLogger(__name__)

def save_to_excel(data: List[Dict], filename: str = None) -> None:
    """
    Saves scraped Instagram data to file with multiple format support
    - Handles empty data scenarios
    - Supports Excel/CSV/JSON formats
    - Adds timestamp to filename
    - Includes proper error handling
    """
    try:
        if not data:
            logger.warning("⚠️ No data to save")
            return

        # Generate filename with timestamp if enabled
        if OUTPUT_CONFIG['timestamp']:
            base_name = filename or OUTPUT_CONFIG['default_filename']
            filename = f"{base_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        else:
            filename = filename or OUTPUT_CONFIG['default_filename']

        # Add file extension
        filename += FILE_EXTENSIONS.get(OUTPUT_CONFIG['format'], '.xlsx')

        # Create DataFrame with validation
        df = pd.DataFrame(data)
        
        # Save in specified format
        if OUTPUT_CONFIG['format'] == 'csv':
            df.to_csv(filename, index=False)
        elif OUTPUT_CONFIG['format'] == 'json':
            df.to_json(filename, orient='records')
        else:  # Default to Excel
            df.to_excel(filename, index=False, sheet_name=OUTPUT_CONFIG['sheet_name'])

        logger.info(f"✅ Successfully saved {len(data)} records to {filename}")
        
    except Exception as e:
        logger.error(f"❌ Failed to save data: {str(e)}")
        raise
