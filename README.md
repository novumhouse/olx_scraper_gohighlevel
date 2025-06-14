# OLX Job Scraper with GoHighLevel Integration

This application scrapes job listings from OLX.pl, filters for manufacturing companies (excluding employment agencies), extracts company name, position, and phone number, and sends the data to GoHighLevel as contacts.

## Features

- Scrapes job listings from OLX.pl's production jobs section
- Filters for manufacturing companies and excludes employment agencies
- Extracts company name, position, and phone number
- Sends data to GoHighLevel as contacts
- Scheduled execution at regular intervals

## Requirements

- Python 3.7+
- Chrome browser
- GoHighLevel API key (optional, for integration)

## Installation

1. Clone this repository or download the files
2. Install the required Python packages:

```bash
pip install -r requirements.txt
```

3. Make sure Chrome is installed on your system

## Usage

### Running the Scraper

To run the scraper once:

```bash
python olx_scraper.py [options]
```

Options:
- `--headless`: Run in headless mode (no browser UI)
- `--api-key API_KEY`: GoHighLevel API key for direct integration
- `--max-pages MAX_PAGES`: Maximum number of pages to scrape (default: 5)
- `--max-listings MAX_LISTINGS`: Maximum number of listings to process (default: 50)

Example:
```bash
python olx_scraper.py --headless --max-pages 10 --max-listings 100
```

### GoHighLevel Integration

To send scraped data to GoHighLevel:

```bash
python gohighlevel_integration.py --api-key API_KEY [--input-file INPUT_FILE]
```

Options:
- `--api-key API_KEY`: GoHighLevel API key (required)
- `--input-file INPUT_FILE`: Input JSON file with contact data (default: olx_results.json)

Example:
```bash
python gohighlevel_integration.py --api-key your_api_key_here
```

### Scheduling

To schedule the scraper to run at regular intervals:

```bash
python scheduler.py [options]
```

Options:
- `--interval HOURS`: Interval in hours (default: 24)
- `--headless`: Run in headless mode
- `--api-key API_KEY`: GoHighLevel API key
- `--max-pages MAX_PAGES`: Maximum number of pages to scrape (default: 5)
- `--max-listings MAX_LISTINGS`: Maximum number of listings to process (default: 50)
- `--run-now`: Run immediately in addition to scheduling

Example:
```bash
python scheduler.py --interval 12 --headless --api-key your_api_key_here --run-now
```

## Configuration

You can configure the application using command-line arguments or environment variables in a `.env` file.

### Environment Variables

Copy the `.env.example` file to `.env` and edit it:

```bash
cp .env.example .env
nano .env
```

Available environment variables:

```
# GoHighLevel API Key
GOHIGHLEVEL_API_KEY=your_api_key_here

# Scraper Settings
MAX_PAGES=5
MAX_LISTINGS=50
HEADLESS=true

# Scheduler Settings
INTERVAL_HOURS=24
```

Command-line arguments will override environment variables.

## Output

The scraper saves the results to `olx_results.json`. Each entry contains:
- Company name
- Position
- Phone number
- Source (OLX)
- URL
- Date collected

## Filtering Logic

The application identifies manufacturing companies using keywords such as:
- "producent" (manufacturer)
- "produkcja" (production)
- "fabryka" (factory)
- "zakład" (plant)
- Industry-specific terms like "meble" (furniture), "automotive", etc.

It excludes employment agencies by looking for keywords like:
- "agencja pracy" (employment agency)
- "agencja zatrudnienia" (recruitment agency)
- "agencja pośrednictwa pracy" (job placement agency)

## Logs

The application creates log files:
- `olx_scraper.log`: Logs from the scraper
- `gohighlevel.log`: Logs from the GoHighLevel integration
- `scheduler.log`: Logs from the scheduler

## Troubleshooting

### Common Issues

1. **Selenium WebDriver issues**:
   - Make sure Chrome is installed
   - Try updating the webdriver-manager: `pip install --upgrade webdriver-manager`

2. **GoHighLevel API errors**:
   - Verify your API key is correct
   - Check the GoHighLevel API documentation for any changes

3. **Rate limiting**:
   - If you're getting blocked by OLX, try increasing the delay between requests
   - Use a proxy rotation service for large-scale scraping

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is for educational purposes only. Use it responsibly and in accordance with OLX.pl's terms of service. The developers are not responsible for any misuse of this tool.

