# LinkedIn Job Scraper

A web scraper that monitors LinkedIn for new job postings based on keywords and sends notifications via Telegram when new jobs are found.

## Features

- Automatically scrapes LinkedIn for new job listings
- Sends notifications via Telegram when new jobs are posted
- Web dashboard for monitoring and configuration
- Customizable search keywords, location, and filters
- Statistics and insights into job trends
- Test message capability to verify Telegram integration
- Runs continuously with regular job checks every 5 minutes

## How to Make Your URL Permanent

By default, Replit development URLs are temporary and will sleep after you leave the workspace. To make your URL permanent and keep the application running:

1. **Deploy your application**:
   - Click the "Deploy" button in the Replit interface
   - This will create a permanent URL for your application (e.g., `your-app-name.replit.app`)
   - Your application will now run continuously

2. **Set up Uptime Robot for additional reliability**:
   - Create an account at [uptimerobot.com](https://uptimerobot.com)
   - Add a new monitor with type "HTTP(s)"
   - Enter your deployed URL + "/ping" as the URL to monitor (e.g., `https://your-app-name.replit.app/ping`)
   - Set the monitoring interval to 5 minutes
   - This will ping your application regularly to keep it alive

## Configuration

The application is configured using environment variables:

- `TELEGRAM_BOT_TOKEN`: Token for your Telegram bot (required for notifications)
- `TELEGRAM_CHAT_IDS`: Comma-separated list of Telegram chat IDs to receive notifications
- `KEYWORDS`: Comma-separated list of keywords to search for (default: qa,java)
- `LOCATION`: Location to search for jobs (default: United States)
- `REMOTE_ONLY`: Whether to only search for remote jobs (default: true)
- `DAYS_RECENT`: Jobs posted in last X days (default: 1)
- `CHECK_INTERVAL`: Seconds between job checks (default: 300 - 5 minutes)

## Web Interface

The application provides a web interface with:

- Status dashboard showing application state and statistics
- Configuration page for updating search parameters
- Test message page for verifying Telegram notifications
- Detailed job view for exploring job listings

## Running Locally

```bash
python main.py
```

## Running Permanently (Deployment Mode)

```bash
python deploy.py
```

This will start the application in deployment mode, which will:
1. Set up the necessary data structures
2. Start the job checking thread
3. Keep the application running indefinitely
4. Log instructions for setting up Uptime Robot

Remember to configure Uptime Robot to ping `/ping` every 5 minutes to ensure your application stays alive.