# 🔐 Dual Repository Strategy Guide

## 📖 Overview

This guide explains how to manage the OLX Multi-Client Scraper using a **dual repository strategy** that keeps sensitive client data private while maintaining an open-source codebase.

## 🎯 Why Use Dual Repositories?

### ✅ **Benefits:**
- **🔒 Security**: API keys and client data stay private
- **📦 Open Source**: Share application code publicly
- **🔄 Easy Updates**: Sync app updates without exposing secrets
- **👥 Team Collaboration**: Different access levels for different team members
- **🚀 Clean Deployment**: Automated deployment with secure configuration

### ⚖️ **Strategy Comparison:**

| Strategy | Public Code | Private Config | Complexity | Security | Maintenance |
|----------|-------------|----------------|------------|----------|-------------|
| **Dual Repos** | ✅ Yes | ✅ Separate | 🟡 Medium | 🟢 High | 🟢 Easy |
| Single Private | ❌ No | ✅ Same Repo | 🟢 Low | 🟢 High | 🟡 Medium |
| Env Variables | ✅ Yes | 🟡 Server Only | 🟢 Low | 🟡 Medium | 🔴 Hard |

## 🏗️ Repository Structure

### 📂 **Public Repository** (`olx_scraper_gohighlevel`)
```
olx_scraper_gohighlevel/          # https://github.com/novumhouse/olx_scraper_gohighlevel
├── multi_client_scraper.py       # ✅ Application code
├── multi_client_scheduler.py     # ✅ Application code
├── olx_scraper.py                # ✅ Application code
├── gohighlevel_integration.py    # ✅ Application code
├── clients_config.json.example   # ✅ Safe example
├── requirements.txt              # ✅ Dependencies
├── setup_private_config.sh       # ✅ Setup helper
├── HETZNER_README.md             # ✅ Documentation
├── hetzner_deployment_guide.md   # ✅ Documentation
└── .gitignore                    # ✅ Protects secrets
```

### 🔒 **Private Repository** (`olx-scraper-private`)
```
olx-scraper-private/              # git@github.com:you/olx-scraper-private.git
├── config/
│   └── clients_config.json      # 🔐 REAL API keys and client data
├── deployment/
│   └── deploy_to_hetzner.sh     # 🔐 Private deployment script
├── logs/                        # 🔐 Private logs (optional)
├── backup/                      # 🔐 Configuration backups
└── README.md                    # 🔐 Private documentation
```

## 🚀 Quick Setup

### **Step 1: Set Up Private Repository**

```bash
# Run the setup script
chmod +x setup_private_config.sh
./setup_private_config.sh
```

**The script will:**
1. ✅ Create private repository structure
2. ✅ Generate template configuration
3. ✅ Create deployment scripts
4. ✅ Set up security documentation

### **Step 2: Configure Your Clients**

Edit `../olx-scraper-private/config/clients_config.json`:

```json
{
  "client1": {
    "name": "JobsEU",
    "gohighlevel_api_key": "pk_live_REAL_API_KEY_HERE",
    "gohighlevel_location_id": "REAL_LOCATION_ID_HERE",
    "olx_search_urls": [
      "https://www.olx.pl/praca/q-producent/?search%5Border%5D=created_at:desc"
    ],
    "keywords": {
      "include": ["producent", "produkcja", "fabryka"],
      "exclude": ["agencja", "pośrednictwo"]
    },
    "schedule": "0 9 * * 1-5",
    "enabled": true,
    "max_pages": 5,
    "delay_between_requests": 2
  }
}
```

### **Step 3: Push Private Configuration**

```bash
cd ../olx-scraper-private
git add .
git commit -m "Add real client configuration"
git push -u origin main
```

### **Step 4: Deploy to Hetzner**

```bash
# From the private repository
./deployment/deploy_to_hetzner.sh git@github.com:yourusername/olx-scraper-private.git
```

## 🔄 Daily Workflow

### **Updating Application Code** (Public Repository)
```bash
cd olx_scraper_gohighlevel
# Make your code changes
git add .
git commit -m "Improve scraper functionality"
git push origin main
```

### **Updating Client Configuration** (Private Repository)
```bash
cd ../olx-scraper-private
# Edit config/clients_config.json
git add config/clients_config.json
git commit -m "Update client1 keywords"
git push origin main
```

### **Deploying Updates**
```bash
# Deploy both repositories to Hetzner
cd olx-scraper-private
./deployment/deploy_to_hetzner.sh git@github.com:yourusername/olx-scraper-private.git
```

## 🔐 Security Best Practices

### ✅ **DO:**
- ✅ Keep private repository truly private
- ✅ Use SSH keys for private repository access
- ✅ Regularly backup private configurations
- ✅ Use strong, unique API keys
- ✅ Review commits before pushing
- ✅ Set up repository access controls

### ❌ **DON'T:**
- ❌ NEVER commit real API keys to public repository
- ❌ NEVER make private repository public
- ❌ NEVER share private repository URLs publicly
- ❌ NEVER store secrets in public files
- ❌ NEVER hardcode credentials in application code

## 🚨 Emergency Procedures

### **If API Key is Compromised:**
1. 🔄 **Regenerate** API key in GoHighLevel
2. 🔧 **Update** `config/clients_config.json`
3. 📤 **Commit and push** configuration changes
4. 🚀 **Deploy** immediately to server
5. 🔍 **Monitor** for suspicious activity

### **If Private Repository is Exposed:**
1. 🚨 **Immediately** regenerate ALL API keys
2. 🗑️ **Delete** exposed repository
3. 🆕 **Create** new private repository
4. 🔧 **Update** all access credentials
5. 🚀 **Redeploy** with new configuration

## 🛠️ Troubleshooting

### **Problem: Private repository setup fails**
```bash
# Check Git configuration
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Verify SSH key setup
ssh -T git@github.com
```

### **Problem: Deployment script can't access private repository**
```bash
# On Hetzner server, set up SSH key for private repository
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
# Add the public key to your private repository's deploy keys
```

### **Problem: Configuration not updating on server**
```bash
# Check deployment logs
ssh root@your_server_ip
journalctl -u olx-multi-scraper -f

# Manually verify configuration
cat /opt/olx-scraper/clients_config.json
```

## 📞 Support

For issues with this dual repository strategy:

1. **📚 Check** this guide and documentation
2. **🔍 Search** existing issues in public repository
3. **❓ Create** new issue (public repository only - NO sensitive data)
4. **💬 Contact** team for private configuration issues

---

## 🎯 Summary

The dual repository strategy provides the perfect balance of:
- **🔒 Security** for sensitive client data
- **📦 Transparency** for application code
- **🔄 Maintainability** for long-term updates
- **🚀 Scalability** for multiple clients

**Next Steps:**
1. ✅ Run `./setup_private_config.sh`
2. ✅ Configure your real API keys
3. ✅ Deploy to Hetzner
4. ✅ Start serving your clients! 