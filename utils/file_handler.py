"""
File handling utilities
"""
import os
from pathlib import Path
import aiohttp
from utils.logger import get_logger

# Get logger
logger = get_logger(__name__)

# Create temp directory if it doesn't exist
temp_dir = Path(__file__).parent.parent / 'temp'
temp_dir.mkdir(exist_ok=True)

async def download_file(file_path: str, output_path: str) -> str:
    """
    Download a file from Telegram's servers
    
    Args:
        file_path: Telegram file path
        output_path: Path where the file should be saved
        
    Returns:
        Path to the downloaded file
    """
    try:
        # Full Telegram file URL
        url = f"https://api.telegram.org/file/bot{os.getenv('TELEGRAM_BOT_TOKEN')}/{file_path}"
        
        logger.info(f"Downloading file from {url} to {output_path}")
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    with open(output_path, 'wb') as f:
                        f.write(await response.read())
                    logger.info(f"File downloaded successfully to {output_path}")
                    return output_path
                else:
                    raise Exception(f"Failed to download file: HTTP {response.status}")
    except Exception as e:
        logger.error(f"Error downloading file: {str(e)}", exc_info=True)
        raise Exception(f"Failed to download file: {str(e)}")