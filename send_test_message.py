import requests
import time
import os
from logger import logger
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_IDS

def send_test_message():
    """Send a test message to all configured Telegram users"""
    
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_IDS or TELEGRAM_CHAT_IDS == ['']:
        logger.error("Telegram configuration is incomplete, cannot send message")
        print("Error: TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_IDS not properly configured.")
        print("Please set these environment variables and try again.")
        return False
        
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    
    # Create a dummy job notification message
    message = """🔔 <b>Test Message from LinkedIn Job Scraper</b>

This is a test notification from your LinkedIn Job Scraper. If you're receiving this message, your Telegram notifications are correctly configured!

<b>System Status:</b> Online
<b>Check Interval:</b> 5 minutes
<b>Monitored Keywords:</b> qa, java, python, javascript, remote

Thank you for using the LinkedIn Job Scraper!
"""
    
    success_count = 0
    total_users = len([chat_id for chat_id in TELEGRAM_CHAT_IDS if chat_id])
    
    print(f"Attempting to send test message to {total_users} users...")
    
    for chat_id in TELEGRAM_CHAT_IDS:
        if not chat_id:  # Skip empty chat IDs
            continue
            
        payload = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'HTML'
        }
        
        try:
            print(f"Sending message to chat ID: {chat_id}...")
            response = requests.post(url, data=payload)
            
            if response.status_code == 200:
                success_count += 1
                print(f"✓ Successfully sent notification to chat {chat_id}")
                logger.info(f"Successfully sent test notification to chat {chat_id}")
            else:
                print(f"✗ Failed to send message to {chat_id}. Status code: {response.status_code}")
                print(f"Response: {response.text}")
                logger.error(f"Failed to send test message to {chat_id}. Status code: {response.status_code}, Response: {response.text}")
            
            # Add a small delay between messages to avoid hitting rate limits
            time.sleep(0.5)
            
        except Exception as e:
            print(f"✗ Failed to send message to {chat_id}: {e}")
            logger.error(f"Failed to send test message to {chat_id}: {e}")
    
    print(f"\nSummary: Successfully sent messages to {success_count} out of {total_users} users.")
    return success_count > 0

if __name__ == "__main__":
    print("\n=== LinkedIn Job Scraper - Telegram Test ===\n")
    send_test_message()