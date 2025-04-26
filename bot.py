"""
Telegram bot implementation for the Telegram to Telegraph Media Converter
"""
import os
import tempfile
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler, 
    filters, ContextTypes
)
from telegraph_client import upload_to_telegraph
from utils.logger import get_logger
from utils.file_handler import download_file

# Get logger
logger = get_logger(__name__)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /start command"""
    user = update.effective_user
    username = user.username or user.id
    
    welcome_message = (
        f"Welcome to the Media to Telegraph Link Converter Bot!\n\n"
        f"Send me any photo, video, or document and I will convert it "
        f"to a Telegraph link for you.\n\n"
        f"Use /help for more information."
    )
    
    await update.message.reply_text(welcome_message)
    logger.info(f"User {username} started the bot")

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
        "Developed with Python and love ❤️\n"
        "Source code: https://github.com/yourusername/telegram-telegraph-bot"
    )
    
    await update.message.reply_text(about_message)

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle photo messages"""
    await handle_media(update, context, 'photo')

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle video messages"""
    await handle_media(update, context, 'video')

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle document messages"""
    await handle_media(update, context, 'document')

async def handle_media(update: Update, context: ContextTypes.DEFAULT_TYPE, media_type: str) -> None:
    """
    Handle media messages and upload them to Telegraph
    
    Args:
        update: The update object
        context: The context object
        media_type: The type of media (photo, video, document)
    """
    user = update.effective_user
    username = user.username or user.id
    chat_id = update.effective_chat.id
    
    # Get file information based on media type
    if media_type == 'photo':
        # Get the largest photo (last in array)
        photo = update.message.photo[-1]
        file_id = photo.file_id
        file_name = f"photo_{file_id}.jpg"
    elif media_type == 'video':
        video = update.message.video
        file_id = video.file_id
        file_name = video.file_name or f"video_{file_id}.mp4"
    elif media_type == 'document':
        document = update.message.document
        file_id = document.file_id
        file_name = document.file_name or f"document_{file_id}"
    else:
        await update.message.reply_text("Sorry, I don't support this media type.")
        return
    
    # Send processing message
    processing_msg = await update.message.reply_text("⏳ Processing your media file...")
    
    try:
        logger.info(f"Processing {media_type} from user {username}")
        
        # Update status message
        await processing_msg.edit_text("⏳ Downloading your file...")
        
        # Get file from Telegram
        file = await context.bot.get_file(file_id)
        
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file_name)[1]) as temp_file:
            temp_path = temp_file.name
        
        # Download the file
        await download_file(file.file_path, temp_path)
        
        # Update status message
        await processing_msg.edit_text("⏳ Uploading to Telegraph...")
        
        # Upload to Telegraph
        telegraph_url = await upload_to_telegraph(temp_path, file_name)
        
        # Send success message with the link
        await processing_msg.edit_text(
            f"✅ Your media has been uploaded to Telegraph!\n\n{telegraph_url}",
            disable_web_page_preview=False
        )
        
        logger.info(f"Successfully processed {media_type} for user {username}")
    except Exception as e:
        logger.error(f"Error processing media: {str(e)}", exc_info=True)
        
        # Send error message
        await processing_msg.edit_text(
            f"❌ Sorry, an error occurred while processing your media.\n\nError: {str(e)}"
        )
    finally:
        # Clean up temporary file
        try:
            if 'temp_path' in locals() and os.path.exists(temp_path):
                os.unlink(temp_path)
        except Exception as e:
            logger.error(f"Error deleting temporary file: {str(e)}")

def start_bot():
    """Start the Telegram bot"""
    # Create the Application
    application = Application.builder().token(os.getenv('TELEGRAM_BOT_TOKEN')).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about_command))
    
    # Add message handlers
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.add_handler(MessageHandler(filters.VIDEO, handle_video))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    
    # Start the Bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)
    
    return application