from flask import Flask, render_template, jsonify
import os
import datetime
from logger import logger
from config import CHECK_INTERVAL, KEYWORDS, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_IDS

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "linkedin-job-scraper")

# Global state to track application status
app_state = {
    "running": True,
    "last_check": None,
    "jobs_found": 0,
    "start_time": datetime.datetime.now(),
    "next_check": None
}

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
        next_check_str = f"in {time_until.seconds // 60} minutes, {time_until.seconds % 60} seconds"
    else:
        next_check_str = "soon"
    
    return render_template('index.html', 
                          app_state=app_state,
                          uptime=uptime_str,
                          next_check=next_check_str,
                          keywords=KEYWORDS,
                          check_interval=CHECK_INTERVAL)

@app.route('/api/status')
def status():
    """Return application status as JSON for API clients"""
    return jsonify({
        "status": "online" if app_state["running"] else "paused",
        "last_check": app_state["last_check"].isoformat() if app_state["last_check"] else None,
        "next_check": app_state["next_check"].isoformat() if app_state["next_check"] else None,
        "jobs_found": app_state["jobs_found"],
        "uptime_seconds": (datetime.datetime.now() - app_state["start_time"]).total_seconds(),
        "keywords": KEYWORDS
    })

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

def update_state(jobs_found=None):
    """Update the application state"""
    if jobs_found is not None:
        app_state["jobs_found"] += jobs_found
    
    app_state["last_check"] = datetime.datetime.now()
    app_state["next_check"] = datetime.datetime.now() + datetime.timedelta(seconds=CHECK_INTERVAL)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)