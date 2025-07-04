# Multi-Client OLX Scraper Setup Guide

This guide explains how to set up and use the multi-client OLX scraper system, which allows you to manage multiple clients with different configurations, API keys, and scraping schedules.

## Overview

The multi-client system provides:
- **Separate configurations** for each client
- **Individual API keys** for GoHighLevel integration
- **Custom search keywords** per client
- **Different scraping schedules** for each client
- **Separate log files** and result files
- **Centralized management** of all clients

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Or if you're using a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Your Clients

Edit `clients_config.json` to add your client configurations:

```json
{
  "clients": {
    "client1": {
      "name": "Manufacturing Solutions Ltd",
      "gohighlevel_api_key": "your_actual_api_key_here",
      "search_keywords": ["producent", "produkcja", "fabryka"],
      "max_pages": 5,
      "max_listings": 50,
      "schedule_interval_hours": 24,
      "output_file": "results_client1.json",
      "log_file": "client1_scraper.log"
    },
    "client2": {
      "name": "Industrial Partners Inc",
      "gohighlevel_api_key": "another_api_key_here",
      "search_keywords": ["automotive", "przemysł", "wytwórnia"],
      "max_pages": 3,
      "max_listings": 30,
      "schedule_interval_hours": 12,
      "output_file": "results_client2.json",
      "log_file": "client2_scraper.log"
    }
  }
}
```

### 3. Test Your Setup

```bash
# List all configured clients
python3 multi_client_scraper.py --list

# Run scraper for a specific client
python3 multi_client_scraper.py --client client1

# Run scraper for all clients
python3 multi_client_scraper.py --all
```

## Configuration Options

### Client Configuration Parameters

| Parameter | Description | Default | Example |
|-----------|-------------|---------|---------|
| `name` | Human-readable client name | Client ID | "Manufacturing Solutions Ltd" |
| `gohighlevel_api_key` | GoHighLevel API key | None | "your_api_key_here" |
| `search_keywords` | Keywords to identify manufacturing companies | Default list | ["producent", "produkcja"] |
| `max_pages` | Maximum pages to scrape | 5 | 3 |
| `max_listings` | Maximum listings to process | 50 | 30 |
| `schedule_interval_hours` | Hours between scheduled runs | 24 | 12 |
| `output_file` | Results file name | "results_{client_id}.json" | "results_client1.json" |
| `log_file` | Log file name | "client_{client_id}_scraper.log" | "client1_scraper.log" |

### Search Keywords

Each client can have custom search keywords to target specific types of manufacturing companies:

```json
"search_keywords": [
  "producent",      // Producer
  "produkcja",      // Production
  "fabryka",        // Factory
  "automotive",     // Automotive
  "przemysł",       // Industry
  "wytwórnia",      // Manufacturing plant
  "meble",          // Furniture
  "huta",           // Foundry
  "manufaktura"     // Manufacture
]
```

## Usage Examples

### Running Individual Clients

```bash
# Run scraper for client1
python3 multi_client_scraper.py --client client1

# Run scraper for client2 with visible browser
python3 multi_client_scraper.py --client client2 --no-headless
```

### Running All Clients

```bash
# Run scraper for all clients
python3 multi_client_scraper.py --all

# Run scraper for all clients with visible browser
python3 multi_client_scraper.py --all --no-headless
```

### Scheduling

```bash
# Start the scheduler (runs continuously)
python3 multi_client_scheduler.py

# Start scheduler and run all clients immediately
python3 multi_client_scheduler.py --run-now

# Run a specific client immediately
python3 multi_client_scheduler.py --client client1

# Check schedule status
python3 multi_client_scheduler.py --status
```

## File Structure

After running the multi-client system, you'll have:

```
/workspace/
├── clients_config.json           # Client configurations
├── multi_client_scraper.py       # Main multi-client scraper
├── multi_client_scheduler.py     # Multi-client scheduler
├── results_client1.json          # Client1 results
├── results_client2.json          # Client2 results
├── client1_scraper.log           # Client1 logs
├── client2_scraper.log           # Client2 logs
├── multi_client_scheduler.log    # Scheduler logs
└── ...
```

## Best Practices

### 1. Client Naming
- Use descriptive client IDs (e.g., "manufacturing_corp", "automotive_ltd")
- Include company type in the name for easy identification

### 2. API Key Management
- Store API keys securely
- Use environment variables for sensitive keys:
  ```json
  "gohighlevel_api_key": "${GOHIGHLEVEL_API_KEY_CLIENT1}"
  ```

### 3. Scheduling
- Stagger client schedules to avoid overwhelming the server
- Consider different intervals based on client needs:
  - High-priority clients: 12 hours
  - Standard clients: 24 hours
  - Low-priority clients: 48 hours

### 4. Resource Management
- Monitor log files for errors
- Clean up old result files periodically
- Monitor system resources when running many clients

## Troubleshooting

### Common Issues

1. **"Client not found in configuration"**
   - Check that the client ID exists in `clients_config.json`
   - Verify JSON syntax is correct

2. **"No GoHighLevel API key provided"**
   - Add the API key to the client configuration
   - Check that the API key is valid

3. **Scraper fails to find listings**
   - Check the search keywords
   - Verify the OLX website structure hasn't changed
   - Check Chrome/ChromeDriver installation

### Log Analysis

Each client has its own log file:
```bash
# Check client1 logs
tail -f client1_scraper.log

# Check scheduler logs
tail -f multi_client_scheduler.log
```

### Performance Optimization

1. **Reduce resource usage:**
   ```json
   "max_pages": 3,
   "max_listings": 20
   ```

2. **Increase intervals for less active clients:**
   ```json
   "schedule_interval_hours": 48
   ```

3. **Use headless mode for production:**
   ```bash
   python3 multi_client_scraper.py --all --headless
   ```

## Advanced Usage

### Environment Variables

You can use environment variables in your configuration:

```bash
export GOHIGHLEVEL_API_KEY_CLIENT1="your_api_key_here"
export GOHIGHLEVEL_API_KEY_CLIENT2="another_api_key_here"
```

### Running as a Service

For production deployment, consider running the scheduler as a system service:

```bash
# Create a systemd service file
sudo nano /etc/systemd/system/olx-scraper.service

# Add service configuration
[Unit]
Description=OLX Multi-Client Scraper
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/workspace
ExecStart=/usr/bin/python3 multi_client_scheduler.py
Restart=always

[Install]
WantedBy=multi-user.target

# Enable and start the service
sudo systemctl enable olx-scraper
sudo systemctl start olx-scraper
```

## Migration from Single Client

If you're migrating from the single-client setup:

1. **Backup your existing configuration:**
   ```bash
   cp .env .env.backup
   ```

2. **Create client configuration:**
   ```json
   {
     "clients": {
       "existing_client": {
         "name": "Your Existing Client",
         "gohighlevel_api_key": "your_existing_api_key",
         "max_pages": 5,
         "max_listings": 50,
         "schedule_interval_hours": 24,
         "output_file": "olx_results.json",
         "log_file": "olx_scraper.log"
       }
     }
   }
   ```

3. **Test the migration:**
   ```bash
   python3 multi_client_scraper.py --client existing_client
   ```

## Support

For issues and questions:
1. Check the log files for error messages
2. Verify your configuration syntax with a JSON validator
3. Test with a single client before running all clients
4. Monitor system resources during execution

This multi-client system provides a scalable solution for managing multiple OLX scraping clients with minimal overhead and maximum flexibility.