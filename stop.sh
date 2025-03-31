#!/bin/bash
# Script to stop the LinkedIn Job Scraper Service

# First check if the service is running via PID file
if [ -f app.pid ]; then
    SERVICE_PID=$(cat app.pid)
    
    if ps -p $SERVICE_PID > /dev/null; then
        echo "Stopping LinkedIn Job Scraper Service (PID: $SERVICE_PID)..."
        kill $SERVICE_PID
        
        # Give it a moment to shut down
        sleep 3
        
        # Check if it's still running
        if ps -p $SERVICE_PID > /dev/null; then
            echo "Warning: Service still running. Forcing termination..."
            kill -9 $SERVICE_PID
        fi
        
        # Remove the PID file
        rm app.pid
        echo "LinkedIn Job Scraper Service stopped successfully."
    else
        echo "PID file exists but process is not running. Cleaning up..."
        rm app.pid
    fi
else
    # No PID file, try to find by process name
    if pgrep -f "python run_bot_service.py" > /dev/null || pgrep -f "python run_bot.py" > /dev/null; then
        echo "Stopping LinkedIn Job Scraper processes..."
        
        # Kill the service first
        if pgrep -f "python run_bot_service.py" > /dev/null; then
            pkill -f "python run_bot_service.py"
            sleep 2
        fi
        
        # Then kill any bot processes
        if pgrep -f "python run_bot.py" > /dev/null; then
            pkill -f "python run_bot.py"
            sleep 2
        fi
        
        # Check if any processes are still running
        if pgrep -f "python run_bot_service.py" > /dev/null || pgrep -f "python run_bot.py" > /dev/null; then
            echo "Warning: Processes still running. Forcing termination..."
            pkill -9 -f "python run_bot_service.py"
            pkill -9 -f "python run_bot.py"
        fi
        
        echo "LinkedIn Job Scraper processes stopped successfully."
    else
        echo "LinkedIn Job Scraper is not currently running."
    fi
fi