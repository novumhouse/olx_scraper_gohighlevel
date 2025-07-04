#!/usr/bin/env python3
"""
Multi-Client OLX Scraper Scheduler

This script schedules the OLX scraper to run for multiple clients
at their configured intervals.
"""

import os
import json
import time
import logging
import argparse
import schedule
import threading
from datetime import datetime, timedelta
from multi_client_scraper import MultiClientScraperManager

class MultiClientScheduler:
    """Schedules scraping for multiple clients"""
    
    def __init__(self, config_file="clients_config.json"):
        """
        Initialize the multi-client scheduler
        
        Args:
            config_file (str): Path to the client configuration file
        """
        self.config_file = config_file
        self.manager = MultiClientScraperManager(config_file)
        self.scheduled_jobs = {}
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler("multi_client_scheduler.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def schedule_client(self, client_id, headless=True):
        """
        Schedule a client for regular scraping
        
        Args:
            client_id (str): The client ID
            headless (bool): Whether to run in headless mode
        """
        if client_id not in self.manager.clients:
            self.logger.error(f"Client {client_id} not found in configuration")
            return False
            
        client_config = self.manager.clients[client_id]
        client_name = client_config.get("name", client_id)
        interval_hours = client_config.get("schedule_interval_hours", 24)
        
        # Define the job function
        def job():
            self.logger.info(f"Running scheduled scraper for client: {client_name}")
            try:
                success = self.manager.run_client_scraper(client_id, headless)
                if success:
                    self.logger.info(f"Scheduled scraper completed successfully for client: {client_name}")
                else:
                    self.logger.error(f"Scheduled scraper failed for client: {client_name}")
            except Exception as e:
                self.logger.error(f"Error in scheduled job for client {client_name}: {str(e)}")
        
        # Schedule the job
        scheduled_job = schedule.every(interval_hours).hours.do(job)
        self.scheduled_jobs[client_id] = scheduled_job
        
        self.logger.info(f"Scheduled client {client_name} to run every {interval_hours} hours")
        return True
        
    def schedule_all_clients(self, headless=True):
        """
        Schedule all clients for regular scraping
        
        Args:
            headless (bool): Whether to run in headless mode
        """
        scheduled_count = 0
        
        for client_id in self.manager.clients:
            if self.schedule_client(client_id, headless):
                scheduled_count += 1
                
        self.logger.info(f"Scheduled {scheduled_count} clients for regular scraping")
        return scheduled_count
        
    def run_client_now(self, client_id, headless=True):
        """
        Run scraper for a specific client immediately
        
        Args:
            client_id (str): The client ID
            headless (bool): Whether to run in headless mode
        """
        if client_id not in self.manager.clients:
            self.logger.error(f"Client {client_id} not found in configuration")
            return False
            
        client_name = self.manager.clients[client_id].get("name", client_id)
        
        def run_async():
            self.logger.info(f"Running immediate scraper for client: {client_name}")
            try:
                success = self.manager.run_client_scraper(client_id, headless)
                if success:
                    self.logger.info(f"Immediate scraper completed successfully for client: {client_name}")
                else:
                    self.logger.error(f"Immediate scraper failed for client: {client_name}")
            except Exception as e:
                self.logger.error(f"Error in immediate job for client {client_name}: {str(e)}")
        
        # Run in a separate thread to not block the scheduler
        thread = threading.Thread(target=run_async)
        thread.daemon = True
        thread.start()
        
        return True
        
    def run_all_clients_now(self, headless=True):
        """
        Run scraper for all clients immediately
        
        Args:
            headless (bool): Whether to run in headless mode
        """
        def run_async():
            self.logger.info("Running immediate scraper for all clients")
            try:
                results = self.manager.run_all_clients(headless)
                self.logger.info(f"Immediate scraper for all clients completed: {results}")
            except Exception as e:
                self.logger.error(f"Error in immediate job for all clients: {str(e)}")
        
        # Run in a separate thread to not block the scheduler
        thread = threading.Thread(target=run_async)
        thread.daemon = True
        thread.start()
        
    def unschedule_client(self, client_id):
        """
        Unschedule a client
        
        Args:
            client_id (str): The client ID
        """
        if client_id in self.scheduled_jobs:
            schedule.cancel_job(self.scheduled_jobs[client_id])
            del self.scheduled_jobs[client_id]
            self.logger.info(f"Unscheduled client: {client_id}")
            return True
        else:
            self.logger.warning(f"Client {client_id} is not scheduled")
            return False
            
    def unschedule_all_clients(self):
        """Unschedule all clients"""
        for client_id in list(self.scheduled_jobs.keys()):
            self.unschedule_client(client_id)
            
    def get_schedule_status(self):
        """Get the current schedule status"""
        status = {
            "total_clients": len(self.manager.clients),
            "scheduled_clients": len(self.scheduled_jobs),
            "next_runs": []
        }
        
        for client_id, job in self.scheduled_jobs.items():
            client_name = self.manager.clients[client_id].get("name", client_id)
            next_run = job.next_run
            
            if next_run:
                status["next_runs"].append({
                    "client_id": client_id,
                    "client_name": client_name,
                    "next_run": next_run.strftime("%Y-%m-%d %H:%M:%S")
                })
        
        # Sort by next run time
        status["next_runs"].sort(key=lambda x: x["next_run"])
        
        return status
        
    def print_schedule_status(self):
        """Print the current schedule status"""
        status = self.get_schedule_status()
        
        print(f"\n{'='*60}")
        print("SCHEDULE STATUS")
        print(f"{'='*60}")
        print(f"Total clients: {status['total_clients']}")
        print(f"Scheduled clients: {status['scheduled_clients']}")
        print()
        
        if status["next_runs"]:
            print("Next scheduled runs:")
            print("-" * 40)
            for run_info in status["next_runs"]:
                print(f"{run_info['client_name']} ({run_info['client_id']}): {run_info['next_run']}")
        else:
            print("No clients scheduled")
            
    def run_scheduler(self, headless=True, run_immediately=False):
        """
        Run the scheduler
        
        Args:
            headless (bool): Whether to run in headless mode
            run_immediately (bool): Whether to run all clients immediately
        """
        try:
            # Schedule all clients
            self.schedule_all_clients(headless)
            
            # Run immediately if requested
            if run_immediately:
                self.run_all_clients_now(headless)
                
            # Print initial status
            self.print_schedule_status()
            
            self.logger.info("Multi-client scheduler started. Press Ctrl+C to stop.")
            
            # Keep the scheduler running
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
                
        except KeyboardInterrupt:
            self.logger.info("Scheduler stopped by user")
        except Exception as e:
            self.logger.error(f"Error in scheduler: {str(e)}")
        finally:
            self.unschedule_all_clients()
            
def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Multi-Client OLX Scraper Scheduler")
    parser.add_argument("--config", default="clients_config.json", help="Configuration file path")
    parser.add_argument("--headless", action="store_true", default=True, help="Run in headless mode")
    parser.add_argument("--run-now", action="store_true", help="Run all clients immediately")
    parser.add_argument("--client", help="Run specific client immediately")
    parser.add_argument("--status", action="store_true", help="Show schedule status and exit")
    
    args = parser.parse_args()
    
    # Initialize the scheduler
    scheduler = MultiClientScheduler(args.config)
    
    if args.status:
        scheduler.print_schedule_status()
        return
        
    if args.client:
        scheduler.run_client_now(args.client, args.headless)
        print(f"Started scraper for client: {args.client}")
        return
        
    if args.run_now:
        scheduler.run_all_clients_now(args.headless)
        print("Started scraper for all clients")
        return
        
    # Run the scheduler
    scheduler.run_scheduler(args.headless, args.run_now)
    
if __name__ == "__main__":
    main()