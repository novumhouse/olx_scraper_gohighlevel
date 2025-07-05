# ✅ Complete OLX Scraper Workflow - Ready to Use!

## 🎯 Current Setup Status

✅ **Hetzner Server**: Running with 3-hour schedule (every 3 hours, 24/7)  
✅ **GitHub SSH**: Configured and working  
✅ **Service**: `olx-multi-scraper` active and running  
✅ **Configuration**: JobsEU client with real API credentials  
✅ **Private Repository**: Connected to `novumhouse/olx-scraper-private`  

## 🚀 Adding New Clients (Simple 3-Step Process)

### Step 1: Configure Locally
```bash
# Edit your private repository configuration
cd olx-scraper-private
nano config/clients_config.json
```

Add your new client:
```json
{
  "client1": {
    "name": "JobsEU",
    "gohighlevel_api_key": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "schedule": "0 */3 * * *",
    "enabled": true
  },
  "client2": {
    "name": "Your New Client",
    "gohighlevel_api_key": "YOUR_NEW_CLIENT_API_KEY",
    "gohighlevel_location_id": "YOUR_NEW_LOCATION_ID",
    "olx_search_urls": [
      "https://www.olx.pl/praca/q-automotive/?search%5Border%5D=created_at:desc"
    ],
    "keywords": {
      "include": ["automotive", "samochodowy", "motoryzacja"],
      "exclude": ["agencja", "pośrednictwo", "hr"]
    },
    "schedule": "0 */6 * * *",
    "enabled": true,
    "max_pages": 3,
    "delay_between_requests": 2
  }
}
```

### Step 2: Test and Commit
```bash
# Test locally
python3 multi_client_scraper.py --client client2 --headless

# Commit changes
git add config/clients_config.json
git commit -m "Add new client: Your New Client"
git push origin master
```

### Step 3: Deploy to Production
```bash
# Run automated deployment
./deployment/deploy.sh
```

**That's it!** Your new client is now running every 6 hours on the Hetzner server.

## 📊 Monitoring Your Clients

### Quick Status Check
```bash
# Service status
ssh hetzner "systemctl status olx-multi-scraper"

# List all clients
ssh hetzner "cd /opt/olx-scraper && python3 multi_client_scraper.py --list"

# Live logs
ssh hetzner "tail -f /opt/olx-scraper/logs/multi_client_scheduler.log"
```

### Check Results
```bash
# View scraped results
ssh hetzner "ls -la /opt/olx-scraper/results_*.json"

# Check specific client results
ssh hetzner "cat /opt/olx-scraper/results_client2.json | head -20"
```

## 🔧 Updating Application Code

### Option 1: Code Changes Only
```bash
# 1. Update public repository
cd olx_scraper_gohighlevel
# Make your changes to multi_client_scraper.py, etc.
git add . && git commit -m "Improve scraping logic" && git push

# 2. Update private repository
cd olx-scraper-private
# Copy updated files or pull changes
git add . && git commit -m "Update application code" && git push

# 3. Deploy
./deployment/deploy.sh
```

### Option 2: Configuration Changes Only
```bash
# 1. Edit configuration
cd olx-scraper-private
nano config/clients_config.json

# 2. Deploy
git add . && git commit -m "Update client schedules" && git push
./deployment/deploy.sh
```

## 🔄 Current Schedule (After Our Updates)

- **JobsEU**: Every 3 hours (00:00, 03:00, 06:00, 09:00, 12:00, 15:00, 18:00, 21:00)
- **Weekend Coverage**: Yes, runs 24/7
- **Frequency**: 56 times per week (vs. 5 times previously)

## 🎯 Repository Structure

```
Your Setup:
├── olx_scraper_gohighlevel/          # ← Public repo (application code)
│   ├── multi_client_scraper.py       # Core application
│   ├── DEPLOYMENT_WORKFLOW.md        # ← Complete workflow guide
│   └── README.md                     # Documentation
│
├── olx-scraper-private/              # ← Private repo (real credentials)
│   ├── config/clients_config.json   # 🔐 Real API keys
│   ├── deployment/deploy.sh          # 🚀 Automated deployment
│   └── README.md                     # Private documentation
│
└── Hetzner Server (188.245.58.182)
    └── /opt/olx-scraper/             # ← Running production system
```

## 🚨 Emergency Commands

### Service Issues
```bash
# Restart service
ssh hetzner "systemctl restart olx-multi-scraper"

# Check logs
ssh hetzner "journalctl -u olx-multi-scraper -f"
```

### Rollback Changes
```bash
# Rollback to previous version
ssh hetzner "cd /opt/olx-scraper && git reset --hard HEAD~1"
ssh hetzner "systemctl restart olx-multi-scraper"
```

## 📞 Quick Help

| Task | Command |
|------|---------|
| Add new client | Edit `config/clients_config.json` → `./deployment/deploy.sh` |
| Check service | `ssh hetzner "systemctl status olx-multi-scraper"` |
| View logs | `ssh hetzner "tail -f /opt/olx-scraper/logs/multi_client_scheduler.log"` |
| List clients | `ssh hetzner "cd /opt/olx-scraper && python3 multi_client_scraper.py --list"` |
| Deploy changes | `./deployment/deploy.sh` |
| Check results | `ssh hetzner "ls -la /opt/olx-scraper/results_*.json"` |

## 🎉 Summary

Your OLX scraper system is now **production-ready** with:

✅ **Automated deployment** (no manual server management)  
✅ **Multi-client support** (unlimited clients)  
✅ **Secure credentials** (private repository)  
✅ **24/7 operation** (3-hour schedule)  
✅ **Easy monitoring** (simple SSH commands)  
✅ **Rollback capability** (git-based versioning)  

**Adding a new client takes less than 5 minutes!**

📚 **Full Documentation**: See `DEPLOYMENT_WORKFLOW.md` for detailed instructions.

---
**Your lead generation system is ready to scale! 🚀** 