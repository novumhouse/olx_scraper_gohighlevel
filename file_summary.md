# OLX Job Scraper with GoHighLevel Integration - File Summary

## Core Files

1. **olx_scraper.py**
   - Main scraper script that extracts job listings from OLX.pl
   - Filters for manufacturing companies and excludes employment agencies
   - Extracts company name, position, and phone number
   - Saves results to JSON file and can send directly to GoHighLevel

2. **gohighlevel_integration.py**
   - Handles integration with GoHighLevel API
   - Creates or updates contacts in GoHighLevel
   - Can be run separately to process previously scraped data

3. **scheduler.py**
   - Schedules the scraper to run at regular intervals
   - Uses the schedule library to manage timing
   - Can run immediately and then continue on schedule

## Configuration Files

4. **.env.example**
   - Template for environment variables
   - Copy to .env and edit with your settings
   - Includes GoHighLevel API key and scraper settings

5. **requirements.txt**
   - Lists all Python dependencies
   - Used by pip to install required packages

## Setup and Documentation

6. **setup.sh**
   - Shell script to set up the environment
   - Creates virtual environment
   - Installs dependencies
   - Makes scripts executable

7. **README.md**
   - Comprehensive documentation
   - Installation and usage instructions
   - Configuration options
   - Troubleshooting tips

8. **olx_scraper_analysis.md**
   - Analysis of OLX job listings structure
   - Data extraction strategy
   - Filtering criteria for manufacturing companies

## How to Use

1. Run the setup script:
   ```bash
   ./setup.sh
   ```

2. Edit the .env file with your GoHighLevel API key:
   ```bash
   nano .env
   ```

3. Run the scraper once:
   ```bash
   source venv/bin/activate
   ./olx_scraper.py
   ```

4. Or schedule it to run regularly:
   ```bash
   source venv/bin/activate
   ./scheduler.py --run-now
   ```

The application will scrape job listings from OLX.pl, filter for manufacturing companies, extract the required information, and send it to GoHighLevel as contacts.

