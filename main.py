import os
import datetime
from flask import Flask, jsonify, render_template
from app_state import app_state, update_state
from config import CHECK_INTERVAL, KEYWORDS, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_IDS
from logger import logger

# Initialize the Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "linkedin-job-scraper")

@app.route('/')
def home():
    """Display application status and configuration"""
    # Calculate uptime
    uptime = datetime.datetime.now() - app_state["start_time"]
    uptime_str = f"{uptime.days} days, {uptime.seconds // 3600} hours, {(uptime.seconds // 60) % 60} minutes"
    
    # Format next check time
    next_check = app_state["next_check"]
    if next_check:
        time_until = next_check - datetime.datetime.now()
        seconds_until = max(0, int(time_until.total_seconds()))
        next_check_str = f"in {seconds_until // 60} minutes, {seconds_until % 60} seconds"
    else:
        next_check_str = "soon"
    
    return render_template('index.html', 
                          app_state=app_state,
                          uptime=uptime_str,
                          next_check=next_check_str,
                          keywords=KEYWORDS,
                          check_interval=CHECK_INTERVAL)

@app.route('/ping')
def ping():
    """Simple endpoint for uptime monitoring services to ping"""
    # Calculate uptime
    uptime = datetime.datetime.now() - app_state["start_time"]
    uptime_str = f"{uptime.days} days, {uptime.seconds // 3600} hours, {(uptime.seconds // 60) % 60} minutes"
    
    # Update the status with the ping time
    app_state["last_ping"] = datetime.datetime.now()
    app_state["ping_count"] = app_state.get("ping_count", 0) + 1
    
    # Return a simple response with some basic status info
    return f"OK - Up for {uptime_str} - Last check: {app_state['last_check'].isoformat() if app_state['last_check'] else 'Never'} - Ping count: {app_state['ping_count']}", 200

@app.route('/api/telegram-status')
def telegram_status():
    """Check Telegram configuration status"""
    return jsonify({
        "configured": bool(TELEGRAM_BOT_TOKEN),
        "chat_ids": len(TELEGRAM_CHAT_IDS),
        "status": "Ready" if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_IDS else "Not Configured"
    })

@app.route('/api/send-test')
def send_test():
    """Send a test message to all Telegram users"""
    from job_checker import job_checker
    success = job_checker.send_test_message()
    if success:
        return render_template('base.html', 
                              uptime=f"Test message sent successfully at {datetime.datetime.now()}")
    else:
        return render_template('base.html', 
                              uptime=f"Failed to send test message. Check Telegram configuration.")

if __name__ == "__main__":
    # Initialize app state
    if not app_state.get("start_time"):
        app_state["start_time"] = datetime.datetime.now()
    
    # Update initial state
    update_state()
    
    # Start the job checker
    from job_checker import start_job_checker
    logger.info("Starting job checker")
    job_checker = start_job_checker()
    
    # Start the web server
    app.run(host='0.0.0.0', port=8080, debug=True)