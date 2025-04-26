const fs = require('fs');
const path = require('path');
const axios = require('axios');
const { logger } = require('./logger');

// Create temp directory if it doesn't exist
const tempDir = path.join(__dirname, '../../temp');
try {
  fs.mkdirSync(tempDir, { recursive: true });
} catch (err) {
  // Directory already exists or cannot be created
}

/**
 * Download a file from a URL and save it to the temp directory
 * @param {String} url - URL of the file to download
 * @param {String} fileName - Name to save the file as
 * @returns {Promise<String>} Path to the downloaded file
 */
async function downloadFile(url, fileName) {
  try {
    // Generate a unique filename
    const uniqueFileName = `${Date.now()}-${fileName}`;
    const filePath = path.join(tempDir, uniqueFileName);
    
    logger.info(`Downloading file from ${url} to ${filePath}`);
    
    // Download the file
    const response = await axios({
      method: 'GET',
      url: url,
      responseType: 'stream',
      maxContentLength: Infinity,
      maxBodyLength: Infinity
    });
    
    // Create a write stream and pipe the response to it
    const writer = fs.createWriteStream(filePath);
    response.data.pipe(writer);
    
    // Return a promise that resolves when the file is downloaded
    return new Promise((resolve, reject) => {
      writer.on('finish', () => {
        logger.info(`File downloaded successfully to ${filePath}`);
        resolve(filePath);
      });
      writer.on('error', (err) => {
        logger.error(`Error writing file to ${filePath}:`, err);
        reject(err);
      });
    });
  } catch (error) {
    logger.error('Error downloading file:', error);
    throw new Error('Failed to download file: ' + error.message);
  }
}

module.exports = { downloadFile };