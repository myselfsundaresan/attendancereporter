<!-- ANIMATED HEADER -->

<div align="center">
<img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=600&size=28&duration=3000&pause=1000&color=249c32&center=true&vCenter=true&width=700&lines=Saveetha+Attendance+Bot;Smart+Daily+Attendance+Tracking;Student-Friendly+Automation;Zero-Touch+Monitoring" alt="Typing SVG" />
</div>

<!-- BADGES -->

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9-blue?logo=python)
![Selenium](https://img.shields.io/badge/Selenium-Automation-brightgreen?logo=selenium)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-Automation-black?logo=githubactions)
![Telegram](https://img.shields.io/badge/Telegram-Bot_API-blue?logo=telegram)
![Status](https://img.shields.io/badge/Status-Active-success)

</div>

---

## 🎓 About the Project

**Saveetha Attendance Bot** is a student-focused automation project that **monitors college attendance daily without manual effort**.

Once configured, the bot:
- Logs into the college attendance portal automatically  
- Compares attendance data day-by-day using logic  
- Detects **Present / Absent / No Class** accurately  
- Sends clear notifications via **Telegram**  

This project demonstrates **real-world automation**, not just basic scripting.

---

## 🧠 Attendance Decision Logic (Simple & Reliable)

The bot compares **yesterday vs today** using:

- **Total Classes**
- **Classes Attended**

### 📊 Logic Table

| Change Observed | Interpretation | Result |
|----------------|---------------|--------|
| Total Classes ↑ & Attended ↑ | You attended the class | Present ✅ |
| Total Classes ↑ & Attended unchanged | Class held, you were absent | Absent ❌ |
| Total Classes unchanged | No class / Holiday | No alert |

This avoids false notifications and unnecessary panic.

---

## 🚀 Quick Setup (Beginner-Friendly)

### 1️⃣ Fork the Repository
Click **Fork** (top-right) to create your own copy.

### 2️⃣ Add Secrets (No Coding Needed)
Go to:

**Settings → Secrets and variables → Actions**

Add:

| Secret | Description |
|------|-------------|
| `USER_ID` | College portal login ID |
| `PASSWORD` | College portal password |
| `BOT_TOKEN` | Telegram bot token (@BotFather) |
| `CHAT_ID` | Your Telegram chat ID (@userinfobot) |

🔐 All values are securely stored by GitHub.

### 3️⃣ Initialize Attendance Memory
Create **`last_attendance.txt`** in the root folder and add:

```
0,0
```

### 4️⃣ Enable Automation
Open **Actions** → Enable workflows.

⏰ Runs automatically **every day at 9:30 AM IST**.

---

## ❓ Beginner FAQ

**Q1. Do I need programming knowledge to use this?**  
No. Setup requires only copying values and clicking buttons.

**Q2. Will this change my attendance?**  
No. It only *checks* attendance and notifies you.

**Q3. Is my password safe?**  
Yes. Credentials are stored securely using GitHub Secrets.

**Q4. What if there is a holiday?**  
The bot detects no change in total classes and stays silent.

**Q5. Can this get me into trouble?**  
Use responsibly. This project is meant for **personal tracking only**.

---

## 🎯 Why This Is Useful for Attendance Shortage

- Early warning when you miss classes  
- Helps you **plan attendance recovery** before exams  
- Prevents last-minute shocks during internal assessments  
- Encourages consistent attendance habits  
- Ideal for students with **75% attendance requirements**  

Think of it as your **daily attendance safety net**.

---

## 🛠️ Tech Stack (Resume-Ready)

- **Python 3.9** – Core automation logic  
- **Selenium (Headless Chrome)** – Web automation  
- **GitHub Actions** – CI/CD & cron scheduling  
- **Telegram Bot API** – Real-time notifications  

### 📌 Skills Demonstrated
- Automation scripting  
- Secure credential handling  
- Cron-based scheduling  
- API integration  
- Practical problem solving  

Perfect for **college projects, internships, and resumes**.

---

## 🔐 Privacy & Ethics

- No data is shared publicly  
- No logs contain sensitive information  
- Intended strictly for **educational and personal use**  

---

<div align="center">
<sub>Built by a student, for students. Learn automation responsibly.</sub>
</div>
