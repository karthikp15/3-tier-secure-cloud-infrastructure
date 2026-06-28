# 3-Tier AWS Network Deployment & Manual Security Verification Lab

## 📌 Project Overview
I deployed a secure 3-tier VPC architecture on AWS to simulate a live production network environment. Following the Software Testing Life Cycle (STLC) framework, I performed end-to-end **Manual Network Testing** directly from the Linux terminal. This lab validates structural routing, cross-tier functional integration, and negative security boundaries between the Web, Application, and Database layers.

## 🏗️ Infrastructure Network Layout
* **Public Web Tier (10.0.0.0/20 & 10.0.16.0/20):** Public subnets handling front-end access, utilized as a secure public jump box environment for administration.
* **Private App Tier (10.0.128.0/20):** Isolated backend hosting application logic, completely cut off from direct internet access.
* **Isolated DB Tier (10.0.144.0/20):** Deeply isolated database subnet space optimized to protect sensitive data from external or lateral exposure.

## 🛡️ Security Group Rules & Stateful Traffic Control
AWS Security Groups were chained sequentially to enforce strict least-privilege traffic flow:
1. `Web-ALB-SG`: Permits public HTTP (Port 80) traffic. Inbound SSH (Port 22) is tightly restricted to specific administrator management IPs.
2. `App-Tier-SG`: Restricts inbound access; it only accepts traffic on Port 22 and business ports if originating directly from the `Web-ALB-SG`.
3. `DB-Tier-SG`: Operates under a default-deny posture, strictly dropping any direct packets unless they originate straight from the private `App-Tier-SG`.

## 📊 Manual Testing Methodology & Verification Matrix
To ensure the infrastructure was production-ready, I performed explicit manual verification using the Linux network utility tool **`ncat`** to execute core STLC testing types:

### 1. Functional Integration Testing (Positive Testing)
* **Objective:** Verify that authorized management paths between dependent tiers operate correctly under normal conditions.
* **Execution:** Executed an open port check from the Web Tier to the App Tier on Port 22.

### 2. Negative Security Testing (Isolation Verification)
* **Objective:** Intentionally execute unauthorized traffic requests to ensure firewalls drop packets and block lateral movement.
* **Execution:** Attempted direct lateral connections from the public Web Tier to unauthorized database ports (Port 3306) and unauthorized management interfaces (Port 22 on the Database Tier).

### Live Manual Test Execution Log:
| Test Case ID | Test Type | Test Scenario | Manual Command Executed | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC_INT_001** | Positive Integration | Web Tier ➔ App Tier (Port 22) | `nc -zv -w 3 10.0.137.196 22` | Connection Open | **Connected** | ✅ PASS |
| **TC_SEC_002** | Negative Security | Web Tier ➔ App Tier (Port 3306) | `nc -zv -w 5 10.0.137.196 3306` | Packet Drop / Timeout | **TIMEOUT** | ✅ PASS |
| **TC_SEC_003** | Negative Security | Web Tier ➔ DB Tier (Port 22) | `nc -zv -w 5 [DB_IP] 22` | Packet Drop / Timeout | **TIMEOUT** | ✅ PASS |

## 🚀 Key Technical Takeaways
* **Sanity Testing:** Ran initial deployment environment verification to ensure compute instances reached a stable "Running" health state.
* **Boundary Analysis:** Evaluated CIDR block layout structures (`/20` vs `/24`) to navigate around overlapping network boundary constraints during private subnet configuration.
* **Defensive Architecture:** Confirmed that a compromise of the public web interface leaves the core database layer structurally isolated and untargetable.
