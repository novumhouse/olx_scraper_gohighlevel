#!/usr/bin/env python3
"""
OLX Scraper Scheduler

This script schedules the OLX scraper to run at regular intervals.
It uses the schedule library to run the scraper at specified times.
"""

import os
import time
import logging
import argparse
import schedule
import subprocess
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("scheduler.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def run_scraper(headless=True, api_key=None, max_pages=5, max_listings=50):
    """
    Run the OLX scraper
    
    Args:
        headless (bool): Whether to run in headless mode
        api_key (str): GoHighLevel API key
        max_pages (int): Maximum number of pages to scrape
        max_listings (int): Maximum number of listings to process
    """
    try:
        logger.info(f"Starting OLX scraper at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Build the command
        cmd = ["python3", "olx_scraper.py"]
        
        if headless:
            cmd.append("--headless")
            
        if api_key:
            cmd.extend(["--api-key", api_key])
            
        cmd.extend(["--max-pages", str(max_pages)])
        cmd.extend(["--max-listings", str(max_listings)])
        
        # Run the command
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            logger.info(f"OLX scraper completed successfully: {result.stdout}")
        else:
            logger.error(f"OLX scraper failed: {result.stderr}")
            
    except Exception as e:
        logger.error(f"Error running OLX scraper: {str(e)}")
        
def run_gohighlevel_integration(api_key, input_file="olx_results.json"):
    """
    Run the GoHighLevel integration
    
    Args:
        api_key (str): GoHighLevel API key
        input_file (str): Input JSON file with contact data
    """
    try:
        logger.info(f"Starting GoHighLevel integration at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Build the command
        cmd = ["python3", "gohighlevel_integration.py", "--api-key", api_key, "--input-file", input_file]
        
        # Run the command
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            logger.info(f"GoHighLevel integration completed successfully: {result.stdout}")
        else:
            logger.error(f"GoHighLevel integration failed: {result.stderr}")
            
    except Exception as e:
        logger.error(f"Error running GoHighLevel integration: {str(e)}")
        
def schedule_job(interval_hours, headless, api_key, max_pages, max_listings, run_immediately=False):
    """
    Schedule the scraper to run at regular intervals
    
    Args:
        interval_hours (int): Interval in hours
        headless (bool): Whether to run in headless mode
        api_key (str): GoHighLevel API key
        max_pages (int): Maximum number of pages to scrape
        max_listings (int): Maximum number of listings to process
        run_immediately (bool): Whether to run immediately
    """
    # Define the job
    def job():
        run_scraper(headless, api_key, max_pages, max_listings)
        if api_key:
            # Wait a bit for the scraper to finish and save results
            time.sleep(10)
            run_gohighlevel_integration(api_key)
            
    # Schedule the job
    schedule.every(interval_hours).hours.do(job)
    
    logger.info(f"Scheduled job to run every {interval_hours} hours")
    
    # Run immediately if requested
    if run_immediately:
        logger.info("Running job immediately")
        job()
        
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute
        
def main():
    """Main function to run the scheduler"""
    # Get defaults from environment variables
    default_interval = int(os.getenv("INTERVAL_HOURS", "24"))
    default_headless = os.getenv("HEADLESS", "true").lower() == "true"
    default_api_key = os.getenv("GOHIGHLEVEL_API_KEY")
    default_max_pages = int(os.getenv("MAX_PAGES", "5"))
    default_max_listings = int(os.getenv("MAX_LISTINGS", "50"))
    
    parser = argparse.ArgumentParser(description="OLX Scraper Scheduler")
    parser.add_argument("--interval", type=int, default=default_interval, help="Interval in hours")
    parser.add_argument("--headless", action="store_true", default=default_headless, help="Run in headless mode")
    parser.add_argument("--api-key", default=default_api_key, help="GoHighLevel API key")
    parser.add_argument("--max-pages", type=int, default=default_max_pages, help="Maximum number of pages to scrape")
    parser.add_argument("--max-listings", type=int, default=default_max_listings, help="Maximum number of listings to process")
    parser.add_argument("--run-now", action="store_true", help="Run immediately")
    
    args = parser.parse_args()
    
    try:
        schedule_job(
            args.interval,
            args.headless,
            args.api_key,
            args.max_pages,
            args.max_listings,
            args.run_now
        )
    except KeyboardInterrupt:
        logger.info("Scheduler stopped by user")
    except Exception as e:
        logger.error(f"Error in scheduler: {str(e)}")
        
if __name__ == "__main__":
    main()

