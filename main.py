# Import the Flask app 
from keep_alive import app
from flask import render_template, request, redirect, url_for, flash
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_IDS, KEYWORDS, LOCATION, REMOTE_ONLY, DAYS_RECENT
from logger import logger
import os

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

@app.route('/configure', methods=['GET', 'POST'])
def configure_page():
    """Display and handle the search configuration page"""
    # Configuration parameters
    current_config = {
        'keywords': ','.join(KEYWORDS),
        'location': LOCATION,
        'remote_only': REMOTE_ONLY,
        'days_recent': DAYS_RECENT
    }
    
    if request.method == 'POST':
        try:
            # Get form data
            keywords = request.form.get('keywords', '').strip()
            location = request.form.get('location', '').strip()
            remote_only = 'remote_only' in request.form
            days_recent = int(request.form.get('days_recent', 1))
            
            # Update environment variables
            # Note: These will only persist for the current session
            os.environ['KEYWORDS'] = keywords
            os.environ['LOCATION'] = location
            os.environ['REMOTE_ONLY'] = 'true' if remote_only else 'false'
            os.environ['DAYS_RECENT'] = str(days_recent)
            
            # Restart the job checker to apply new settings
            from job_checker import stop_job_checker, start_job_checker
            stop_job_checker()
            start_job_checker()
            
            # Update current config to show updated values
            current_config = {
                'keywords': keywords,
                'location': location,
                'remote_only': remote_only,
                'days_recent': days_recent
            }
            
            logger.info(f"Configuration updated: {current_config}")
            
            # Display a success message
            flash('Configuration updated successfully! Job checker has been restarted with new settings.', 'success')
            return redirect(url_for('configure_page'))
            
        except Exception as e:
            logger.error(f"Error updating configuration: {e}")
            flash(f'Error updating configuration: {str(e)}', 'error')
    
    return render_template('configure.html', config=current_config)

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