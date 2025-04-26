#!/bin/bash

# Update system packages
apt update && apt upgrade -y

# Install required system packages
apt install -y python3 python3-pip python3-venv git supervisor

# Create directory for the bot
mkdir -p /opt/telegram-telegraph-bot
cd /opt/telegram-telegraph-bot

# Clone the repository
git clone https://github.com/Xssgit47/Media2TelegraphLink.git

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env

# Create supervisor configuration
cat > /etc/supervisor/conf.d/telegram-telegraph-bot.conf << EOL
[program:telegram-telegraph-bot]
directory=/opt/telegram-telegraph-bot
command=/opt/telegram-telegraph-bot/venv/bin/python main.py
autostart=true
autorestart=true
stderr_logfile=/var/log/telegram-telegraph-bot.err.log
stdout_logfile=/var/log/telegram-telegraph-bot.out.log
user=root
environment=PATH="/opt/telegram-telegraph-bot/venv/bin"
EOL

# Reload supervisor
supervisorctl reread
supervisorctl update
