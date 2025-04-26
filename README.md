# Telegram to Telegraph Media Converter Bot

A simple Telegram bot that converts media files to Telegraph links.

## Features

- Converts photos, videos, and documents to Telegraph links
- Simple and intuitive interface
- Real-time progress updates
- Error handling and logging

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure environment variables:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your tokens:
   - Get Telegram Bot Token from [@BotFather](https://t.me/BotFather)
   - Create Telegraph token:
     ```python
     from telegraph import Telegraph
     telegraph = Telegraph()
     telegraph.create_account(short_name='YourBot')
     print(f"Access token: {telegraph.get_access_token()}")
     ```

3. Start the bot:
   ```bash
   python main.py
   ```

## Usage

1. Send any media to the bot
2. Wait for processing
3. Receive Telegraph link
4. Share the link

## Commands

- `/start` - Start the bot
- `/help` - Show help
- `/about` - About info