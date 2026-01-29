<!-- ANIMATED HEADER -->

<div align="center">
<img src="https://www.google.com/search?q=https://readme-typing-svg.herokuapp.com%3Ffont%3DFira%2BCode%26weight%3D600%26size%3D30%26duration%3D3000%26pause%3D1000%26color%3D249c32%26center%3Dtrue%26vCenter%3Dtrue%26width%3D500%26lines%3DSaveetha%2BAttendance%2BBot%3BAutomated%2BDaily%2BChecks%3BSmart%2BAbsent%2Bvs%2BPresent%2BLogic%3BZero-Touch%2BAutomation" alt="Typing SVG" />
</div>

<!-- BADGES -->

<div align="center">

</div>

🤖 What is this?

This is a fully automated "Zero-Touch" bot that checks your college attendance daily. It goes beyond simple scraping—it uses smart logic to interpret the data.

Instead of just reading the number, it compares your Total Classes count from yesterday against today to mathematically determine if you were marked Present or Absent.

⚡ Smart Logic Table

The bot tracks two numbers: Total Classes and Classes Attended.

Scenario

Bot Analysis

Status Report

Total Class ↑ & Attended ↑

"Attendance taken and you were there."

Present ✅

Total Class ↑ & Attended -

"Attendance taken, but your count stayed same."

Absent ❌

Total Class -

"No attendance taken today (or Holiday)."

Silent (or "No new attendance")

🚀 How to Set Up in 2 Minutes

1. Fork this Repo

Click the Fork button at the top right of this page to save a copy to your own GitHub account.

2. Add Your Secrets

Go to your repo Settings > Secrets and variables > Actions and add these 4 keys:

Secret Name

Value

USER_ID

Your College Roll Number / Login ID

PASSWORD

Your Portal Password

BOT_TOKEN

Token from Telegram's @BotFather

CHAT_ID

Your Personal Chat ID (from @userinfobot)

3. Initialize Memory

Create a file named last_attendance.txt in your repo and write exactly this inside:

0,0


4. Enable Workflow

Go to the Actions tab and enable the workflow. It is scheduled to run automatically every day at 9:30 AM IST.

🛠️ Tech Stack

Core: Python 3.9

Engine: Selenium (Headless Chrome)

Infrastructure: GitHub Actions (Cron Job)

Notifications: Telegram Bot API

<div align="center">
<sub>Built for educational purposes. Use responsibly.</sub>
</div>
