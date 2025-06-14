#!/usr/bin/env python3
"""
GoHighLevel Integration Module

This module handles the integration with GoHighLevel API for creating contacts
from the data scraped from OLX job listings.
"""

import os
import json
import logging
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("gohighlevel.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class GoHighLevelAPI:
    """Handles integration with the GoHighLevel API"""
    
    def __init__(self, api_key):
        """
        Initialize the GoHighLevel API client
        
        Args:
            api_key (str): The GoHighLevel API key
        """
        self.api_key = api_key
        self.base_url = "https://rest.gohighlevel.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
    def create_contact(self, data):
        """
        Create a contact in GoHighLevel
        
        Args:
            data (dict): The contact data
            
        Returns:
            dict: The API response or None if failed
        """
        try:
            url = f"{self.base_url}/contacts/"
            
            # Format the payload according to GoHighLevel API requirements
            payload = {
                "name": data["company_name"],
                "phone": data["phone_number"],
                "type": "lead",  # Mark as a lead
                "source": "OLX Scraper",
                "tags": ["OLX", "Manufacturing", "Job Listing"],
                "customField": {}
            }
            
            # Add custom fields
            if "position" in data:
                payload["customField"]["position"] = data["position"]
                
            if "url" in data:
                payload["customField"]["source_url"] = data["url"]
                
            if "date_collected" in data:
                payload["customField"]["date_collected"] = data["date_collected"]
                
            # Add notes with additional information
            notes = f"Position: {data.get('position', 'N/A')}\n"
            notes += f"Source: OLX\n"
            notes += f"URL: {data.get('url', 'N/A')}\n"
            notes += f"Date Collected: {data.get('date_collected', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}"
            
            payload["notes"] = notes
            
            # Make the API request
            response = requests.post(url, headers=self.headers, json=payload)
            
            if response.status_code in (200, 201):
                logger.info(f"Successfully created contact: {data['company_name']}")
                return response.json()
            else:
                logger.error(f"Failed to create contact: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error creating contact: {str(e)}")
            return None
            
    def search_contact(self, phone):
        """
        Search for a contact by phone number
        
        Args:
            phone (str): The phone number to search for
            
        Returns:
            dict: The contact data or None if not found
        """
        try:
            url = f"{self.base_url}/contacts/lookup?phone={phone}"
            
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("contacts") and len(data["contacts"]) > 0:
                    logger.info(f"Found existing contact with phone: {phone}")
                    return data["contacts"][0]
                else:
                    logger.info(f"No existing contact found with phone: {phone}")
                    return None
            else:
                logger.error(f"Failed to search contact: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error searching contact: {str(e)}")
            return None
            
    def update_contact(self, contact_id, data):
        """
        Update an existing contact in GoHighLevel
        
        Args:
            contact_id (str): The ID of the contact to update
            data (dict): The updated contact data
            
        Returns:
            dict: The API response or None if failed
        """
        try:
            url = f"{self.base_url}/contacts/{contact_id}"
            
            # Format the payload according to GoHighLevel API requirements
            payload = {
                "customField": {}
            }
            
            # Add custom fields
            if "position" in data:
                payload["customField"]["position"] = data["position"]
                
            if "url" in data:
                payload["customField"]["source_url"] = data["url"]
                
            if "date_collected" in data:
                payload["customField"]["date_collected"] = data["date_collected"]
                
            # Add notes with additional information
            notes = f"Position: {data.get('position', 'N/A')}\n"
            notes += f"Source: OLX\n"
            notes += f"URL: {data.get('url', 'N/A')}\n"
            notes += f"Date Collected: {data.get('date_collected', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}"
            
            payload["notes"] = notes
            
            # Make the API request
            response = requests.put(url, headers=self.headers, json=payload)
            
            if response.status_code == 200:
                logger.info(f"Successfully updated contact: {contact_id}")
                return response.json()
            else:
                logger.error(f"Failed to update contact: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error updating contact: {str(e)}")
            return None
            
    def create_or_update_contact(self, data):
        """
        Create a new contact or update an existing one
        
        Args:
            data (dict): The contact data
            
        Returns:
            dict: The API response or None if failed
        """
        # Clean the phone number
        phone = data["phone_number"].replace(" ", "").replace("-", "")
        
        # Search for existing contact
        existing_contact = self.search_contact(phone)
        
        if existing_contact:
            # Update existing contact
            return self.update_contact(existing_contact["id"], data)
        else:
            # Create new contact
            return self.create_contact(data)
            
    def process_batch(self, data_list):
        """
        Process a batch of contacts
        
        Args:
            data_list (list): List of contact data dictionaries
            
        Returns:
            dict: Summary of the results
        """
        results = {
            "total": len(data_list),
            "success": 0,
            "failed": 0,
            "skipped": 0
        }
        
        for data in data_list:
            if not data.get("phone_number"):
                logger.warning(f"Skipping record without phone number: {data}")
                results["skipped"] += 1
                continue
                
            response = self.create_or_update_contact(data)
            
            if response:
                results["success"] += 1
            else:
                results["failed"] += 1
                
        return results
        
def load_data_from_file(filename):
    """
    Load data from a JSON file
    
    Args:
        filename (str): The name of the file to load
        
    Returns:
        list: The loaded data or empty list if failed
    """
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading data from {filename}: {str(e)}")
        return []
        
def main():
    """Main function to demonstrate the usage"""
    import argparse
    
    # Get default API key from environment variable
    default_api_key = os.getenv("GOHIGHLEVEL_API_KEY")
    
    parser = argparse.ArgumentParser(description="GoHighLevel Integration")
    parser.add_argument("--api-key", default=default_api_key, help="GoHighLevel API key")
    parser.add_argument("--input-file", default="olx_results.json", help="Input JSON file with contact data")
    
    args = parser.parse_args()
    
    if not args.api_key:
        logger.error("No API key provided. Please provide an API key using --api-key or set GOHIGHLEVEL_API_KEY in .env file.")
        return
    
    # Load data from file
    data_list = load_data_from_file(args.input_file)
    
    if not data_list:
        logger.error(f"No data found in {args.input_file}")
        return
        
    # Process the data
    api = GoHighLevelAPI(args.api_key)
    results = api.process_batch(data_list)
    
    # Print summary
    print(f"Total records: {results['total']}")
    print(f"Successfully processed: {results['success']}")
    print(f"Failed: {results['failed']}")
    print(f"Skipped: {results['skipped']}")
    
if __name__ == "__main__":
    main()

