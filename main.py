# Import the Flask app 
from keep_alive import app
from flask import render_template
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_IDS
from logger import logger

@app.route('/telegram-setup')
def telegram_setup():
    """Display Telegram setup instructions and status"""
    # Extract bot username from token (if available)
    bot_username = "tsh_job_alert_bot"  # Default from your earlier message
    
    # Get chat IDs as a list
    chat_ids = []
    if TELEGRAM_CHAT_IDS and TELEGRAM_CHAT_IDS != ['']:
        chat_ids = [cid for cid in TELEGRAM_CHAT_IDS if cid]
    
    return render_template('telegram_setup.html',
                          bot_username=bot_username,
                          telegram_token=TELEGRAM_BOT_TOKEN is not None,
                          chat_ids=chat_ids)

@app.route('/send-test')
def send_test_page():
    """Display a page to send test messages"""
    # Get chat IDs as a list
    chat_ids = []
    if TELEGRAM_CHAT_IDS and TELEGRAM_CHAT_IDS != ['']:
        chat_ids = [cid for cid in TELEGRAM_CHAT_IDS if cid]
    
    return render_template('send_test.html',
                          telegram_token=TELEGRAM_BOT_TOKEN is not None,
                          chat_ids=chat_ids)

if __name__ == "__main__":
    # Import the keep_alive function to start the server
    from keep_alive import keep_alive
    
    # Start the server and job checker
    keep_alive()
    
    try:
        # Keep the main thread alive
        import time
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        print("Application shutting down...")
        
        # Import job_checker to stop it properly
        from job_checker import stop_job_checker
        stop_job_checker()