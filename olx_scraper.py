#!/usr/bin/env python3
"""
OLX Job Scraper - Extracts manufacturing job listings and sends to GoHighLevel

This script scrapes job listings from OLX.pl, filters for manufacturing companies
(excluding employment agencies), extracts company name, position, and phone number,
and sends the data to GoHighLevel as contacts.
"""

import os
import time
import json
import re
import logging
import argparse
from datetime import datetime
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("olx_scraper.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class OLXScraper:
    """Scrapes job listings from OLX.pl and sends data to GoHighLevel"""
    
    def __init__(self, headless=True, gohighlevel_api_key=None):
        """Initialize the scraper with browser options and API key"""
        self.headless = headless
        self.gohighlevel_api_key = gohighlevel_api_key
        self.driver = None
        self.base_url = "https://www.olx.pl/praca/produkcja/"
        self.results = []
        
        # Keywords to identify manufacturing companies
        self.manufacturing_keywords = [
            "producent", "produkcja", "fabryka", "zakład", "meble", 
            "automotive", "przemysł", "wytwórnia", "huta", "manufaktura"
        ]
        
        # Keywords to identify employment agencies
        self.agency_keywords = [
            "agencja pracy", "agencja zatrudnienia", "agencja pośrednictwa", 
            "rekrutacja", "hr", "human resources", "outsourcing", "leasing pracowniczy"
        ]
        
    def setup_driver(self):
        """Set up the Chrome WebDriver with appropriate options"""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--allow-running-insecure-content")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36")
        
        # Use the system ChromeDriver
        chrome_options.binary_location = "/usr/bin/chromium-browser"
        service = Service("/usr/local/bin/chromedriver")
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.implicitly_wait(10)
        
    def close_driver(self):
        """Close the WebDriver"""
        if self.driver:
            self.driver.quit()
            
    def accept_cookies(self):
        """Accept cookies if the dialog appears"""
        try:
            cookie_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Akceptuję')]"))
            )
            cookie_button.click()
            logger.info("Accepted cookies")
        except TimeoutException:
            logger.info("No cookie dialog found or already accepted")
            
    def is_manufacturing_company(self, description):
        """
        Check if the job listing is from a manufacturing company
        
        Args:
            description (str): The job description text
            
        Returns:
            bool: True if it appears to be a manufacturing company, False otherwise
        """
        description_lower = description.lower()
        
        # Check for agency keywords first (exclusion)
        for keyword in self.agency_keywords:
            if keyword in description_lower:
                return False
                
        # Then check for manufacturing keywords
        for keyword in self.manufacturing_keywords:
            if keyword in description_lower:
                return True
                
        # If no clear indicators, do additional checks
        # Look for manufacturing processes or equipment
        manufacturing_indicators = [
            "produkcyjn", "maszyn", "linia produkcyjna", "operator", "monter",
            "spawacz", "tokarz", "ślusarz", "lakiernik", "magazyn", "magazynier"
        ]
        
        for indicator in manufacturing_indicators:
            if indicator in description_lower:
                return True
                
        return False
        
    def extract_phone_number(self):
        """
        Click the Call/SMS button and extract the phone number
        
        Returns:
            str: The extracted phone number or None if not found
        """
        try:
            # Find and click the Call/SMS button
            call_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Zadzwoń') or contains(text(), 'SMS')]"))
            )
            call_button.click()
            time.sleep(1)  # Wait for the number to appear
            
            # Extract the phone number
            phone_element = self.driver.find_element(By.XPATH, "//button[contains(@class, 'phone')] | //a[contains(@class, 'phone')]")
            phone_number = phone_element.text.strip()
            
            # Clean up the phone number
            phone_number = re.sub(r'\s+', '', phone_number)
            return phone_number
            
        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"Failed to extract phone number: {str(e)}")
            return None
            
    def extract_company_name(self):
        """
        Extract the company name from the job listing
        
        Returns:
            str: The company name or None if not found
        """
        try:
            # Try to find company name in the recruiter section
            company_element = self.driver.find_element(By.XPATH, "//div[contains(@class, 'recruiter')]//*[contains(@class, 'title')]")
            return company_element.text.strip()
        except NoSuchElementException:
            # Try alternative methods
            try:
                # Look for company name in the description
                description = self.driver.find_element(By.XPATH, "//div[contains(@class, 'description')]").text
                # Extract company name using regex patterns
                patterns = [
                    r'Firma\s+([A-Za-z0-9\s]+)(?:\s+to|\s+jest|\s+poszukuje)',
                    r'([A-Za-z0-9\s]+)(?:\s+to firma|\s+jest firmą)',
                    r'O\s+([A-Za-z0-9\s]+)(?:\s+Jesteśmy|\s+to)'
                ]
                
                for pattern in patterns:
                    match = re.search(pattern, description)
                    if match:
                        return match.group(1).strip()
                        
                # If no match found, return None
                return None
                
            except NoSuchElementException:
                return None
                
    def extract_position(self):
        """
        Extract the job position title
        
        Returns:
            str: The job position title or None if not found
        """
        try:
            title_element = self.driver.find_element(By.XPATH, "//h1[contains(@class, 'title')]")
            return title_element.text.strip()
        except NoSuchElementException:
            return None
            
    def process_listing(self, url):
        """
        Process a single job listing
        
        Args:
            url (str): The URL of the job listing
            
        Returns:
            dict: The extracted data or None if not a manufacturing company
        """
        try:
            self.driver.get(url)
            time.sleep(2)  # Wait for page to load
            
            # Extract job description to check if it's a manufacturing company
            description = self.driver.find_element(By.XPATH, "//div[contains(@class, 'description') or contains(@id, 'description')]").text
            
            if not self.is_manufacturing_company(description):
                logger.info(f"Skipping non-manufacturing company: {url}")
                return None
                
            # Extract data
            company_name = self.extract_company_name()
            position = self.extract_position()
            phone_number = self.extract_phone_number()
            
            if not company_name:
                logger.warning(f"Could not extract company name for {url}")
                company_name = "Unknown Company"
                
            if not position:
                logger.warning(f"Could not extract position for {url}")
                position = "Unknown Position"
                
            if not phone_number:
                logger.warning(f"Could not extract phone number for {url}")
                return None  # Skip if no phone number
                
            data = {
                "company_name": company_name,
                "position": position,
                "phone_number": phone_number,
                "source": "OLX",
                "url": url,
                "date_collected": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            logger.info(f"Extracted data: {data}")
            return data
            
        except Exception as e:
            logger.error(f"Error processing listing {url}: {str(e)}")
            return None
            
    def get_listing_urls(self, page=1, max_pages=10):
        """
        Get URLs of job listings from the search results
        
        Args:
            page (int): The starting page number
            max_pages (int): Maximum number of pages to scrape
            
        Returns:
            list: List of job listing URLs
        """
        urls = []
        current_page = page
        
        while current_page <= max_pages:
            try:
                if current_page == 1:
                    page_url = self.base_url
                else:
                    page_url = f"{self.base_url}?page={current_page}"
                    
                logger.info(f"Visiting page: {page_url}")
                self.driver.get(page_url)
                time.sleep(3)  # Wait for page to load
                
                # Accept cookies if needed
                if current_page == 1:
                    self.accept_cookies()
                    time.sleep(2)
                    
                # Find all job listing links - try multiple selectors
                listing_elements = []
                
                # Try different selectors for job listings
                selectors = [
                    "a[data-cy='listing-ad-title']",
                    "a[data-testid='listing-ad-title']",
                    "h3 a",
                    "h4 a",
                    "h6 a",
                    ".title a",
                    "[data-cy='l-card'] a",
                    ".offer-item a"
                ]
                
                for selector in selectors:
                    try:
                        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        if elements:
                            listing_elements = elements
                            logger.info(f"Found elements using selector: {selector}")
                            break
                    except Exception as e:
                        logger.debug(f"Selector {selector} failed: {e}")
                        continue
                
                # If no elements found with CSS selectors, try XPath
                if not listing_elements:
                    xpath_selectors = [
                        "//a[contains(@href, '/oferta/')]",
                        "//a[contains(text(), 'Operator') or contains(text(), 'Pracownik') or contains(text(), 'Produkcja')]"
                    ]
                    
                    for xpath in xpath_selectors:
                        try:
                            elements = self.driver.find_elements(By.XPATH, xpath)
                            if elements:
                                listing_elements = elements
                                logger.info(f"Found elements using XPath: {xpath}")
                                break
                        except Exception as e:
                            logger.debug(f"XPath {xpath} failed: {e}")
                            continue
                
                page_urls = []
                for element in listing_elements:
                    try:
                        url = element.get_attribute("href")
                        if url and "olx.pl/oferta" in url and "/praca/" in url:
                            page_urls.append(url)
                    except Exception as e:
                        logger.debug(f"Error getting URL from element: {e}")
                        continue
                        
                urls.extend(page_urls)
                logger.info(f"Found {len(page_urls)} job listings on page {current_page}")
                
                # If no listings found, log page source for debugging
                if not page_urls and current_page == 1:
                    logger.warning("No listings found on first page. Checking page content...")
                    page_source = self.driver.page_source
                    if "produkcja" in page_source.lower():
                        logger.info("Page contains 'produkcja' keyword")
                    else:
                        logger.warning("Page does not contain 'produkcja' keyword")
                
                # Check if there's a next page
                try:
                    next_button = self.driver.find_element(By.XPATH, "//a[contains(@data-cy, 'pagination-forward') or contains(@class, 'next')]")
                    if "disabled" in next_button.get_attribute("class") or not next_button.is_enabled():
                        logger.info("Reached last page")
                        break
                except NoSuchElementException:
                    logger.info("No more pages or pagination element not found")
                    break
                    
                current_page += 1
                
            except Exception as e:
                logger.error(f"Error getting listing URLs on page {current_page}: {str(e)}")
                break
                
        return urls
        
    def send_to_gohighlevel(self, data):
        """
        Send the extracted data to GoHighLevel API
        
        Args:
            data (dict): The data to send
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.gohighlevel_api_key:
            logger.warning("No GoHighLevel API key provided, skipping API call")
            return False
            
        try:
            api_url = "https://rest.gohighlevel.com/v1/contacts/"
            headers = {
                "Authorization": f"Bearer {self.gohighlevel_api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "name": data["company_name"],
                "phone": data["phone_number"],
                "customField": {
                    "position": data["position"],
                    "source": data["source"],
                    "url": data["url"],
                    "date_collected": data["date_collected"]
                }
            }
            
            response = requests.post(api_url, headers=headers, json=payload)
            
            if response.status_code in (200, 201):
                logger.info(f"Successfully sent data to GoHighLevel: {data['company_name']}")
                return True
            else:
                logger.error(f"Failed to send data to GoHighLevel: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending data to GoHighLevel: {str(e)}")
            return False
            
    def run(self, max_pages=10, max_listings=100):
        """
        Run the scraper
        
        Args:
            max_pages (int): Maximum number of pages to scrape
            max_listings (int): Maximum number of listings to process
            
        Returns:
            list: The scraped data
        """
        try:
            self.setup_driver()
            
            # Get listing URLs
            listing_urls = self.get_listing_urls(max_pages=max_pages)
            logger.info(f"Found {len(listing_urls)} total listings")
            
            # Process each listing
            count = 0
            for url in listing_urls:
                if count >= max_listings:
                    logger.info(f"Reached maximum number of listings ({max_listings})")
                    break
                    
                data = self.process_listing(url)
                if data:
                    self.results.append(data)
                    
                    # Send to GoHighLevel
                    if self.gohighlevel_api_key:
                        self.send_to_gohighlevel(data)
                        
                    count += 1
                    
                # Add a small delay between requests
                time.sleep(1)
                
            logger.info(f"Processed {count} listings, found {len(self.results)} manufacturing companies")
            
            # Save results to file
            with open("olx_results.json", "w", encoding="utf-8") as f:
                json.dump(self.results, f, ensure_ascii=False, indent=2)
                
            return self.results
            
        finally:
            self.close_driver()
            
def main():
    """Main function to run the scraper"""
    # Get defaults from environment variables
    default_headless = os.getenv("HEADLESS", "true").lower() == "true"
    default_api_key = os.getenv("GOHIGHLEVEL_API_KEY")
    default_max_pages = int(os.getenv("MAX_PAGES", "5"))
    default_max_listings = int(os.getenv("MAX_LISTINGS", "50"))
    
    parser = argparse.ArgumentParser(description="OLX Job Scraper")
    parser.add_argument("--headless", action="store_true", default=default_headless, help="Run in headless mode")
    parser.add_argument("--api-key", default=default_api_key, help="GoHighLevel API key")
    parser.add_argument("--max-pages", type=int, default=default_max_pages, help="Maximum number of pages to scrape")
    parser.add_argument("--max-listings", type=int, default=default_max_listings, help="Maximum number of listings to process")
    
    args = parser.parse_args()
    
    scraper = OLXScraper(headless=args.headless, gohighlevel_api_key=args.api_key)
    results = scraper.run(max_pages=args.max_pages, max_listings=args.max_listings)
    
    print(f"Found {len(results)} manufacturing companies")
    print(f"Results saved to olx_results.json")
    
if __name__ == "__main__":
    main()

