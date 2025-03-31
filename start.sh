#!/bin/bash
# Script to start the LinkedIn Job Scraper Service

# Check if the service is already running
if [ -f app.pid ] && ps -p $(cat app.pid) > /dev/null; then
    echo "LinkedIn Job Scraper Service is already running."
    echo "Service Process ID: $(cat app.pid)"
    exit 0
fi

# Clean up any stale PID file
if [ -f app.pid ]; then
    rm app.pid
fi

# Start the service in the background
echo "Starting LinkedIn Job Scraper Service..."
nohup python run_bot_service.py > service.log 2>&1 &
PID=$!

# Sleep for a moment to ensure the service starts correctly
sleep 5

# Check if the service created a PID file
if [ -f app.pid ]; then
    SERVICE_PID=$(cat app.pid)
    echo "LinkedIn Job Scraper Service started successfully."
    echo "Service Process ID: $SERVICE_PID"
    echo "View the web interface at: https://${REPL_SLUG}.${REPL_OWNER}.repl.co:8080"
    echo "Logs are being saved to: app.log and service.log"
else
    echo "Warning: Service started but no PID file was created."
    echo "Check service.log for details."
fi