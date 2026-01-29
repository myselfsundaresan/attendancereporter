# Saveetha Attendance Bot

![Python](https://img.shields.io/badge/Python-3.9-blue?logo=python)
![Selenium](https://img.shields.io/badge/Selenium-Automation-brightgreen?logo=selenium)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-Automation-black?logo=githubactions)
![Telegram](https://img.shields.io/badge/Telegram-Bot_API-blue?logo=telegram)
![Status](https://img.shields.io/badge/Status-Active-success)

---

## 🎓 About the Project

**Saveetha Attendance Bot** is a student-friendly automation project that helps you **monitor your college attendance daily without manual checking**.

Once configured, the bot:
- Automatically logs into the college portal  
- Checks attendance every day  
- Applies logical comparison (not just raw numbers)  
- Notifies you via **Telegram** only when needed  

This project is designed to demonstrate **practical automation skills** suitable for college projects and internships.

---

## 🧠 Attendance Logic

The bot compares **yesterday vs today** attendance using:

- **Total Classes**
- **Classes Attended**

| Observation | Meaning | Result |
|------------|---------|--------|
| Total Classes ↑ & Attended ↑ | You attended the class | Present ✅ |
| Total Classes ↑ & Attended unchanged | Class held, you were absent | Absent ❌ |
| Total Classes unchanged | No class / Holiday | No notification |

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
|-----|-------|
| `USER_ID` | Your college roll number / login ID |
| `PASSWORD` | Your college portal password |
| `BOT_TOKEN` | Telegram bot token from @BotFather |
| `CHAT_ID` | Telegram chat ID from @userinfobot |

After adding all four, they should appear in the secrets list.

---

## 🧠 Initialize Attendance Memory

Create a file named **`last_attendance.txt`** in the repository root and add:

```
0,0
```

This file stores the previous day’s attendance values.

---

## ⏰ Enable Automation

- Open the **Actions** tab  
- Enable workflows  

The bot runs automatically **every day at 9:30 AM IST**.

---

## ❓ Beginner FAQ

**Do I need programming knowledge?**  
No. Setup is simple and beginner-friendly.

**Will this modify my attendance?**  
No. It only checks and reports attendance.

**Is my password safe?**  
Yes. Stored securely using GitHub Secrets.

**What happens on holidays?**  
No change in total classes → no notification.

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
- **Telegram Bot API**

### Skills Demonstrated
- Automation scripting  
- Secure credential handling  
- Scheduled workflows  
- API integration  
- Real-world problem solving  

Ideal for **college projects, resumes, and internship portfolios**.

---

<sub>Built for educational purposes. Use responsibly.</sub>
