#!/usr/bin/env python3
"""
Multi-Client OLX Scraper Manager

This script manages multiple clients for the OLX scraper.
Each client has their own configuration, API keys, and data storage.
"""

import os
import json
import logging
import argparse
import sys
from datetime import datetime
from olx_scraper import OLXScraper
from gohighlevel_integration import GoHighLevelAPI

class MultiClientScraperManager:
    """Manages multiple clients for the OLX scraper"""
    
    def __init__(self, config_file="clients_config.json"):
        """
        Initialize the multi-client manager
        
        Args:
            config_file (str): Path to the client configuration file
        """
        self.config_file = config_file
        self.clients = {}
        self.load_config()
        
    def load_config(self):
        """Load client configurations from JSON file"""
        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                config = json.load(f)
                
                # Handle both old and new configuration formats
                if "clients" in config:
                    # Old format: {"clients": {"client1": {...}}}
                    self.clients = config["clients"]
                    print(f"Loaded {len(self.clients)} client configurations (legacy format)")
                else:
                    # New format: {"client1": {...}, "client2": {...}}
                    self.clients = config
                    print(f"Loaded {len(self.clients)} client configurations")
                    
        except FileNotFoundError:
            print(f"Configuration file {self.config_file} not found")
            self.clients = {}
        except json.JSONDecodeError as e:
            print(f"Error parsing configuration file: {e}")
            self.clients = {}
            
    def get_client_logger(self, client_id, client_config):
        """
        Get a logger for a specific client
        
        Args:
            client_id (str): The client ID
            client_config (dict): The client configuration
            
        Returns:
            logging.Logger: Configured logger for the client
        """
        logger = logging.getLogger(f"client_{client_id}")
        
        # Clear any existing handlers
        logger.handlers.clear()
        
        # Set up logging for this client
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # File handler - support both old and new config format
        log_file = client_config.get("log_file", f"{client_id}_scraper.log")
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        logger.setLevel(logging.INFO)
        return logger
        
    def run_client_scraper(self, client_id, headless=True, test_mode=False):
        """
        Run the scraper for a specific client
        
        Args:
            client_id (str): The client ID
            headless (bool): Whether to run in headless mode
            test_mode (bool): Whether to run in test mode (no API calls)
            
        Returns:
            bool: True if successful, False otherwise
        """
        if client_id not in self.clients:
            print(f"Client {client_id} not found in configuration")
            return False
            
        client_config = self.clients[client_id]
        client_name = client_config.get("name", client_id)
        
        # Check if client is enabled (new format)
        if not client_config.get("enabled", True):
            print(f"Client {client_name} is disabled, skipping...")
            return True
        
        # Get client-specific logger
        logger = self.get_client_logger(client_id, client_config)
        
        logger.info(f"Starting scraper for client: {client_name}")
        
        if test_mode:
            logger.info("Running in TEST MODE - no API calls will be made")
        
        try:
            # Create a custom scraper instance for this client
            api_key = client_config.get("gohighlevel_api_key") if not test_mode else None
            location_id = client_config.get("gohighlevel_location_id") if not test_mode else None
            
            scraper = OLXScraper(
                headless=headless,
                gohighlevel_api_key=api_key,
                gohighlevel_location_id=location_id
            )
            
            # Handle search URLs (new format) or keywords (old format)
            search_urls = []
            if "olx_search_urls" in client_config:
                # New format: direct URLs
                search_urls = client_config["olx_search_urls"]
            elif "search_keywords" in client_config:
                # Old format: convert keywords to URLs
                keywords = client_config["search_keywords"]
                for keyword in keywords:
                    url = f"https://www.olx.pl/praca/q-{keyword}/?search%5Border%5D=created_at:desc"
                    search_urls.append(url)
            else:
                # Fallback to default URLs
                search_urls = ["https://www.olx.pl/praca/q-producent/?search%5Border%5D=created_at:desc"]
            
            # Set up keyword filtering (new format)
            if "keywords" in client_config:
                include_keywords = client_config["keywords"].get("include", [])
                exclude_keywords = client_config["keywords"].get("exclude", [])
                
                # Update scraper's keyword lists
                scraper.manufacturing_keywords.extend(include_keywords)
                scraper.exclusion_keywords.extend(exclude_keywords)
            elif "search_keywords" in client_config:
                # Old format compatibility
                scraper.manufacturing_keywords.extend(client_config["search_keywords"])
                
            # Run the scraper with client-specific settings
            max_pages = client_config.get("max_pages", 5)
            max_listings = client_config.get("max_listings", 50)
            delay = client_config.get("delay_between_requests", 2)
            
            results = []
            
            # Process each search URL
            for url in search_urls:
                logger.info(f"Processing URL: {url}")
                try:
                    url_results = scraper.run_custom_url(url, max_pages=max_pages, max_listings=max_listings)
                    results.extend(url_results)
                    
                    if delay > 0:
                        import time
                        time.sleep(delay)
                        
                except Exception as e:
                    logger.error(f"Error processing URL {url}: {str(e)}")
                    continue
            
            # Save results to client-specific file
            output_file = client_config.get("output_file", f"results_{client_id}.json")
            
            # Add client information to results
            for result in results:
                result["client_id"] = client_id
                result["client_name"] = client_name
                result["processed_at"] = datetime.now().isoformat()
                
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
                
            logger.info(f"Client {client_name}: Found {len(results)} results, saved to {output_file}")
            
            # Send to GoHighLevel if API key is provided and not in test mode
            if client_config.get("gohighlevel_api_key") and not test_mode:
                try:
                    ghl_api = GoHighLevelAPI(
                        client_config["gohighlevel_api_key"],
                        client_config.get("gohighlevel_location_id")
                    )
                    ghl_results = ghl_api.process_batch(results)
                    logger.info(f"GoHighLevel results for {client_name}: {ghl_results}")
                except Exception as e:
                    logger.error(f"GoHighLevel integration error for {client_name}: {str(e)}")
            elif test_mode:
                logger.info(f"TEST MODE: Would have sent {len(results)} results to GoHighLevel")
                
            return True
            
        except Exception as e:
            logger.error(f"Error running scraper for client {client_name}: {str(e)}")
            return False
            
    def run_all_clients(self, headless=True, test_mode=False):
        """
        Run the scraper for all enabled clients
        
        Args:
            headless (bool): Whether to run in headless mode
            test_mode (bool): Whether to run in test mode
            
        Returns:
            dict: Summary of results for all clients
        """
        results = {
            "total_clients": len(self.clients),
            "enabled_clients": 0,
            "successful": 0,
            "failed": 0,
            "skipped": 0,
            "failed_clients": []
        }
        
        for client_id, client_config in self.clients.items():
            # Check if client is enabled
            if not client_config.get("enabled", True):
                results["skipped"] += 1
                print(f"Skipping disabled client: {client_id}")
                continue
                
            results["enabled_clients"] += 1
            
            print(f"\n{'='*50}")
            print(f"Processing client: {client_id}")
            print(f"{'='*50}")
            
            success = self.run_client_scraper(client_id, headless, test_mode)
            
            if success:
                results["successful"] += 1
            else:
                results["failed"] += 1
                results["failed_clients"].append(client_id)
                
        return results
        
    def list_clients(self):
        """List all configured clients"""
        print("\nConfigured Clients:")
        print("-" * 70)
        
        for client_id, client_config in self.clients.items():
            name = client_config.get("name", "N/A")
            enabled = client_config.get("enabled", True)
            has_api_key = bool(client_config.get("gohighlevel_api_key"))
            has_location_id = bool(client_config.get("gohighlevel_location_id"))
            max_pages = client_config.get("max_pages", 5)
            schedule = client_config.get("schedule", "Not set")
            
            # Count search URLs or keywords
            url_count = 0
            if "olx_search_urls" in client_config:
                url_count = len(client_config["olx_search_urls"])
            elif "search_keywords" in client_config:
                url_count = len(client_config["search_keywords"])
            
            status = "✅ Enabled" if enabled else "❌ Disabled"
            api_status = "✅ Yes" if has_api_key else "❌ No"
            location_status = "✅ Yes" if has_location_id else "❌ No"
            
            print(f"ID: {client_id}")
            print(f"Name: {name}")
            print(f"Status: {status}")
            print(f"API Key: {api_status}")
            print(f"Location ID: {location_status}")
            print(f"Search URLs: {url_count}")
            print(f"Max Pages: {max_pages}")
            print(f"Schedule: {schedule}")
            print("-" * 70)
            
def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Multi-Client OLX Scraper Manager")
    parser.add_argument("--config", default="clients_config.json", help="Configuration file path")
    parser.add_argument("--client", help="Run scraper for specific client ID")
    parser.add_argument("--all", action="store_true", help="Run scraper for all enabled clients")
    parser.add_argument("--list", action="store_true", help="List all configured clients")
    parser.add_argument("--headless", action="store_true", default=True, help="Run in headless mode")
    parser.add_argument("--test-mode", action="store_true", help="Run in test mode (no API calls)")
    
    args = parser.parse_args()
    
    # Initialize the manager
    manager = MultiClientScraperManager(args.config)
    
    if args.list:
        manager.list_clients()
        return
        
    if args.client:
        success = manager.run_client_scraper(args.client, args.headless, args.test_mode)
        if success:
            print(f"\nScraper completed successfully for client: {args.client}")
        else:
            print(f"\nScraper failed for client: {args.client}")
            sys.exit(1)
            
    elif args.all:
        results = manager.run_all_clients(args.headless, args.test_mode)
        
        print(f"\n{'='*50}")
        print("SUMMARY")
        print(f"{'='*50}")
        print(f"Total clients: {results['total_clients']}")
        print(f"Enabled clients: {results['enabled_clients']}")
        print(f"Successful: {results['successful']}")
        print(f"Failed: {results['failed']}")
        print(f"Skipped (disabled): {results['skipped']}")
        
        if results['failed_clients']:
            print(f"Failed clients: {', '.join(results['failed_clients'])}")
            
    else:
        print("Please specify --client, --all, or --list")
        print("Use --help for more information")
        
if __name__ == "__main__":
    main()