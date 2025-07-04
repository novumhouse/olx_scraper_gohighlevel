# 🚀 OLX Multi-Client Job Scraper with GoHighLevel Integration

**A powerful, scalable multi-client job scraping system** that extracts manufacturing job listings from OLX.pl and automatically sends leads to GoHighLevel CRM.

## Features

### 🎯 **Multi-Client Architecture**
- **👥 Multiple Clients**: Manage unlimited client configurations
- **🔧 Individual Settings**: Custom keywords, schedules, and API keys per client
- **📊 Separate Monitoring**: Individual logs and performance tracking
- **⚙️ Flexible Scheduling**: Different schedules for each client

### 🛡️ **Advanced Filtering & Processing**
- **🏭 Manufacturing Focus**: Targets production companies and manufacturers
- **🚫 Agency Exclusion**: Automatically filters out employment agencies
- **📞 Contact Extraction**: Extracts company names, positions, and phone numbers
- **🔍 Smart Keyword Matching**: Sophisticated include/exclude logic

### 🔒 **Security & Configuration**
- **🔐 Dual Repository Strategy**: Keep sensitive data private
- **🔑 Secure API Key Management**: Never expose credentials publicly
- **📝 Example Configurations**: Safe templates for public sharing

### 🚀 **Enterprise Deployment**
- **☁️ Hetzner Cloud Ready**: Complete deployment automation
- **🔄 Auto-Scheduling**: Cron-based multi-client scheduling
- **📈 Monitoring & Logging**: Comprehensive logging system
- **🐳 Cross-Platform**: Windows/Linux compatibility

## 🏗️ Architecture

### 📂 **Repository Structure**
```
📦 Public Repository (this repo)
├── 🎯 multi_client_scraper.py      # Multi-client scraper manager
├── ⏰ multi_client_scheduler.py    # Automated scheduling system
├── 🕷️ olx_scraper.py              # Core scraping engine
├── 🔗 gohighlevel_integration.py  # GoHighLevel API integration
├── 📋 clients_config.json.example # Safe configuration template
├── 🛠️ setup_private_config.sh     # Private repository setup
├── 📚 DUAL_REPOSITORY_GUIDE.md    # Dual repo strategy guide
├── 🚀 HETZNER_README.md           # Hetzner deployment guide
├── 📖 hetzner_deployment_guide.md # Complete deployment docs
└── 📝 requirements.txt            # Python dependencies
```

### 🔐 **Private Repository** (your sensitive data)
```
📦 Private Repository (your private repo)
├── config/
│   └── clients_config.json        # 🔑 REAL API keys & client data
├── deployment/
│   └── deploy_to_hetzner.sh       # 🚀 Private deployment script
├── logs/                          # 📊 Private logs
└── backup/                        # 💾 Configuration backups
```

## 🚀 Quick Start

### **Option 1: 🔐 Dual Repository Setup (Recommended)**

Perfect for production use with multiple clients:

```bash
# 1. Clone public repository
git clone https://github.com/novumhouse/olx_scraper_gohighlevel.git
cd olx_scraper_gohighlevel

# 2. Set up private configuration repository
chmod +x setup_private_config.sh  # Linux/Mac
./setup_private_config.sh

# 3. Configure your real API keys in private repo
cd ../olx-scraper-private
# Edit config/clients_config.json with real data

# 4. Deploy to production
./deployment/deploy_to_hetzner.sh YOUR_PRIVATE_REPO_URL
```

**📚 Learn More**: See [`DUAL_REPOSITORY_GUIDE.md`](DUAL_REPOSITORY_GUIDE.md) for complete setup instructions.

### **Option 2: 🏃 Quick Local Testing**

For testing and development:

```bash
# 1. Clone and install
git clone https://github.com/novumhouse/olx_scraper_gohighlevel.git
cd olx_scraper_gohighlevel
pip install -r requirements.txt

# 2. Copy example configuration
cp clients_config.json.example clients_config.json

# 3. Edit configuration with your API keys
# Edit clients_config.json (add your real API keys)

# 4. Test the system
python multi_client_scraper.py --list
python multi_client_scraper.py --client client1 --headless
```

## 📖 Usage

### 🎯 **Multi-Client Management**

```bash
# List all configured clients
python multi_client_scraper.py --list

# Run specific client
python multi_client_scraper.py --client client1 --headless

# Run all enabled clients
python multi_client_scraper.py --all --headless

# Test mode (no API calls)
python multi_client_scraper.py --client client1 --test-mode
```

### ⏰ **Automated Scheduling**

```bash
# Start scheduler for all clients
python multi_client_scheduler.py

# Check scheduler status
python multi_client_scheduler.py --status

# Run specific client immediately
python multi_client_scheduler.py --client client1

# Run with custom schedule override
python multi_client_scheduler.py --client client1 --schedule "*/30 * * * *"
```

### 🔧 **Single Client Operations** (Legacy Support)

```bash
# Original single-client mode still works
python olx_scraper.py --headless --api-key YOUR_API_KEY
```

## ⚙️ Configuration

### 📋 **Client Configuration Format**

Edit `clients_config.json` with your client details:

```json
{
  "client1": {
    "name": "Manufacturing Client",
    "gohighlevel_api_key": "pk_live_your_real_api_key",
    "gohighlevel_location_id": "your_location_id",
    "olx_search_urls": [
      "https://www.olx.pl/praca/q-producent/?search%5Border%5D=created_at:desc",
      "https://www.olx.pl/praca/q-produkcja/?search%5Border%5D=created_at:desc"
    ],
    "keywords": {
      "include": ["producent", "produkcja", "fabryka", "manufacturing"],
      "exclude": ["agencja", "pośrednictwo", "kadry", "hr"]
    },
    "schedule": "0 9 * * 1-5",  // Monday-Friday at 9 AM
    "enabled": true,
    "max_pages": 5,
    "delay_between_requests": 2
  }
}
```

### 🔍 **Advanced Filtering**

**Manufacturing Keywords (Include):**
- `producent`, `produkcja`, `fabryka` (Polish)
- `manufacturing`, `production`, `factory` (English)
- Industry-specific: `automotive`, `meble`, `electronic`

**Agency Keywords (Exclude):**
- `agencja`, `pośrednictwo`, `rekrutacja`
- `staffing`, `hr`, `human resources`

## 🚀 Deployment

### ☁️ **Hetzner Cloud Deployment**

Complete automated deployment to Hetzner Cloud:

```bash
# Quick deployment
cd olx-scraper-private
./deployment/deploy_to_hetzner.sh YOUR_PRIVATE_REPO_URL

# Manual deployment
ssh root@your_hetzner_ip
git clone https://github.com/novumhouse/olx_scraper_gohighlevel.git /opt/olx-scraper
git clone YOUR_PRIVATE_REPO_URL /opt/olx-scraper-private
cp /opt/olx-scraper-private/config/clients_config.json /opt/olx-scraper/
systemctl enable olx-multi-scraper
systemctl start olx-multi-scraper
```

**📚 Complete Guide**: [`HETZNER_README.md`](HETZNER_README.md) | [`hetzner_deployment_guide.md`](hetzner_deployment_guide.md)

## 📊 Monitoring

### 📝 **Log Files**
- `multi_client_scheduler.log` - Scheduler operations
- `{client_id}_scraper.log` - Individual client logs
- `olx_scraper.log` - Core scraper operations
- `gohighlevel.log` - API integration logs

### 📈 **Performance Monitoring**
```bash
# Check client status
python multi_client_scheduler.py --status

# View recent logs
tail -f multi_client_scheduler.log

# Monitor specific client
tail -f client1_scraper.log
```

## 🔒 Security Best Practices

- ✅ **Use dual repository strategy** for production
- ✅ **Never commit real API keys** to public repositories
- ✅ **Regularly rotate API keys**
- ✅ **Use SSH keys** for private repository access
- ✅ **Set up monitoring** for unauthorized access attempts

## 🛠️ Requirements

### 🐍 **System Requirements**
- **Python 3.7+**
- **Chrome Browser** (automatically managed)
- **Git** (for dual repository setup)

### 📦 **Python Dependencies**
```bash
pip install -r requirements.txt
```

Key dependencies:
- `selenium>=4.0.0` - Web automation
- `webdriver-manager>=4.0.0` - Chrome WebDriver management
- `requests>=2.25.0` - HTTP requests
- `schedule>=1.1.0` - Task scheduling
- `python-dotenv>=0.19.0` - Environment management

## 🆘 Troubleshooting

### 🔧 **Common Issues**

**Problem: Chrome/ChromeDriver compatibility**
```bash
# Solution: Update webdriver-manager
pip install --upgrade webdriver-manager
```

**Problem: GoHighLevel API errors**
```bash
# Solution: Verify API key and location ID
python multi_client_scraper.py --client client1 --test-mode
```

**Problem: Private repository access**
```bash
# Solution: Set up SSH keys
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
# Add public key to GitHub deploy keys
```

**Problem: Scheduling not working**
```bash
# Solution: Check cron service and logs
systemctl status cron
journalctl -u olx-multi-scraper -f
```

## 📞 Support

- 📚 **Documentation**: Check all `.md` files in this repository
- 🐛 **Issues**: Create GitHub issues (public code only - no API keys!)
- 💬 **Discussions**: GitHub Discussions for general questions
- 🔐 **Private Issues**: Contact maintainers directly for sensitive topics

## 📄 License

MIT License - see [`LICENSE`](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is for legitimate business lead generation only. Use responsibly and in accordance with:
- **OLX.pl Terms of Service**
- **GoHighLevel API Terms**
- **Local data protection laws**
- **Ethical web scraping practices**

---

## 🎯 Next Steps

1. **🔧 Set up dual repositories**: `./setup_private_config.sh`
2. **⚙️ Configure your clients**: Edit private `clients_config.json`
3. **🚀 Deploy to Hetzner**: Follow deployment guides
4. **📊 Monitor performance**: Set up log monitoring
5. **📈 Scale your business**: Add more clients as needed

**Ready to start?** See [`DUAL_REPOSITORY_GUIDE.md`](DUAL_REPOSITORY_GUIDE.md) for step-by-step setup!