import os
import time
import requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- CONFIGURATION ---
FILE_NAME = "last_attendance.txt"
LOGIN_URL = "https://arms.smc.saveetha.com/Login.aspx"
REPORT_URL = "https://arms.smc.saveetha.com/StudentPortal/AttendanceReport.aspx"

# --- HELPER: SEND OR EDIT TELEGRAM MESSAGE ---
def send_telegram(msg, message_id=None):
    """
    Sends a new message OR edits an existing one if message_id is provided.
    Returns the message_id of the sent/edited message.
    """
    try:
        bot_token = os.environ.get('BOT_TOKEN')
        chat_id = os.environ.get('CHAT_ID')

        if not bot_token or not chat_id:
            print("❌ DEBUG ERROR: BOT_TOKEN or CHAT_ID is missing from Secrets!")
            return None

        # 1. Try to EDIT existing message if ID is provided
        if message_id:
            print(f"✏️ Attempting to edit Message ID: {message_id}...")
            edit_url = f"https://api.telegram.org/bot{bot_token}/editMessageText"
            edit_payload = {
                "chat_id": chat_id, 
                "message_id": message_id, 
                "text": msg, 
                "parse_mode": "Markdown"
            }
            response = requests.post(edit_url, json=edit_payload)
            
            # If successful (200) or if message content is exactly same (400 - "message is not modified"), return ID
            if response.status_code == 200:
                print("✅ Message edited successfully!")
                return message_id
            elif response.status_code == 400 and "message is not modified" in response.text:
                print("ℹ️ Content unchanged, skipping edit.")
                return message_id
            
            print(f"⚠️ Edit failed ({response.status_code}), sending new message instead.")

        # 2. Fallback: SEND NEW message (if no ID provided or edit failed)
        send_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"}
        
        print(f"📨 Sending new message to Chat ID: {chat_id}...")
        response = requests.post(send_url, json=payload)
        
        if response.status_code == 200:
            print("✅ New Telegram message sent!")
            return response.json().get('result', {}).get('message_id')
        else:
            print(f"❌ TELEGRAM API ERROR: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ CONNECTION ERROR: Could not reach Telegram. {e}")
        return None

# 1. READ MEMORY (Format: "Total,Attended,MessageID,Date")
last_total = 0
last_attended = 0
last_msg_id = None
last_date = ""

try:
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as f:
            content = f.read().strip().split(',')
            # Support both old format (2 items) and new format (4 items)
            if len(content) >= 2:
                last_total = int(content[0])
                last_attended = int(content[1])
            if len(content) == 4:
                last_msg_id = int(content[2]) if content[2] != 'None' else None
                last_date = content[3]
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

    # 5. SMART LOGIC & MESSAGING
    today_date = datetime.now().strftime("%d-%m-%Y")
    current_time = datetime.now().strftime("%I:%M %p")
    
    # Determine Message ID to use
    # If today matches the stored date, we EDIT the existing message.
    # Otherwise (new day), we start fresh (msg_id = None).
    msg_id_to_use = last_msg_id if (last_date == today_date) else None
    
    # Calculate Stats
    percentage = round((current_attended / current_total) * 100, 2) if current_total > 0 else 0.0
    
    # Determine Status Logic
    # Note: We compare against 'last_total' to show daily progress, 
    # but if it's a new day, 'last_total' might be yesterday's final count.
    
    diff_total = current_total - last_total
    diff_attended = current_attended - last_attended
    
    status = "No classes yet today 💤"
    
    if diff_total > 0:
        if diff_attended == diff_total:
            status = f"Present ({diff_attended}/{diff_total} classes) ✅"
        elif diff_attended == 0:
            status = f"Absent ({diff_total} classes missed) ❌"
        else:
            status = f"Partial ({diff_attended}/{diff_total} hrs) ⚠️"
    elif last_date == today_date and diff_total == 0:
        # If running multiple times same day and no change
        status = "No new updates since last check ⏳"

    msg = (f"📅 *Daily Attendance Tracker* ({today_date})\n"
           f"⏰ Last Checked: {current_time}\n"
           f"-----------------------------\n"
           f"Status: *{status}*\n"
           f"-----------------------------\n"
           f"🏫 Total Classes: {current_total}\n"
           f"✅ Your Count: {current_attended}\n"
           f"📊 Percentage: *{percentage}%*")

    # Send or Edit Telegram Message
    sent_msg_id = send_telegram(msg, msg_id_to_use)
    
    # Update Memory File
    # Format: Total, Attended, MessageID, Date
    # We save current stats so next run today compares against these
    # actually, for correct "daily progress", we might want to keep 'last_total' as start-of-day? 
    # But for simplicity, we just save current state.
    
    final_msg_id = sent_msg_id if sent_msg_id else last_msg_id
    new_data_str = f"{current_total},{current_attended},{final_msg_id},{today_date}"
    
    with open(FILE_NAME, "w") as f:
        f.write(new_data_str)
        print("💾 Memory updated.")

except Exception as e:
    print(f"❌ Error: {e}")
    error_message = f"⚠️ *Bot Crashed*\nError: `{str(e)}`"
    send_telegram(error_message)

finally:
    driver.quit()
