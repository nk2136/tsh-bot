import requests
import time
import os
from logger import logger
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_IDS

def get_bot_updates():
    """Get updates from the Telegram bot to see recent chat IDs"""
    if not TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN is not set in environment variables")
        print("Error: TELEGRAM_BOT_TOKEN not configured.")
        return False
    
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates'
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            updates = response.json()
            print("\n=== Recent Bot Interactions ===\n")
            
            if not updates.get('result'):
                print("No recent interactions found. Users must start a chat with your bot first.")
                print(f"Ask users to search for @tsh_job_alert_bot on Telegram and send the message '/start'")
                return
            
            print("Here are the most recent chat IDs from users who have interacted with your bot:")
            print("Use these IDs in your TELEGRAM_CHAT_IDS environment variable.")
            print("\nChat ID\t\tUsername/First Name")
            print("-" * 40)
            
            seen_chat_ids = set()
            for update in updates.get('result', []):
                if 'message' in update and 'chat' in update['message']:
                    chat = update['message']['chat']
                    chat_id = chat.get('id')
                    if chat_id and chat_id not in seen_chat_ids:
                        seen_chat_ids.add(chat_id)
                        username = chat.get('username', 'N/A')
                        first_name = chat.get('first_name', 'N/A')
                        display_name = username if username != 'N/A' else first_name
                        print(f"{chat_id}\t{display_name}")
            
            return seen_chat_ids
        else:
            print(f"Failed to get updates. Status code: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error getting bot updates: {e}")
        return False

def send_direct_message(chat_id, message_text):
    """Send a direct message to a specific chat ID for testing"""
    if not TELEGRAM_BOT_TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN not configured.")
        return False
        
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    
    payload = {
        'chat_id': chat_id,
        'text': message_text,
        'parse_mode': 'HTML'
    }
    
    try:
        print(f"Sending message to chat ID: {chat_id}...")
        response = requests.post(url, data=payload)
        
        if response.status_code == 200:
            print(f"✓ Successfully sent notification to chat {chat_id}")
            return True
        else:
            print(f"✗ Failed to send message to {chat_id}. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ Failed to send message to {chat_id}: {e}")
        return False

def send_test_message():
    """Send a test message to all configured Telegram users"""
    
    if not TELEGRAM_BOT_TOKEN:
        logger.error("Telegram configuration is incomplete, cannot send message")
        print("Error: TELEGRAM_BOT_TOKEN not properly configured.")
        print("Please set this environment variable and try again.")
        return False
        
    # Check if we have any chat IDs
    chat_ids = []
    if TELEGRAM_CHAT_IDS and TELEGRAM_CHAT_IDS != ['']:
        chat_ids = [cid.strip() for cid in TELEGRAM_CHAT_IDS if cid.strip()]
    
    if not chat_ids:
        print("Warning: No chat IDs configured. Fetching recent interactions...")
        chat_ids_from_updates = get_bot_updates()
        if chat_ids_from_updates:
            chat_ids = list(chat_ids_from_updates)
        
    if not chat_ids:
        print("\n=== NO VALID USERS FOUND ===")
        print("Please ensure users have initiated a conversation with your bot (@tsh_job_alert_bot).")
        print("Each user should search for the bot on Telegram and send a '/start' message.")
        print("After users have interacted with the bot, run 'python send_test_message.py --get-updates'")
        print("to see their chat IDs, and then update your TELEGRAM_CHAT_IDS environment variable.")
        return False
    
    # Create a dummy job notification message
    message = """🔔 <b>Test Message from LinkedIn Job Scraper</b>

This is a test notification from your LinkedIn Job Scraper. If you're receiving this message, your Telegram notifications are correctly configured!

<b>System Status:</b> Online
<b>Check Interval:</b> 5 minutes
<b>Monitored Keywords:</b> qa, java, python, javascript, remote

Thank you for using the LinkedIn Job Scraper!
"""
    
    success_count = 0
    total_users = len(chat_ids)
    
    print(f"Attempting to send test message to {total_users} users...")
    
    for chat_id in chat_ids:
        if send_direct_message(chat_id, message):
            success_count += 1
            logger.info(f"Successfully sent test notification to chat {chat_id}")
        else:
            logger.error(f"Failed to send test message to {chat_id}")
        
        # Add a small delay between messages to avoid hitting rate limits
        time.sleep(0.5)
    
    print(f"\nSummary: Successfully sent messages to {success_count} out of {total_users} users.")
    
    if success_count == 0:
        print("\n=== TROUBLESHOOTING ===")
        print("If all messages failed, please ensure:")
        print("1. Each user has started a chat with your bot (@tsh_job_alert_bot)")
        print("2. The chat IDs are correct")
        print("\nTo find valid chat IDs, run: python send_test_message.py --get-updates")
    
    return success_count > 0

if __name__ == "__main__":
    print("\n=== LinkedIn Job Scraper - Telegram Test ===\n")
    
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--get-updates":
        get_bot_updates()
    else:
        send_test_message()