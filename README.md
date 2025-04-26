# Telegram to Telegraph Media Converter Bot v3.0

![Release](https://img.shields.io/badge/Release-v3.0-red)
![License](https://img.shields.io/badge/License-MIT-gray)

## Supported Operating Systems

<div align="center">
  <img src="https://img.shields.io/badge/Ubuntu%2018.04-BIONIC%20BEAVER-orange?style=for-the-badge&logo=ubuntu&logoColor=white" alt="Ubuntu 18.04" />
  <img src="https://img.shields.io/badge/Ubuntu%2020.04-FOCAL%20FOSSA-orange?style=for-the-badge&logo=ubuntu&logoColor=white" alt="Ubuntu 20.04" />
  <img src="https://img.shields.io/badge/Debian%2010-BUSTER-purple?style=for-the-badge&logo=debian&logoColor=white" alt="Debian 10" />
  <img src="https://img.shields.io/badge/Debian%2011-BULLSEYE-purple?style=for-the-badge&logo=debian&logoColor=white" alt="Debian 11" />
</div>

## Features

<div align="center">
  <img src="https://img.shields.io/badge/PHOTO-SUPPORT-blue?style=for-the-badge" alt="Photo Support" />
  <img src="https://img.shields.io/badge/VIDEO-SUPPORT-blue?style=for-the-badge" alt="Video Support" />
  <img src="https://img.shields.io/badge/DOCUMENT-SUPPORT-blue?style=for-the-badge" alt="Document Support" />
</div>

## Requirements

- Python 3.8 or higher
- Telegram Bot Token (from [@BotFather](https://t.me/BotFather))
- Telegraph Access Token

## Quick Installation

```bash
# Update system packages
apt update && apt upgrade -y

# Install required packages
apt install -y python3 python3-pip python3-venv git supervisor

# Clone repository
git clone https://github.com/yourusername/telegram-telegraph-bot.git
cd telegram-telegraph-bot

# Install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your tokens
```

##
