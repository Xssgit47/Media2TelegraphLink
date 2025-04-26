require('dotenv').config();
const { initBot } = require('./src/bot');
const { logger } = require('./src/utils/logger');

// Check if required environment variables are set
const requiredEnvVars = ['TELEGRAM_BOT_TOKEN', 'TELEGRAPH_ACCESS_TOKEN'];
const missingEnvVars = requiredEnvVars.filter(envVar => !process.env[envVar]);

if (missingEnvVars.length > 0) {
  logger.error(`Missing required environment variables: ${missingEnvVars.join(', ')}`);
  logger.info('Please set the required environment variables in the .env file');
  process.exit(1);
}

// Initialize the bot
try {
  logger.info('Starting Telegram to Telegraph Bot...');
  initBot();
  logger.info('Bot successfully started!');
} catch (error) {
  logger.error('Failed to start the bot:', error);
  process.exit(1);
}