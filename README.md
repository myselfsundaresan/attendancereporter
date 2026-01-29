# Saveetha Attendance Bot

![Python](https://img.shields.io/badge/Python-3.9-blue?logo=python)
![Selenium](https://img.shields.io/badge/Selenium-Automation-brightgreen?logo=selenium)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-Cron--Based-black?logo=githubactions)
![Telegram](https://img.shields.io/badge/Telegram-Bot_API-blue?logo=telegram)

---

## 🎓 About the Project

**Saveetha Attendance Bot** is a student-friendly automation project that helps you monitor your college attendance daily without manual checking.

Once configured, the bot:
- Automatically logs into the college portal  
- Checks attendance multiple times a day (**9 AM, 11 AM, 2 PM IST**)  
- **Smart Messaging:** Sends a single *Daily Tracker* message that updates itself throughout the day instead of spamming  
- Applies logical comparison (not just raw numbers)  

This project demonstrates **real-world automation and DevOps concepts**, making it suitable for college projects and internships.

---

## 🧠 Attendance Logic

The bot compares **yesterday vs today** attendance using:
- **Total Classes**
- **Classes Attended**

| Observation | Meaning | Result |
|------------|--------|--------|
| Total Classes ↑ & Attended ↑ | You attended the class | Present ✅ |
| Total Classes ↑ & Attended unchanged | Class held, you were absent | Absent ❌ |
| Total Classes unchanged | No class / Holiday | No notification |

---

## 🔄 Dynamic Updates (Smart Messaging)

Instead of sending multiple messages per day, the bot uses the **Telegram Edit API**.

- **Morning:** Sends a fresh *Daily Tracker* message  
- **Midday & Afternoon:** Edits the same message with updated counts and timestamps  

This keeps notifications clean and non-intrusive.

---

## 🚀 Setup Guide (Beginner Friendly)

### 1. Fork the Repository
Click **Fork** (top-right of this page) to create your own copy.

### 2. Add GitHub Secrets
GitHub stores sensitive information securely using **Secrets**.

#### Navigation
1. Open your repository  
2. Click **Settings**  
3. Go to **Secrets and variables → Actions**  
4. Click **New repository secret**  

#### Required Secrets

| Name | Value |
|------|------|
| `USER_ID` | Your college roll number / login ID |
| `PASSWORD` | Your college portal password |
| `BOT_TOKEN` | Telegram bot token from **@BotFather** |
| `CHAT_ID` | Telegram chat ID from **@userinfobot** |

---

## 🧠 Initialize Attendance Memory

Create a file named **`last_attendance.txt`** in the repository root and add:

```
0,0,None,01-01-2000
```

---

## ⏰ Enable Automation

The bot runs automatically **multiple times daily**:
- 9:00 AM  
- 11:00 AM  
- 2:00 PM (IST)

---

## ❓ Beginner FAQ

**Do I need programming knowledge?**  
No. Setup is simple and beginner-friendly.

**Will this modify my attendance?**  
No. It only checks and reports attendance.

**Is my password safe?**  
Yes. Stored securely using GitHub Secrets.

---

## 🎯 Why This Is Useful for Attendance Shortage

- Daily awareness of attendance status  
- Early warning before dropping below limits  
- Helps plan attendance recovery  
- Avoids last-minute exam eligibility issues  
- Especially useful for **75% attendance rules**  

---

## 🛠️ Tech Stack & Resume Value

- **Python 3.9**
- **Selenium (Headless Chrome)**
- **GitHub Actions (Cron-based automation)**
- **Telegram Bot API** (*SendMessage & EditMessageText*)

### Skills Demonstrated
- Automation scripting  
- Secure credential handling  
- Scheduled workflows  
- API integration  
- Real-world problem solving  

---

## 📄 Resume Description (2 Lines)

- Built an automated attendance monitoring bot using Python, Selenium, and GitHub Actions to track college attendance in real time.  
- Implemented smart Telegram notifications with dynamic message updates to reduce spam and improve daily tracking efficiency.

---

<sub>Built for educational purposes. Use responsibly.</sub>
