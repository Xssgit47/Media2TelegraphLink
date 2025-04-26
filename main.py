#!/usr/bin/env python3
import os
import sys
import logging
import tempfile
from pathlib import Path
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegraph import Telegraph as TelegraphClient
import aiohttp

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='[%(asctime)s] %(levelname)s: %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Initialize Telegraph client
telegraph_client = TelegraphClient(access_token=os.getenv('TELEGRAPH_ACCESS_TOKEN'))

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /start command"""
    welcome_message = (
        f"Welcome to the Media to Telegraph Link Converter Bot!\n\n"
        f"Send me any photo, video, or document and I will convert it "
        f"to a Telegraph link for you.\n\n"
        f"Use /help for more information."
    )
    await update.message.reply_text(welcome_message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /help command"""
    help_message = (
        "How to use this bot:\n\n"
        "1. Simply send any photo, video, or document to the bot\n"
        "2. The bot will upload it to Telegraph and send you the link\n"
        "3. You can share this link with anyone\n\n"
        "Available commands:\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/about - Information about the bot"
    )
    await update.message.reply_text(help_message)

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /about command"""
    about_message = (
        "Media to Telegraph Link Converter Bot\n\n"
        "This bot helps you convert media files to Telegraph links for easy sharing.\n\n"
        "Developed with Python and love ❤️"
    )
    await update.message.reply_text(about_message)

async def upload_to_telegraph(file_path: str, file_name: str) -> str:
    """Upload a file to Telegraph"""
    async with aiohttp.ClientSession() as session:
        form = aiohttp.FormData()
        form.add_field('file', open(file_path, 'rb'))
        
        async with session.post('https://telegra.ph/upload', data=form) as response:
            if response.status == 200:
                result = await response.json()
                if result and result[0] and 'src' in result[0]:
                    image_url = 'https://telegra.ph' + result[0]['src']
                    
                    # Create a Telegraph page with the image
                    page = telegraph_client.create_page(
                        title='Shared Media',
                        html_content='',
                        content=[
                            {
                                'tag': 'figure',
                                'children': [
                                    {
                                        'tag': 'img',
                                        'attrs': {'src': image_url}
                                    }
                                ]
                            }
                        ],
                        author_name='Telegraph Bot'
                    )
                    return page['url']
            raise Exception("Failed to upload to Telegraph")

async def handle_media(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle media messages"""
    # Determine the type of media and get file info
    if update.message.photo:
        file = update.message.photo[-1]
        file_name = f"photo_{file.file_id}.jpg"
    elif update.message.video:
        file = update.message.video
        file_name = file.file_name or f"video_{file.file_id}.mp4"
    elif update.message.document:
        file = update.message.document
        file_name = file.file_name or f"document_{file.file_id}"
    else:
        await update.message.reply_text("Sorry, I don't support this media type.")
        return

    # Send processing message
    processing_msg = await update.message.reply_text("⏳ Processing your media file...")
    
    try:
        # Get file from Telegram
        tg_file = await context.bot.get_file(file.file_id)
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file_name).suffix) as temp_file:
            # Download file
            await processing_msg.edit_text("⏳ Downloading your file...")
            await tg_file.download_to_drive(temp_file.name)
            
            # Upload to Telegraph
            await processing_msg.edit_text("⏳ Uploading to Telegraph...")
            telegraph_url = await upload_to_telegraph(temp_file.name, file_name)
            
            # Send success message
            await processing_msg.edit_text(
                f"✅ Your media has been uploaded to Telegraph!\n\n{telegraph_url}",
                disable_web_page_preview=False
            )
    except Exception as e:
        logger.error(f"Error processing media: {str(e)}", exc_info=True)
        await processing_msg.edit_text(
            f"❌ Sorry, an error occurred while processing your media.\n\nError: {str(e)}"
        )
    finally:
        # Clean up temporary file
        if 'temp_file' in locals():
            try:
                os.unlink(temp_file.name)
            except Exception as e:
                logger.error(f"Error deleting temporary file: {str(e)}")

def main():
    """Main function to start the bot"""
    if not os.getenv('TELEGRAM_BOT_TOKEN') or not os.getenv('TELEGRAPH_ACCESS_TOKEN'):
        logger.error("Missing required environment variables. Please check your .env file.")
        sys.exit(1)
    
    try:
        # Create the Application
        application = Application.builder().token(os.getenv('TELEGRAM_BOT_TOKEN')).build()
        
        # Add handlers
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("about", about_command))
        application.add_handler(MessageHandler(
            filters.PHOTO | filters.VIDEO | filters.Document.ALL,
            handle_media
        ))
        
        # Start the Bot
        logger.info("Starting bot...")
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    except Exception as e:
        logger.error(f"Failed to start the bot: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()