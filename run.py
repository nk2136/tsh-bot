"""
Web server for the LinkedIn Job Scraper application
This is the main entry point for the web interface
"""

from keep_alive import app

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)