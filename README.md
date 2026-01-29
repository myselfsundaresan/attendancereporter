# Saveetha Attendance Bot

## 🎓 About the Project

**Saveetha Attendance Bot** is a student-friendly automation project that helps you monitor your college attendance daily without manual checking.

Once configured, the bot:
- Automatically logs into the college portal  
- Checks attendance multiple times a day (**9 AM, 11 AM, 2 PM IST**)  
- **Smart Messaging:** Sends a single *Daily Tracker* message that updates itself throughout the day instead of spamming  
- Applies logical comparison (not just raw numbers)  

This project is designed to demonstrate **practical automation skills** suitable for college projects and internships.

---

## 🧠 Attendance Logic

The bot tracks attendance in real time by comparing **Start-of-Day counts** against **Current counts**.

Instead of a simple *Present / Absent* status, it provides a detailed daily breakdown:

- **No. of classes today:** Total classes conducted since 9:00 AM  
- **No. of classes present:** Classes you actually attended  

This approach correctly handles **multiple classes per day** and produces an accurate daily summary.

---

## 🔄 Dynamic Updates

Instead of sending multiple messages a day, the bot uses the **Telegram Edit API**.

- **Morning:** Sends a fresh *Daily Tracker* message  
- **Afternoon:** Edits the same message with updated counts and timestamps  

This keeps notifications clean, minimal, and informative.

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

After adding all four, they should appear in the secrets list.

---

## 🧠 Initialize Attendance Memory

Create a file named **`last_attendance.txt`** in the repository root and add **exactly this line**:

```
0,0,None,01-01-2000
```

### What this means
- `0,0` → Starting counts for Total and Attended classes  
- `None` → No message sent yet today  
- `01-01-2000` → Forces a fresh tracker message on first run  

---

## ⏰ Enable Automation

- Open the **Actions** tab  
- Enable workflows  

⏱️ The bot runs automatically **multiple times daily**:
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

**What happens on holidays?**  
No change in total classes → bot stays silent or updates the message with *No classes yet*.

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

Ideal for **college projects, resumes, and internship portfolios**.

---

<sub>Built for educational purposes. Use responsibly.</sub>
