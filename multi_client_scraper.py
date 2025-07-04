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
                self.clients = config.get("clients", {})
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
        
        # File handler
        log_file = client_config.get("log_file", f"client_{client_id}_scraper.log")
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        logger.setLevel(logging.INFO)
        return logger
        
    def run_client_scraper(self, client_id, headless=True):
        """
        Run the scraper for a specific client
        
        Args:
            client_id (str): The client ID
            headless (bool): Whether to run in headless mode
            
        Returns:
            bool: True if successful, False otherwise
        """
        if client_id not in self.clients:
            print(f"Client {client_id} not found in configuration")
            return False
            
        client_config = self.clients[client_id]
        client_name = client_config.get("name", client_id)
        
        # Get client-specific logger
        logger = self.get_client_logger(client_id, client_config)
        
        logger.info(f"Starting scraper for client: {client_name}")
        
        try:
            # Create a custom scraper instance for this client
            scraper = OLXScraper(
                headless=headless,
                gohighlevel_api_key=client_config.get("gohighlevel_api_key")
            )
            
            # Override manufacturing keywords if specified
            if "search_keywords" in client_config:
                scraper.manufacturing_keywords = client_config["search_keywords"]
                
            # Run the scraper
            max_pages = client_config.get("max_pages", 5)
            max_listings = client_config.get("max_listings", 50)
            
            results = scraper.run(max_pages=max_pages, max_listings=max_listings)
            
            # Save results to client-specific file
            output_file = client_config.get("output_file", f"results_{client_id}.json")
            
            # Add client information to results
            for result in results:
                result["client_id"] = client_id
                result["client_name"] = client_name
                
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
                
            logger.info(f"Client {client_name}: Found {len(results)} results, saved to {output_file}")
            
            # Send to GoHighLevel if API key is provided
            if client_config.get("gohighlevel_api_key"):
                ghl_api = GoHighLevelAPI(client_config["gohighlevel_api_key"])
                ghl_results = ghl_api.process_batch(results)
                logger.info(f"GoHighLevel results for {client_name}: {ghl_results}")
                
            return True
            
        except Exception as e:
            logger.error(f"Error running scraper for client {client_name}: {str(e)}")
            return False
            
    def run_all_clients(self, headless=True):
        """
        Run the scraper for all clients
        
        Args:
            headless (bool): Whether to run in headless mode
            
        Returns:
            dict: Summary of results for all clients
        """
        results = {
            "total_clients": len(self.clients),
            "successful": 0,
            "failed": 0,
            "failed_clients": []
        }
        
        for client_id in self.clients:
            print(f"\n{'='*50}")
            print(f"Processing client: {client_id}")
            print(f"{'='*50}")
            
            success = self.run_client_scraper(client_id, headless)
            
            if success:
                results["successful"] += 1
            else:
                results["failed"] += 1
                results["failed_clients"].append(client_id)
                
        return results
        
    def list_clients(self):
        """List all configured clients"""
        print("\nConfigured Clients:")
        print("-" * 50)
        
        for client_id, client_config in self.clients.items():
            name = client_config.get("name", "N/A")
            has_api_key = bool(client_config.get("gohighlevel_api_key"))
            max_pages = client_config.get("max_pages", 5)
            max_listings = client_config.get("max_listings", 50)
            
            print(f"ID: {client_id}")
            print(f"Name: {name}")
            print(f"API Key: {'Yes' if has_api_key else 'No'}")
            print(f"Max Pages: {max_pages}")
            print(f"Max Listings: {max_listings}")
            print("-" * 30)
            
    def add_client(self, client_id, client_config):
        """
        Add a new client to the configuration
        
        Args:
            client_id (str): The client ID
            client_config (dict): The client configuration
        """
        self.clients[client_id] = client_config
        self.save_config()
        print(f"Added client: {client_id}")
        
    def remove_client(self, client_id):
        """
        Remove a client from the configuration
        
        Args:
            client_id (str): The client ID
        """
        if client_id in self.clients:
            del self.clients[client_id]
            self.save_config()
            print(f"Removed client: {client_id}")
        else:
            print(f"Client {client_id} not found")
            
    def save_config(self):
        """Save the current configuration to file"""
        try:
            config = {"clients": self.clients}
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            print(f"Configuration saved to {self.config_file}")
        except Exception as e:
            print(f"Error saving configuration: {e}")
            
def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Multi-Client OLX Scraper Manager")
    parser.add_argument("--config", default="clients_config.json", help="Configuration file path")
    parser.add_argument("--client", help="Run scraper for specific client ID")
    parser.add_argument("--all", action="store_true", help="Run scraper for all clients")
    parser.add_argument("--list", action="store_true", help="List all configured clients")
    parser.add_argument("--headless", action="store_true", default=True, help="Run in headless mode")
    
    args = parser.parse_args()
    
    # Initialize the manager
    manager = MultiClientScraperManager(args.config)
    
    if args.list:
        manager.list_clients()
        return
        
    if args.client:
        success = manager.run_client_scraper(args.client, args.headless)
        if success:
            print(f"\nScraper completed successfully for client: {args.client}")
        else:
            print(f"\nScraper failed for client: {args.client}")
            
    elif args.all:
        results = manager.run_all_clients(args.headless)
        
        print(f"\n{'='*50}")
        print("SUMMARY")
        print(f"{'='*50}")
        print(f"Total clients: {results['total_clients']}")
        print(f"Successful: {results['successful']}")
        print(f"Failed: {results['failed']}")
        
        if results['failed_clients']:
            print(f"Failed clients: {', '.join(results['failed_clients'])}")
            
    else:
        print("Please specify --client, --all, or --list")
        print("Use --help for more information")
        
if __name__ == "__main__":
    main()