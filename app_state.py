import datetime
from config import CHECK_INTERVAL

# Global state to track application status
app_state = {
    "running": True,
    "last_check": None,
    "jobs_found": 0,
    "start_time": datetime.datetime.now(),
    "next_check": None
}

def update_state(jobs_found=None):
    """Update the application state"""
    if jobs_found is not None:
        app_state["jobs_found"] += jobs_found
    
    app_state["last_check"] = datetime.datetime.now()
    app_state["next_check"] = datetime.datetime.now() + datetime.timedelta(seconds=CHECK_INTERVAL)