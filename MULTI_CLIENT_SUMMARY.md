# Multi-Client OLX Scraper Solution

## Problem Solved
You needed to use your OLX scraper application for multiple clients. The original application was designed for single-client usage with global configuration.

## Solution: Configuration-Based Multi-Client System

I've created a **simple, scalable solution** that allows you to manage multiple clients through JSON configuration files. This is the **best practice** for multi-client applications because it:

- ✅ **Separates client data** completely
- ✅ **Scales easily** - add clients by editing a config file
- ✅ **Maintains security** - separate API keys per client
- ✅ **Provides flexibility** - different settings per client
- ✅ **Keeps it simple** - no database or complex setup required

## What I Created

### 1. **clients_config.json** - Client Configuration
```json
{
  "clients": {
    "client1": {
      "name": "Manufacturing Solutions Ltd",
      "gohighlevel_api_key": "your_api_key_here",
      "search_keywords": ["producent", "produkcja", "fabryka"],
      "max_pages": 5,
      "max_listings": 50,
      "schedule_interval_hours": 24,
      "output_file": "results_client1.json",
      "log_file": "client1_scraper.log"
    }
  }
}
```

### 2. **multi_client_scraper.py** - Main Multi-Client Manager
- Loads client configurations
- Runs scraper for specific clients or all clients
- Manages separate log files and result files
- Integrates with GoHighLevel per client

### 3. **multi_client_scheduler.py** - Multi-Client Scheduler
- Schedules different clients at different intervals
- Supports immediate runs and status checking
- Runs clients in parallel without blocking

### 4. **MULTI_CLIENT_SETUP_GUIDE.md** - Complete Setup Guide
- Step-by-step installation instructions
- Usage examples and best practices
- Troubleshooting guide
- Migration instructions from single-client setup

## Key Features

### ✅ **Per-Client Configuration**
- Individual API keys for GoHighLevel
- Custom search keywords for targeting specific industries
- Different scraping limits (pages, listings)
- Separate scheduling intervals

### ✅ **Complete Data Separation**
- Each client gets their own result file
- Separate log files for debugging
- Client information tagged in results

### ✅ **Flexible Scheduling**
- Client1: Every 24 hours
- Client2: Every 12 hours  
- Client3: Every 48 hours
- Run specific clients on demand

### ✅ **Easy Management**
```bash
# List all clients
python3 multi_client_scraper.py --list

# Run specific client
python3 multi_client_scraper.py --client client1

# Run all clients
python3 multi_client_scraper.py --all

# Start scheduler
python3 multi_client_scheduler.py
```

## Why This Approach?

### 🎯 **Simplest Solution**
- No database setup required
- No complex architecture
- Easy to understand and maintain
- Quick to implement

### 🎯 **Best Practice**
- Configuration as code
- Separation of concerns
- Scalable architecture
- Production-ready

### 🎯 **Practical Benefits**
- Add clients by editing JSON
- Each client completely isolated
- Easy to debug individual clients
- Can run specific clients on demand

## Getting Started

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure your clients:**
   - Edit `clients_config.json`
   - Add your API keys
   - Set client-specific parameters

3. **Test the setup:**
   ```bash
   python3 multi_client_scraper.py --list
   python3 multi_client_scraper.py --client client1
   ```

4. **Set up scheduling:**
   ```bash
   python3 multi_client_scheduler.py
   ```

## File Structure After Setup
```
/workspace/
├── clients_config.json           # ← Your client configurations
├── multi_client_scraper.py       # ← Main multi-client manager
├── multi_client_scheduler.py     # ← Scheduler for all clients
├── results_client1.json          # ← Client1 results
├── results_client2.json          # ← Client2 results
├── client1_scraper.log           # ← Client1 logs
├── client2_scraper.log           # ← Client2 logs
└── MULTI_CLIENT_SETUP_GUIDE.md   # ← Complete setup guide
```

## Next Steps

1. **Read the setup guide:** `MULTI_CLIENT_SETUP_GUIDE.md`
2. **Update the client configuration** with your real API keys
3. **Test with one client** before running all clients
4. **Set up scheduling** for production use

This solution provides the **simplest way** to manage multiple clients while following **best practices** for scalability and maintainability.