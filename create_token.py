#!/usr/bin/env python3
from telegraph import Telegraph

def create_telegraph_token():
    # Create a new Telegraph account
    telegraph = Telegraph()
    
    # Create account and get access token
    account = telegraph.create_account(
        short_name='TelegraphBot',  # Display name
        author_name='Media Converter Bot',  # Author name for articles
        author_url='https://t.me/your_bot_username'  # Replace with your bot's username
    )
    
    # Print the access token
    print("\nTelegraph Access Token created successfully!")
    print("-" * 50)
    print(f"Access Token: {account['access_token']}")
    print("-" * 50)
    print("\nAdd this token to your .env file as TELEGRAPH_ACCESS_TOKEN")

if __name__ == "__main__":
    create_telegraph_token()