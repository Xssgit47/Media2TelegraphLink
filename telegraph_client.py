"""
Telegraph API client for uploading files and creating pages
"""
import os
import mimetypes
from pathlib import Path
import aiohttp
from telegraph import Telegraph
from utils.logger import get_logger

# Get logger
logger = get_logger(__name__)

# Initialize Telegraph client
telegraph = Telegraph(access_token=os.getenv('TELEGRAPH_ACCESS_TOKEN'))

async def upload_to_telegraph(file_path: str, file_name: str) -> str:
    """
    Upload a file to Telegraph
    
    Args:
        file_path: Path to the file
        file_name: Name of the file
        
    Returns:
        Telegraph URL
    """
    try:
        # Determine file type
        file_ext = Path(file_name).suffix.lower()
        mime_type = mimetypes.guess_type(file_name)[0]
        
        # Check if it's an image
        is_image = False
        if mime_type and mime_type.startswith('image/'):
            is_image = True
        elif file_ext in ['.jpg', '.jpeg', '.png', '.gif']:
            is_image = True
        
        if is_image:
            # Use direct upload for images
            return await upload_image(file_path)
        else:
            # For videos and other files, create a Telegraph page
            return await create_telegraph_page(file_path, file_name)
    except Exception as e:
        logger.error(f"Error uploading to Telegraph: {str(e)}", exc_info=True)
        raise Exception(f"Failed to upload to Telegraph: {str(e)}")

async def upload_image(file_path: str) -> str:
    """
    Upload an image to Telegraph
    
    Args:
        file_path: Path to the image file
        
    Returns:
        Telegraph URL
    """
    async with aiohttp.ClientSession() as session:
        form = aiohttp.FormData()
        form.add_field('file', open(file_path, 'rb'))
        
        async with session.post('https://telegra.ph/upload', data=form) as response:
            if response.status == 200:
                result = await response.json()
                if result and result[0] and 'src' in result[0]:
                    image_url = 'https://telegra.ph' + result[0]['src']
                    logger.info(f"Image uploaded to Telegraph: {image_url}")
                    
                    # Create a Telegraph page with the image
                    page_title = 'Shared Media'
                    author_name = 'Telegraph Bot'
                    content = [
                        {
                            'tag': 'figure',
                            'children': [
                                {
                                    'tag': 'img',
                                    'attrs': {'src': image_url}
                                }
                            ]
                        }
                    ]
                    
                    page = telegraph.create_page(
                        title=page_title,
                        html_content='',
                        content=content,
                        author_name=author_name
                    )
                    
                    logger.info(f"Telegraph page created: {page['url']}")
                    return page['url']
                else:
                    raise Exception("Invalid response from Telegraph API")
            else:
                raise Exception(f"Telegraph API returned status code {response.status}")

async def create_telegraph_page(file_path: str, file_name: str) -> str:
    """
    Create a Telegraph page with embedded content
    
    Args:
        file_path: Path to the file
        file_name: Name of the file
        
    Returns:
        Telegraph URL
    """
    # For now, we'll create a simple page with text
    # In a real implementation, you might want to upload the file to a service
    # that supports the file type and then embed it in the Telegraph page
    
    page_title = 'Shared Media: ' + file_name
    author_name = 'Telegraph Bot'
    
    content = [
        {
            'tag': 'p',
            'children': [
                f"This file ({file_name}) cannot be directly embedded. It has been processed by the Telegraph Bot."
            ]
        }
    ]
    
    page = telegraph.create_page(
        title=page_title,
        html_content='',
        content=content,
        author_name=author_name
    )
    
    logger.info(f"Telegraph page created for non-image file: {page['url']}")
    return page['url']