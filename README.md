# 3-Tier AWS Network Deployment & Automated Validation Lab

## 📌 Project Overview
I built a secure 3-tier VPC architecture on AWS to simulate a production network environment. To make sure the firewall boundaries were completely airtight before handing it off, I followed the Software Testing Life Cycle (STLC) framework and wrote a Python automation script to scan ports and validate network isolation between layers.



## 🏗️ How the Network is Structured
* **Public Web Tier (10.0.0.0/20 & 10.0.16.0/20):** Public subnets handling the front-end entry point. Auto-assign public IP is enabled here so we can manage the environment.
* **Private App Tier (10.0.128.0/20):** Isolated backend layer. No direct internet routes. 
* **Isolated DB Tier (10.0.144.0/20):** Completely locked down. It sits in a deep private subnet to keep sensitive data safe.

## 🛡️ Security Group Chaining & Rules
Instead of leaving ports wide open, I chained the security groups together so traffic can only move laterally if explicitly trusted:
1. `Web-ALB-SG`: Open to Port 80 for web traffic. Port 22 (SSH) is locked down strictly to my local laptop's public IP for secure management.
2. `App-Tier-SG`: Only accepts inbound traffic on Port 22 and Port 8080 if it comes directly from the `Web-ALB-SG`. 
3. `DB-Tier-SG`: Strictly drops any direct traffic unless it comes straight from the `App-Tier-SG`.

## ⚙️ Automated Testing & Validation Results
Instead of manually typing network validation commands every time the infrastructure updates, I wrote `network_validator.py`. It runs socket-level connection checks from inside the public jump box to verify if our firewall rules are working or failing.

### Live Test Matrix Report:
* **TC_INT_001 (Web to App Port 22):** 🟢 **PASS** (Management path is open for admins)
* **TC_SEC_002 (Web to App Port 3306):** 🟢 **PASS** (Correctly TIMED OUT. Web cannot scan app for DB ports)
* **TC_SEC_003 (Web to DB Port 22):** 🟢 **PASS** (Correctly TIMED OUT. Web cannot talk directly to the Database)

## 🚀 Running the Health Check Script
If you deploy this architecture, you can drop into the web server instance and run the script to verify your setup instantly:
```bash
python3 network_validator.py
