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
        
        # Check if client is enabled
        if not client_config.get("enabled", True):
            self.logger.info(f"Client {client_name} is disabled, skipping scheduling")
            return True
        
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
        
        # Schedule the job using new cron format or legacy hour format
        scheduled_job = None
        
        # Priority 1: New cron format (schedule field)
        if "schedule" in client_config and client_config["schedule"]:
            try:
                cron_schedule = client_config["schedule"]
                scheduled_job = self._schedule_with_cron(cron_schedule, job)
                self.logger.info(f"Scheduled client {client_name} with cron: {cron_schedule}")
            except Exception as e:
                self.logger.warning(f"Failed to schedule client {client_name} with cron '{client_config['schedule']}': {e}")
                scheduled_job = None
        
        # Priority 2: Legacy hour interval format (schedule_interval_hours field)
        if not scheduled_job and "schedule_interval_hours" in client_config:
            try:
                interval_hours = client_config["schedule_interval_hours"]
                scheduled_job = schedule.every(interval_hours).hours.do(job)
                self.logger.info(f"Scheduled client {client_name} to run every {interval_hours} hours (legacy format)")
            except Exception as e:
                self.logger.warning(f"Failed to schedule client {client_name} with hour interval: {e}")
                scheduled_job = None
        
        # Priority 3: Default fallback
        if not scheduled_job:
            default_hours = 24
            scheduled_job = schedule.every(default_hours).hours.do(job)
            self.logger.info(f"Scheduled client {client_name} with default interval: {default_hours} hours")
        
        if scheduled_job:
            self.scheduled_jobs[client_id] = scheduled_job
            return True
        else:
            self.logger.error(f"Failed to schedule client {client_name}")
            return False
    
    def _schedule_with_cron(self, cron_expression, job_func):
        """
        Schedule a job using cron-like expression
        
        Args:
            cron_expression (str): Cron expression (e.g., "0 9 * * 1-5")
            job_func: Function to execute
            
        Returns:
            Scheduled job object
            
        Note: This is a simplified cron parser for common cases.
        Full cron expressions: minute hour day_of_month month day_of_week
        """
        try:
            parts = cron_expression.strip().split()
            if len(parts) != 5:
                raise ValueError(f"Invalid cron format. Expected 5 parts, got {len(parts)}")
            
            minute, hour, day_of_month, month, day_of_week = parts
            
            # Handle common patterns
            
            # Daily at specific time: "0 9 * * *" (9 AM daily)
            if day_of_week == "*" and day_of_month == "*" and month == "*":
                if minute == "0" and hour.isdigit():
                    time_str = f"{hour:0>2}:00"
                    return schedule.every().day.at(time_str).do(job_func)
                elif minute.isdigit() and hour.isdigit():
                    time_str = f"{hour:0>2}:{minute:0>2}"
                    return schedule.every().day.at(time_str).do(job_func)
            
            # Weekday scheduling: "0 9 * * 1-5" (9 AM Monday-Friday)
            elif day_of_week == "1-5" and day_of_month == "*" and month == "*":
                if minute == "0" and hour.isdigit():
                    time_str = f"{hour:0>2}:00"
                    # Schedule for each weekday
                    jobs = []
                    jobs.append(schedule.every().monday.at(time_str).do(job_func))
                    jobs.append(schedule.every().tuesday.at(time_str).do(job_func))
                    jobs.append(schedule.every().wednesday.at(time_str).do(job_func))
                    jobs.append(schedule.every().thursday.at(time_str).do(job_func))
                    jobs.append(schedule.every().friday.at(time_str).do(job_func))
                    # Return the first job (they're all linked)
                    return jobs[0]
                    
            # Specific day of week: "0 9 * * 1" (9 AM every Monday)
            elif day_of_week.isdigit() and day_of_month == "*" and month == "*":
                day_names = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
                day_index = int(day_of_week)
                if 0 <= day_index <= 6:
                    day_name = day_names[day_index]
                    if minute == "0" and hour.isdigit():
                        time_str = f"{hour:0>2}:00"
                        return getattr(schedule.every(), day_name).at(time_str).do(job_func)
            
            # Hourly: "0 * * * *" (every hour)
            elif minute == "0" and hour == "*":
                return schedule.every().hour.do(job_func)
            
            # Every X hours: "0 */6 * * *" (every 6 hours)
            elif minute == "0" and hour.startswith("*/"):
                interval = int(hour[2:])
                return schedule.every(interval).hours.do(job_func)
            
            # Every X minutes: "*/30 * * * *" (every 30 minutes)
            elif minute.startswith("*/") and hour == "*":
                interval = int(minute[2:])
                return schedule.every(interval).minutes.do(job_func)
            
            # Fallback: treat as daily if we can't parse
            else:
                self.logger.warning(f"Complex cron expression '{cron_expression}' not fully supported, falling back to daily schedule")
                if hour.isdigit():
                    time_str = f"{hour:0>2}:00"
                    return schedule.every().day.at(time_str).do(job_func)
                else:
                    return schedule.every().day.do(job_func)
                    
        except Exception as e:
            raise ValueError(f"Failed to parse cron expression '{cron_expression}': {e}")
        
    def schedule_all_clients(self, headless=True):
        """
        Schedule all enabled clients for regular scraping
        
        Args:
            headless (bool): Whether to run in headless mode
        """
        scheduled_count = 0
        skipped_count = 0
        
        for client_id, client_config in self.manager.clients.items():
            if not client_config.get("enabled", True):
                skipped_count += 1
                self.logger.info(f"Skipping disabled client: {client_id}")
                continue
                
            if self.schedule_client(client_id, headless):
                scheduled_count += 1
                
        self.logger.info(f"Scheduled {scheduled_count} clients, skipped {skipped_count} disabled clients")
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
            
        client_config = self.manager.clients[client_id]
        client_name = client_config.get("name", client_id)
        
        # Check if client is enabled
        if not client_config.get("enabled", True):
            self.logger.warning(f"Client {client_name} is disabled but running anyway (manual override)")
        
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
        Run scraper for all enabled clients immediately
        
        Args:
            headless (bool): Whether to run in headless mode
        """
        def run_async():
            self.logger.info("Running immediate scraper for all enabled clients")
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
            "enabled_clients": 0,
            "disabled_clients": 0,
            "scheduled_clients": len(self.scheduled_jobs),
            "clients": [],
            "next_runs": []
        }
        
        for client_id, client_config in self.manager.clients.items():
            client_name = client_config.get("name", client_id)
            enabled = client_config.get("enabled", True)
            
            if enabled:
                status["enabled_clients"] += 1
            else:
                status["disabled_clients"] += 1
            
            # Get scheduling information
            schedule_info = "Not scheduled"
            schedule_type = "None"
            
            if client_id in self.scheduled_jobs:
                job = self.scheduled_jobs[client_id]
                next_run = job.next_run
                
                # Determine schedule type and info
                if "schedule" in client_config and client_config["schedule"]:
                    schedule_type = "Cron"
                    schedule_info = f"Cron: {client_config['schedule']}"
                elif "schedule_interval_hours" in client_config:
                    hours = client_config["schedule_interval_hours"]
                    schedule_type = "Interval"
                    schedule_info = f"Every {hours} hours"
                else:
                    schedule_type = "Default"
                    schedule_info = "Every 24 hours (default)"
                
                if next_run:
                    status["next_runs"].append({
                        "client_id": client_id,
                        "client_name": client_name,
                        "next_run": next_run.strftime("%Y-%m-%d %H:%M:%S"),
                        "schedule_type": schedule_type,
                        "schedule_info": schedule_info
                    })
            
            status["clients"].append({
                "client_id": client_id,
                "client_name": client_name,
                "enabled": enabled,
                "scheduled": client_id in self.scheduled_jobs,
                "schedule_type": schedule_type,
                "schedule_info": schedule_info
            })
        
        # Sort by next run time
        status["next_runs"].sort(key=lambda x: x["next_run"])
        
        return status
        
    def print_schedule_status(self):
        """Print the current schedule status"""
        status = self.get_schedule_status()
        
        print(f"\n{'='*80}")
        print("MULTI-CLIENT SCHEDULER STATUS")
        print(f"{'='*80}")
        print(f"Total clients: {status['total_clients']}")
        print(f"Enabled clients: {status['enabled_clients']}")
        print(f"Disabled clients: {status['disabled_clients']}")
        print(f"Scheduled clients: {status['scheduled_clients']}")
        print()
        
        # Show client details
        print("CLIENT DETAILS:")
        print("-" * 80)
        for client in status["clients"]:
            status_icon = "✅" if client["enabled"] else "❌"
            scheduled_icon = "⏰" if client["scheduled"] else "⏸️"
            
            print(f"{status_icon} {scheduled_icon} {client['client_name']} ({client['client_id']})")
            print(f"    Schedule: {client['schedule_info']}")
            print()
        
        # Show next runs
        if status["next_runs"]:
            print("NEXT SCHEDULED RUNS:")
            print("-" * 80)
            for run_info in status["next_runs"]:
                print(f"📅 {run_info['next_run']} - {run_info['client_name']} ({run_info['schedule_type']})")
        else:
            print("No clients scheduled")
            
        print(f"{'='*80}")
            
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