# Saveetha Attendance Bot (Pro)

## 🎓 About the Project

**Saveetha Attendance Bot (Pro)** is an automated student assistant designed to monitor your college attendance daily. It removes the need for manual portal logins by delivering a smart, self-updating **Daily Tracker** directly to your Telegram.

Once configured, the bot:
- Automatically logs into the college portal  
- Tracks attendance using **baseline comparison logic**  
- Sends a **clean Daily Tracker message** directly to Telegram  
- Updates attendance information automatically throughout the day  
- Avoids manual attendance checking completely  

This project is designed to demonstrate **practical automation skills, API integration, and workflow automation** suitable for college projects and portfolios.

---

## 🧠 Smart Attendance Logic

Unlike basic trackers, this bot uses **Baseline Comparison Logic**.

### Morning Reset
Every morning, the bot captures your **current portal attendance counts** and stores them as the **Baseline**.

### Today's Stats
It calculates:


Current Count - Morning Baseline


This ensures the bot shows **exactly how many classes were held today**, instead of relying on raw totals.

### Dynamic Messaging
Instead of sending multiple messages:

- The bot **deletes the previous message**
- Sends a **fresh Daily Tracker message**
- This keeps your Telegram chat **clean while still triggering notifications**

---

## 🚀 Setup Guide

### Phase 1: Basic Setup (Mandatory)

#### 1. Fork the Repository
Click **Fork** (top-right of this page) to create your personal copy of the repository.

---

#### 2. Configure GitHub Secrets
Sensitive credentials are securely stored using **GitHub Secrets** so the bot can log into the portal automatically.

##### Navigation
1. Open your **forked repository**  
2. Go to **Settings**  
3. Click **Secrets and variables → Actions**  
4. Click **New repository secret**

##### Required Secrets

| Secret Name | Value |
|-------------|------|
| `USER_ID` | Your college portal username / roll number |
| `PASSWORD` | Your college portal password |
| `BOT_TOKEN` | Token from **@BotFather** on Telegram |
| `CHAT_ID` | Your ID from **@userinfobot** on Telegram |
| `GH_PAT` | A GitHub Personal Access Token (Classic) with **workflow scope** |
| `REPO_FULL_NAME` | Your GitHub repository path (example: `username/attendancereporter`) |

---

### 🧠 Initialize Attendance Memory

Edit the file **`last_attendance.txt`** in your repository and set it to:


`0,0,None,01-01-2000`


### What this means
- `0,0` → Initial counts for total and attended classes  
- `None` → No Telegram message created yet  
- `01-01-2000` → Forces a fresh Daily Tracker message on the first run  

---

## 🔄 Phase 2: "Refresh Now" Button (Optional)

The **Refresh Now** button allows you to trigger an attendance check instantly from Telegram.

Since **GitHub Actions cannot listen to Telegram button clicks**, a **listener service** is required.

---

## 🛠️ Cloudflare Worker Setup (The Listener)

### 1. Create Worker
1. Log in to **Cloudflare**  
2. Navigate to **Workers & Pages**  
3. Click **Create application**  
4. Select **Create Worker**

---

### 2. Deploy Worker
- Click **Deploy**  
- After deployment, click **Edit Code**

---

### 3. Paste Worker Code
Replace everything inside **worker.js** with the **Webhook script provided during setup**.

---

### 4. Add Environment Variables

Go to:


Worker Settings → Variables → Environment Variables


Add the following variables:

| Variable | Value |
|---------|------|
| `BOT_TOKEN` | Same Telegram bot token used in GitHub |
| `GH_PAT` | Same GitHub Personal Access Token |
| `REPO_FULL_NAME` | Same repository path |

---

### 5. Activate Telegram Webhook

Copy your **Worker URL** and open this link in your browser:


`https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook?url=<YOUR_WORKER_URL>`

Replace `<YOUR_BOT_TOKEN>` with your BOT Token from Telegram Bot Father


Replace `<YOUR_WORKER_URL>` with your worker url from Cloudfare


This connects your Telegram bot to the Cloudflare listener.

---

> [!NOTE]  
> **Don't want to use Cloudflare?**  
> If you skip Phase 2, the bot will still run automatically **3 times a day**.  
> However, do **not click the "Refresh Now" button** in Telegram because GitHub Actions cannot process the request without the listener.

---

## ⏰ Automation Schedule

The bot runs automatically through **GitHub Actions workflows** at the following times:

- **09:00 AM IST** → Morning Baseline  
- **11:00 AM IST** → Mid-day Update  
- **02:00 PM IST** → Afternoon Summary  

These scheduled runs keep your **Daily Tracker updated throughout the day**.

---

## ❓ FAQ

**Is my password safe?**  
Yes. Your credentials are stored securely inside **GitHub Secrets** and never printed in logs.

**What if I have a holiday?**  
The bot will detect **0 new classes** and update the message accordingly with *0 classes held today*.

**Can I run it manually?**  
Yes. Go to the **Actions tab** in your GitHub repository and click **Run workflow**.

---

## 🛠️ Tech Stack & Resume Value

- **Python**
- **GitHub Actions (Scheduled automation)**
- **Telegram Bot API**
- **Cloudflare Workers (Webhook listener)**

### Skills Demonstrated
- Automation scripting  
- Secure credential handling  
- Scheduled workflows  
- API integration  
- Cloud automation pipelines  

Ideal for **college projects, resumes, and internship portfolios**.

---

<sub>Built for educational purposes to demonstrate Python automation and API integration.</sub>
