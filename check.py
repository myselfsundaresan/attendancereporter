import os
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
LOGIN_URL = "https://arms.smc.saveetha.com/Login.aspx"
REPORT_URL = "https://arms.smc.saveetha.com/StudentPortal/AttendanceReport.aspx"

# --- HELPER: TELEGRAM FUNCTIONS ---
def get_secrets():
    token = os.environ.get('BOT_TOKEN')
    chat_id = os.environ.get('CHAT_ID')
    if not token or not chat_id:
        print("❌ DEBUG ERROR: BOT_TOKEN or CHAT_ID is missing!")
        return None, None
    return token, chat_id

def delete_message(message_id):
    """Deletes a specific message to keep chat clean."""
    if not message_id: return
    
    token, chat_id = get_secrets()
    if not token: return

    try:
        url = f"https://api.telegram.org/bot{token}/deleteMessage"
        payload = {"chat_id": chat_id, "message_id": message_id}
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            print(f"🗑️ Deleted old message ID: {message_id}")
        else:
            print(f"⚠️ Could not delete message {message_id} (It might not exist anymore). API: {response.text}")
    except Exception as e:
        print(f"❌ Delete Error: {e}")

def send_message(msg):
    """Sends a fresh message (triggers notification sound)."""
    token, chat_id = get_secrets()
    if not token: return None

    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"}
        
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

# 1. READ MEMORY (Format: "StartTotal,StartAttended,MessageID,Date")
stored_total = 0
stored_attended = 0
stored_msg_id = None
stored_date = ""

try:
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as f:
            content = f.read().strip().split(',')
            if len(content) == 4:
                stored_total = int(content[0])
                stored_attended = int(content[1])
                stored_msg_id = int(content[2]) if content[2] != 'None' else None
                stored_date = content[3]
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

    try:
        wait.until(EC.url_contains("StudentPortal"))
        print("✅ Login Successful! Redirected to Portal.")
    except:
        print(f"⚠️ Warning: URL is still {driver.current_url}")
        try:
            error_msg = driver.find_element(By.ID, "lblError").text
            raise Exception(f"Login Failed: {error_msg}")
        except:
            pass

    # 4. NAVIGATE & EXTRACT DATA
    print("➡️ Navigating to Attendance Report...")
    driver.get(REPORT_URL)
    
    row_xpath = "//table[@id='tblStudent']/tbody/tr[1]"
    wait.until(EC.visibility_of_element_located((By.XPATH, row_xpath)))
    
    total_xpath = "//table[@id='tblStudent']/tbody/tr[1]/td[6]"
    attended_xpath = "//table[@id='tblStudent']/tbody/tr[1]/td[4]"
    
    current_total = int(driver.find_element(By.XPATH, total_xpath).text)
    current_attended = int(driver.find_element(By.XPATH, attended_xpath).text)
    
    print(f"📊 Extracted -> Total: {current_total}, Attended: {current_attended}")

    # 5. LOGIC: DETERMINE BASELINE FOR TODAY
    ist_timezone = timezone(timedelta(hours=5, minutes=30))
    now_ist = datetime.now(ist_timezone)
    
    today_date = now_ist.strftime("%d-%m-%Y")
    current_time = now_ist.strftime("%I:%M %p")
    
    # Check if it's a new day or same day
    if stored_date != today_date:
        print("📅 New Day Detected! Resetting baseline.")
        baseline_total = current_total
        baseline_attended = current_attended
        # No message to delete if it's a brand new day (optional, or we could delete yesterday's last msg)
        # Let's keep yesterday's history? Or delete it? 
        # User said "update", usually implies keeping daily history is fine, 
        # but for "no spam", we only delete TODAY's previous message.
        msg_id_to_delete = None 
    else:
        print("📅 Same Day. Keeping previous baseline.")
        baseline_total = stored_total
        baseline_attended = stored_attended
        msg_id_to_delete = stored_msg_id # Delete the message from earlier today

    # Calculate Today's Stats
    today_classes_held = current_total - baseline_total
    today_classes_present = current_attended - baseline_attended
    
    percentage = round((current_attended / current_total) * 100, 2) if current_total > 0 else 0.0

    # 6. BUILD MESSAGE
    msg = (f"📅 *Daily Attendance Tracker* ({today_date})\n"
           f"⏰ Last Checked: {current_time}\n"
           f"-----------------------------\n"
           f"📝 *Today's Stats*\n"
           f"✅ No. of classes present: {today_classes_present}\n"
           f"🏫 No. of classes today: {today_classes_held}\n"
           f"-----------------------------\n"
           f"📊 *Overall Stats*\n"
           f"🏫 Total Classes: {current_total}\n"
           f"✅ Total Attended: {current_attended}\n"
           f"📈 Percentage: *{percentage}%*")

    # 7. DELETE OLD -> SEND NEW
    if msg_id_to_delete:
        delete_message(msg_id_to_delete)
        
    sent_msg_id = send_message(msg)
    
    # 8. SAVE MEMORY
    # Save the NEW message ID so we can delete it next time
    final_msg_id = sent_msg_id if sent_msg_id else "None"
    new_data_str = f"{baseline_total},{baseline_attended},{final_msg_id},{today_date}"
    
    with open(FILE_NAME, "w") as f:
        f.write(new_data_str)
        print("💾 Memory updated.")

except Exception as e:
    print(f"❌ Error: {e}")
    error_message = f"⚠️ *Bot Crashed*\nError: `{str(e)}`"
    send_message(error_message)

finally:
    driver.quit()
