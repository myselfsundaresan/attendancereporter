import os
import json
import time
import requests
from datetime import datetime, timezone, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- CONFIGURATION ---
FILE_NAME = "last_attendance.txt"

# Safely fetch BASE_URL (Handles GitHub Actions empty strings)
BASE_URL = os.environ.get('BASE_URL', '').strip()
if not BASE_URL:
    BASE_URL = 'https://arms.smc.saveetha.com'
BASE_URL = BASE_URL.rstrip('/')

LOGIN_URL = f"{BASE_URL}/Login.aspx"
REPORT_URL = f"{BASE_URL}/StudentPortal/AttendanceReport.aspx"

# --- HELPER: TELEGRAM FUNCTIONS ---
def get_secrets():
    return {
        "token": os.environ.get('BOT_TOKEN'),
        "chat_id": os.environ.get('CHAT_ID'),
        "gh_pat": os.environ.get('GH_PAT'),
        "repo": os.environ.get('REPO_FULL_NAME')
    }

def delete_message(message_id):
    """Deletes a specific message to keep chat clean."""
    if not message_id: return
    
    secrets = get_secrets()
    token = secrets['token']
    chat_id = secrets['chat_id']
    if not token: return

    try:
        url = f"https://api.telegram.org/bot{token}/deleteMessage"
        payload = {"chat_id": chat_id, "message_id": message_id}
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            print(f"🗑️ Deleted old message ID: {message_id}")
        else:
            print(f"⚠️ Could not delete message {message_id}. API: {response.text}")
    except Exception as e:
        print(f"❌ Delete Error: {e}")

def send_message(msg):
    """Sends a fresh message with a Refresh button."""
    secrets = get_secrets()
    token = secrets['token']
    chat_id = secrets['chat_id']
    if not token: return None

    # Inline Keyboard Button to trigger the GitHub workflow via repository_dispatch
    reply_markup = {
        "inline_keyboard": [[
            {"text": "🔄 Refresh Now", "callback_data": "trigger_gh_action"}
        ]]
    }

    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {
            "chat_id": chat_id, 
            "text": msg, 
            "parse_mode": "Markdown",
            "reply_markup": reply_markup
        }
        
        print(f"📨 Sending new message...")
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            new_id = response.json().get('result', {}).get('message_id')
            print(f"✅ Sent! New ID: {new_id}")
            return new_id
        else:
            print(f"❌ Send Failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Send Error: {e}")
        return None

# 1. READ JSON MEMORY
stored_data = {"date": "", "message_id": None, "subjects": {}}

try:
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as f:
            content = f.read().strip()
            if content.startswith("{"):  # Check if it's valid JSON format
                stored_data = json.loads(content)
            else:
                print("⚠️ Old memory format detected. Upgrading to JSON memory.")
except Exception:
    print("⚠️ Memory file empty or corrupt. Starting fresh.")

# 2. SETUP HEADLESS BROWSER
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")

driver = webdriver.Chrome(options=options)

try:
    print("🚀 Starting Attendance Check...")

    # 3. LOGIN PROCESS
    driver.get(LOGIN_URL)
    wait = WebDriverWait(driver, 25)
    
    wait.until(EC.presence_of_element_located((By.ID, "txtusername")))
    
    driver.find_element(By.ID, "txtusername").send_keys(os.environ['USER_ID'])
    driver.find_element(By.ID, "txtpassword").send_keys(os.environ['PASSWORD'])
    driver.find_element(By.ID, "btnlogin").click()
    print("⏳ Login submitted. Waiting for dashboard...")

    wait.until(EC.url_contains("StudentPortal"))
    print("✅ Login Successful!")

    # 4. NAVIGATE & EXTRACT DATA DYNAMICALLY
    print("➡️ Navigating to Attendance Report...")
    driver.get(REPORT_URL)
    
    wait.until(EC.visibility_of_element_located((By.XPATH, "//table[@id='tblStudent']/tbody/tr")))
    
    # Get all rows in the table
    rows = driver.find_elements(By.XPATH, "//table[@id='tblStudent']/tbody/tr")
    current_data = {}
    
    for row in rows:
        cols = row.find_elements(By.XPATH, "./td")
        if len(cols) >= 6:
            code = cols[1].text.strip()
            name = cols[2].text.strip()
            attended = int(cols[3].text.strip()) # Class Attended Column
            total = int(cols[5].text.strip())    # Total Class Column
            
            # Store in a dictionary by Subject Code
            current_data[code] = {"name": name, "attended": attended, "total": total}

    print(f"📊 Extracted data for {len(current_data)} subjects.")

    # 5. LOGIC: DETERMINE BASELINE & CALCULATE STATS
    ist_timezone = timezone(timedelta(hours=5, minutes=30))
    now_ist = datetime.now(ist_timezone)
    
    today_date = now_ist.strftime("%d-%m-%Y")
    current_time = now_ist.strftime("%I:%M %p")
    
    # Check if it's a new day
    is_new_day = stored_data.get("date") != today_date
    
    if is_new_day:
        print(f"📅 New Day ({today_date})! Setting baseline to current values.")
        msg_id_to_delete = None
        baseline_subjects = {}
    else:
        print("📅 Same Day. Using stored morning baseline.")
        msg_id_to_delete = stored_data.get("message_id")
        baseline_subjects = stored_data.get("subjects", {})

    today_msg_lines = []
    total_overall_classes = 0
    total_overall_attended = 0

    # Calculate differences subject by subject
    for code, data in current_data.items():
        total_overall_classes += data["total"]
        total_overall_attended += data["attended"]
        
        # Get baseline for this specific subject
        if is_new_day or code not in baseline_subjects:
            baseline_subjects[code] = {"name": data["name"], "total": data["total"], "attended": data["attended"]}
            base_total = data["total"]
            base_attended = data["attended"]
        else:
            base_total = baseline_subjects[code]["total"]
            base_attended = baseline_subjects[code]["attended"]
            
        # Calculate what happened TODAY for this subject
        today_held = data["total"] - base_total
        today_present = data["attended"] - base_attended
        
        # Only add to message if a class was actually held today for this subject
        if today_held > 0:
            # Shorten very long subject names to keep the Telegram message clean
            short_name = data["name"][:25] + ".." if len(data["name"]) > 25 else data["name"]
            today_msg_lines.append(f"🔹 *{short_name}* ({code})\n      Held: {today_held} | Present: {today_present}")

    # Build the Subject-wise string
    if not today_msg_lines:
        today_str = "💤 No classes updated yet today."
    else:
        today_str = "\n".join(today_msg_lines)

    overall_percentage = round((total_overall_attended / total_overall_classes) * 100, 2) if total_overall_classes > 0 else 0.0

    # 6. BUILD MESSAGE
    msg = (f"📅 *Daily Attendance Tracker* ({today_date})\n"
           f"⏰ Last Checked: {current_time}\n"
           f"-----------------------------\n"
           f"📝 *Today's Updates*\n"
           f"{today_str}\n"
           f"-----------------------------\n"
           f"📊 *Overall Stats (All Subjects)*\n"
           f"🏫 Total Classes: {total_overall_classes}\n"
           f"✅ Total Attended: {total_overall_attended}\n"
           f"📈 Percentage: *{overall_percentage}%*")

    # 7. DELETE OLD -> SEND NEW
    if msg_id_to_delete:
        delete_message(msg_id_to_delete)
        
    sent_msg_id = send_message(msg)
    
    # 8. SAVE JSON MEMORY
    new_memory = {
        "date": today_date,
        "message_id": sent_msg_id,
        "subjects": baseline_subjects
    }
    
    with open(FILE_NAME, "w") as f:
        json.dump(new_memory, f, indent=4)
        print("💾 JSON Memory updated.")

except Exception as e:
    print(f"❌ Error: {e}")
    error_message = f"⚠️ *Bot Crashed*\nError: `{str(e)}`"
    send_message(error_message)
finally:
    driver.quit()
