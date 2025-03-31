import logging
import sys
from config import LOG_LEVEL

# Configure logger
def setup_logger():
    logger = logging.getLogger('linkedin_job_scraper')
    logger.setLevel(LOG_LEVEL)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(LOG_LEVEL)
    
    # Format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(console_handler)
    
    return logger

logger = setup_logger()
