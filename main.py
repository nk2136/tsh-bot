import os
import time
from datetime import datetime
from flask import Flask, jsonify

app = Flask(__name__)

# Configuration
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_IDS = os.environ.get('TELEGRAM_CHAT_IDS', '').split(',') if os.environ.get('TELEGRAM_CHAT_IDS') else []

# Global state
app_state = {
    "start_time": datetime.now(),
    "last_ping": None,
    "ping_count": 0
}

@app.route('/')
def home():
    """Display application status"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>LinkedIn Job Scraper</title>
        <link href="https://cdn.replit.com/agent/bootstrap-agent-dark-theme.min.css" rel="stylesheet">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body>
        <div class="container mt-5">
            <div class="card">
                <div class="card-header bg-primary text-white">
                    LinkedIn Job Scraper - Status
                </div>
                <div class="card-body">
                    <h5 class="card-title">Application Status</h5>
                    <p class="card-text">The application is running!</p>
                    <p>Check the README.md file for instructions on how to make this application run permanently.</p>
                    <a href="/ping" class="btn btn-primary">Check Ping Status</a>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

@app.route('/ping')
def ping():
    """Simple endpoint for uptime monitoring services to ping"""
    # Calculate uptime
    uptime = datetime.now() - app_state["start_time"]
    uptime_str = f"{uptime.days} days, {uptime.seconds // 3600} hours, {(uptime.seconds // 60) % 60} minutes"
    
    # Update the status with the ping time
    app_state["last_ping"] = datetime.now()
    app_state["ping_count"] = app_state.get("ping_count", 0) + 1
    
    # Return a simple response with some basic status info
    return f"OK - Up for {uptime_str} - Ping count: {app_state['ping_count']}", 200

@app.route('/api/telegram-status')
def telegram_status():
    """Check Telegram configuration status"""
    return jsonify({
        "configured": bool(TELEGRAM_BOT_TOKEN),
        "chat_ids": len(TELEGRAM_CHAT_IDS),
        "status": "Ready" if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_IDS else "Not Configured"
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)