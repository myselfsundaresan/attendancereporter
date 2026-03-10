# Saveetha Attendance Bot (Pro)

## 🎓 About the Project

**Saveetha Attendance Bot (Pro)** is an automated student assistant designed to monitor your college attendance daily. It removes the need for manual portal logins by delivering a smart, self-updating **Daily Tracker** directly to your Telegram.

Once configured, the bot:
- Automatically logs into the college portal
- Dynamically tracks attendance for **every single subject** individually
- Tracks attendance using **baseline comparison logic**
- Sends a **clean Daily Tracker message** directly to Telegram
- Updates attendance information automatically throughout the day
- Avoids manual attendance checking completely

This project is designed to demonstrate **practical automation skills, API integration, and workflow automation** suitable for college projects and portfolios.

---

## 📱 Telegram Message Preview

```
📅 Daily Attendance Tracker (11-03-2026)
⏰ Last Checked: 02:00 PM
━━━━━━━━━━━━━━━━━━━━━
📝 Today's Updates
🔹 Epidemiology, Biostati.. (MSC011)
      Held: 2 | Present: 2
━━━━━━━━━━━━━━━━━━━━━
📊 Subject-Wise Stats
🔹 Epidemiology, Biostati..: 14/14 (100.0%)
🔹 Recent Advances in Mol..: 4/4 (100.0%)
🔹 Library Hour: 17/19 (89.47%)
━━━━━━━━━━━━━━━━━━━━━
📈 Total Overall: 35/37 (94.59%)
```

---

## 🧠 Smart Attendance Logic

Unlike basic trackers, this bot uses **Baseline Comparison Logic** combined with **Dynamic JSON Memory**.

### Subject-Wise Morning Reset
Every morning, the bot scans your portal, identifies all your enrolled subjects, and captures the current attendance counts for **each specific subject** to store as the morning **Baseline**.

### Today's Stats (Itemized Tracking)
It calculates:

```
Current Count - Morning Baseline (Per Subject)
```

This ensures the bot shows **exactly how many classes were held today for which subjects**, rather than relying on raw overall numbers. It provides a detailed, itemized breakdown of what happened today, alongside your true combined overall percentage.

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

#### 2. Create Your Telegram Bot

Before filling in GitHub Secrets, you need a **Bot Token** and your **Chat ID** from Telegram.

---

##### Part A — Get Your `BOT_TOKEN` from @BotFather

**Step 1 — Open BotFather**
- Open Telegram and search for **`@BotFather`**
- It is the **official verified bot** with a blue checkmark ✓
- Tap on it and press **Start**

**Step 2 — Create a new bot**
- Send the command: `/newbot`
- BotFather will ask you to choose a **display name** for your bot
- Enter any name you like (e.g. `My Attendance Bot`)

**Step 3 — Choose a username**
- BotFather will then ask for a **username**
- It must be unique and **must end with** `bot`
- Example: `my_attendance_bot` or `SaveethaTrackerBot`

**Step 4 — Copy your Bot Token**
- BotFather will reply with your token. It looks like this:
  ```
  7123456789:AAFxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
  ```
- Copy this entire string — this is your **`BOT_TOKEN`**
- ⚠️ **Never share this token publicly**

**Step 5 — Start a chat with your new bot**
- Search your bot's username in Telegram and press **Start**
- This is required — the bot **cannot send you messages** until you initiate the conversation first

---

##### Part B — Get Your `CHAT_ID` from @userinfobot

**Step 1 — Open userinfobot**
- In Telegram, search **`@userinfobot`** and press **Start**

**Step 2 — Copy your ID**
- The bot will instantly reply with your account details:
  ```
  Id: 987654321
  First: Your Name
  Username: @yourhandle
  ```
- Copy the number next to **Id:** — this is your **`CHAT_ID`**

---

#### 3. Configure GitHub Secrets
Sensitive credentials are securely stored using **GitHub Secrets** so the bot can log into the portal automatically.

##### Navigation
1. Open your **forked repository**
2. Go to **Settings**
3. Click **Secrets and variables → Actions**
4. Click **New repository secret**

##### Required Secrets

| Secret Name | Value |
|-------------|-------|
| `USER_ID` | Your college portal username / roll number |
| `PASSWORD` | Your college portal password |
| `BASE_URL` | **(Optional)** Your college portal link (e.g., `https://arms.sse.saveetha.com`). **Defaults to SMC - for Saveetha Medical College** if left blank. |
| `BOT_TOKEN` | Token copied from **@BotFather** (Step 2A above) |
| `CHAT_ID` | Your ID copied from **@userinfobot** (Step 2B above) |
| `GH_PAT` | A GitHub Personal Access Token (Classic) with **workflow scope** |
| `REPO_FULL_NAME` | Your GitHub repository path (example: `username/attendancereporter`) |

---

#### 4. Initialize Attendance Memory

Because this bot uses dynamic multi-subject tracking, it requires a JSON structure.  
Edit the file **`last_attendance.txt`** in your repository, delete everything inside, and set it to exactly this:

```json
{}
```

**What this means:**
- `{}` → An empty JSON dictionary.
- On its first run, the bot will automatically read your portal, extract all your subjects, and build a detailed memory map to track each one individually.

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

```
Worker Settings → Variables → Environment Variables
```

Add the following variables:

| Variable | Value |
|----------|-------|
| `BOT_TOKEN` | Same Telegram bot token used in GitHub |
| `GH_PAT` | Same GitHub Personal Access Token |
| `REPO_FULL_NAME` | Same repository path |

---

### 5. Activate Telegram Webhook

Copy your **Worker URL** and open this link in your browser:

```
https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook?url=<YOUR_WORKER_URL>
```

> Replace `<YOUR_BOT_TOKEN>` with your BOT Token from Telegram BotFather  
> Replace `<YOUR_WORKER_URL>` with your Worker URL from Cloudflare

This connects your Telegram bot to the Cloudflare listener.

---

> [!NOTE]
> **Don't want to use Cloudflare?**  
> If you skip Phase 2, the bot will still run automatically **3 times a day**.  
> However, do **not click the "Refresh Now" button** in Telegram because GitHub Actions cannot process the request without the listener.

---

## ⏰ Automation Schedule

The bot runs automatically through **GitHub Actions workflows** at the following times:

| Time | Run |
|------|-----|
| **09:00 AM IST** | Morning Baseline |
| **11:00 AM IST** | Mid-day Update |
| **02:00 PM IST** | Afternoon Summary |

These scheduled runs keep your **Daily Tracker updated throughout the day**.

---

## ❓ FAQ

**Is my password safe?**  
Yes. Your credentials are stored securely inside **GitHub Secrets** and never printed in logs.

**What if I have a holiday?**  
The bot will detect **0 new classes** for all subjects and update the message accordingly with *No classes updated yet today*.

**Can I run it manually?**  
Yes. Go to the **Actions tab** in your GitHub repository and click **Run workflow**.

---

## 🛠️ Tech Stack & Resume Value

- **Python**
- **GitHub Actions** (Scheduled automation)
- **Telegram Bot API**
- **Cloudflare Workers** (Webhook listener)

### Skills Demonstrated
- Automation scripting
- Secure credential handling
- Scheduled workflows
- API integration
- Cloud automation pipelines

Ideal for **college projects, resumes, and internship portfolios**.

---

<sub>Built for educational purposes to demonstrate Python automation and API integration.</sub>
