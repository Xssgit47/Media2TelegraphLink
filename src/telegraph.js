const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');
const path = require('path');
const { logger } = require('./utils/logger');
const Telegraph = require('telegraph-node');

// Initialize Telegraph client
const telegraph = new Telegraph(process.env.TELEGRAPH_ACCESS_TOKEN);

/**
 * Upload a file to Telegraph
 * @param {String} filePath - Path to the file
 * @param {String} fileName - Name of the file
 * @returns {Promise<String>} Telegraph URL
 */
async function uploadToTelegraph(filePath, fileName) {
  try {
    // Determine if the file is an image based on extension
    const fileExt = path.extname(fileName).toLowerCase();
    const isImage = ['.jpg', '.jpeg', '.png', '.gif'].includes(fileExt);
    
    if (isImage) {
      // Use direct upload for images
      return await uploadImage(filePath);
    } else {
      // For videos and other files, create a Telegraph page with embedded content
      return await createTelegraphPage(filePath, fileName);
    }
  } catch (error) {
    logger.error('Error uploading to Telegraph:', error);
    throw new Error('Failed to upload to Telegraph: ' + error.message);
  } finally {
    // Clean up the temporary file
    try {
      fs.unlinkSync(filePath);
      logger.info(`Deleted temporary file: ${filePath}`);
    } catch (err) {
      logger.error(`Error deleting temporary file ${filePath}:`, err);
    }
  }
}

/**
 * Upload an image to Telegraph
 * @param {String} filePath - Path to the image file
 * @returns {Promise<String>} Telegraph URL
 */
async function uploadImage(filePath) {
  const formData = new FormData();
  formData.append('file', fs.createReadStream(filePath));

  const response = await axios.post('https://telegra.ph/upload', formData, {
    headers: formData.getHeaders(),
    maxContentLength: Infinity,
    maxBodyLength: Infinity
  });

  if (response.data && response.data[0] && response.data[0].src) {
    const imageUrl = 'https://telegra.ph' + response.data[0].src;
    logger.info(`Image uploaded to Telegraph: ${imageUrl}`);
    
    // Create a Telegraph page with the image
    const pageTitle = 'Shared Media';
    const authorName = 'Telegraph Bot';
    const content = [
      {
        tag: 'figure',
        children: [
          {
            tag: 'img',
            attrs: { src: imageUrl }
          }
        ]
      }
    ];

    const page = await telegraph.createPage(pageTitle, content, authorName);
    logger.info(`Telegraph page created: ${page.url}`);
    return page.url;
  } else {
    throw new Error('Invalid response from Telegraph API');
  }
}

/**
 * Create a Telegraph page with embedded content
 * @param {String} filePath - Path to the file
 * @param {String} fileName - Name of the file
 * @returns {Promise<String>} Telegraph URL
 */
async function createTelegraphPage(filePath, fileName) {
  // For now, we'll create a simple page with text
  // In a real implementation, you might want to upload the file to a service
  // that supports the file type and then embed it in the Telegraph page
  
  const pageTitle = 'Shared Media: ' + fileName;
  const authorName = 'Telegraph Bot';
  const content = [
    {
      tag: 'p',
      children: [
        `This file (${fileName}) cannot be directly embedded. It has been processed by the Telegraph Bot.`
      ]
    }
  ];

  const page = await telegraph.createPage(pageTitle, content, authorName);
  logger.info(`Telegraph page created for non-image file: ${page.url}`);
  return page.url;
}

module.exports = { uploadToTelegraph };