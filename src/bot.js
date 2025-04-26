const TelegramBot = require('node-telegram-bot-api');
const { uploadToTelegraph } = require('./telegraph');
const { logger } = require('./utils/logger');
const { downloadFile } = require('./utils/fileHandler');

/**
 * Initialize the Telegram bot with the provided token
 */
function initBot() {
  // Create a bot instance
  const bot = new TelegramBot(process.env.TELEGRAM_BOT_TOKEN, { polling: true });

  // Handle /start command
  bot.onText(/\/start/, (msg) => {
    const chatId = msg.chat.id;
    const message = 'Welcome to the Media to Telegraph Link Converter Bot!\n\n' +
      'Send me any photo, video, or document and I will convert it to a Telegraph link for you.\n\n' +
      'Use /help for more information.';
    
    bot.sendMessage(chatId, message);
    logger.info(`User ${msg.from.username || msg.from.id} started the bot`);
  });

  // Handle /help command
  bot.onText(/\/help/, (msg) => {
    const chatId = msg.chat.id;
    const message = 'How to use this bot:\n\n' +
      '1. Simply send any photo, video, or document to the bot\n' +
      '2. The bot will upload it to Telegraph and send you the link\n' +
      '3. You can share this link with anyone\n\n' +
      'Available commands:\n' +
      '/start - Start the bot\n' +
      '/help - Show this help message\n' +
      '/about - Information about the bot';
    
    bot.sendMessage(chatId, message);
  });

  // Handle /about command
  bot.onText(/\/about/, (msg) => {
    const chatId = msg.chat.id;
    const message = 'Media to Telegraph Link Converter Bot\n\n' +
      'This bot helps you convert media files to Telegraph links for easy sharing.\n\n' +
      'Developed with Node.js and love ❤️\n' +
      'Source code: https://github.com/yourusername/telegram-telegraph-bot';
    
    bot.sendMessage(chatId, message);
  });

  // Handle photo messages
  bot.on('photo', async (msg) => {
    await handleMedia(bot, msg, 'photo');
  });

  // Handle video messages
  bot.on('video', async (msg) => {
    await handleMedia(bot, msg, 'video');
  });

  // Handle document messages
  bot.on('document', async (msg) => {
    await handleMedia(bot, msg, 'document');
  });

  // Log errors
  bot.on('polling_error', (error) => {
    logger.error('Polling error:', error);
  });

  return bot;
}

/**
 * Handle media messages and upload them to Telegraph
 * @param {TelegramBot} bot - The bot instance
 * @param {Object} msg - The message object
 * @param {String} mediaType - The type of media (photo, video, document)
 */
async function handleMedia(bot, msg, mediaType) {
  const chatId = msg.chat.id;
  let fileId, fileName;

  // Get file ID based on media type
  if (mediaType === 'photo') {
    // Get the largest photo (last in array)
    const photos = msg.photo;
    fileId = photos[photos.length - 1].file_id;
    fileName = 'photo.jpg';
  } else if (mediaType === 'video') {
    fileId = msg.video.file_id;
    fileName = msg.video.file_name || 'video.mp4';
  } else if (mediaType === 'document') {
    fileId = msg.document.file_id;
    fileName = msg.document.file_name || 'document';
  }

  if (!fileId) {
    bot.sendMessage(chatId, 'Sorry, I could not process this file.');
    return;
  }

  // Send processing message
  const processingMessage = await bot.sendMessage(
    chatId, 
    '⏳ Processing your media file...'
  );

  try {
    logger.info(`Processing ${mediaType} from user ${msg.from.username || msg.from.id}`);
    
    // Get file path
    const file = await bot.getFile(fileId);
    
    // Update status message
    await bot.editMessageText(
      '⏳ Downloading your file...', 
      { 
        chat_id: chatId, 
        message_id: processingMessage.message_id 
      }
    );

    // Download the file
    const filePath = await downloadFile(
      `https://api.telegram.org/file/bot${process.env.TELEGRAM_BOT_TOKEN}/${file.file_path}`,
      fileName
    );

    // Update status message
    await bot.editMessageText(
      '⏳ Uploading to Telegraph...', 
      { 
        chat_id: chatId, 
        message_id: processingMessage.message_id 
      }
    );

    // Upload to Telegraph
    const telegraphUrl = await uploadToTelegraph(filePath, fileName);

    // Send success message with the link
    await bot.editMessageText(
      `✅ Your media has been uploaded to Telegraph!\n\n${telegraphUrl}`, 
      { 
        chat_id: chatId, 
        message_id: processingMessage.message_id,
        disable_web_page_preview: false
      }
    );

    logger.info(`Successfully processed ${mediaType} for user ${msg.from.username || msg.from.id}`);
  } catch (error) {
    logger.error('Error processing media:', error);
    
    // Send error message
    await bot.editMessageText(
      `❌ Sorry, an error occurred while processing your media.\n\nError: ${error.message}`, 
      { 
        chat_id: chatId, 
        message_id: processingMessage.message_id 
      }
    );
  }
}

module.exports = { initBot };
