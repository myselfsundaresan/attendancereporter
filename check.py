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

# --- HELPER: SEND TELEGRAM MESSAGE ---
def send_telegram(msg):
    """Sends a message to Telegram and logs the result for debugging."""
    try:
        bot_token = os.environ.get('BOT_TOKEN')
        chat_id = os.environ.get('CHAT_ID')

        if not bot_token or not chat_id:
            print("❌ DEBUG ERROR: BOT_TOKEN or CHAT_ID is missing from Secrets!")
            return

        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"}
        
        print(f"📨 Attempting to send message to Chat ID: {chat_id}...")
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            print("✅ Telegram message sent successfully!")
        else:
            print(f"❌ TELEGRAM API ERROR: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ CONNECTION ERROR: Could not reach Telegram. {e}")

# 1. READ MEMORY
last_total = 0
last_attended = 0

try:
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as f:
            content = f.read().strip().split(',')
            if len(content) == 2:
                last_total = int(content[0])
                last_attended = int(content[1])
except Exception:
    print("⚠️ Memory file empty or corrupt. Starting fresh from 0,0.")

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

    # 5. SMART COMPARISON LOGIC
    new_data_str = f"{current_total},{current_attended}"
    percentage = round((current_attended / current_total) * 100, 2) if current_total > 0 else 0.0
    
    # Get current date
    today_date = datetime.now().strftime("%d-%m-%Y")

    if current_total > last_total:
        # LOGIC A: Data Changed (Attendance Marked)
        diff_total = current_total - last_total
        diff_attended = current_attended - last_attended
        
        if diff_attended == diff_total:
            status = "Present ✅"
        elif diff_attended == 0:
            status = "Absent ❌"
        else:
            status = f"Partial ({diff_attended}/{diff_total} hrs) ⚠️"

        msg = (f"📅 *Daily Attendance Update* ({today_date})\n"
               f"-----------------------------\n"
               f"Status: *{status}*\n"
               f"-----------------------------\n"
               f"🏫 Total Classes: {last_total} ➝ {current_total}\n"
               f"✅ Your Count: {last_attended} ➝ {current_attended}\n"
               f"📊 Percentage: *{percentage}%*")

        send_telegram(msg)
        
        with open(FILE_NAME, "w") as f:
            f.write(new_data_str)

    elif current_total != last_total:
        # LOGIC B: Data correction
        print("⚠️ Data correction detected.")
        with open(FILE_NAME, "w") as f:
            f.write(new_data_str)

    else:
        # LOGIC C: No Change
        # IMPORTANT: We now send a message here too so you know it's working!
        print("💤 No new attendance marked today.")
        msg = (f"💤 *No New Attendance* ({today_date})\n"
               f"-----------------------------\n"
               f"Attendance hasn't been updated today.\n"
               f"🏫 Current Total: {current_total}\n"
               f"✅ Your Count: {current_attended}\n"
               f"📊 Percentage: *{percentage}%*")
        send_telegram(msg)

except Exception as e:
    print(f"❌ Error: {e}")
    # Try to send the specific error to Telegram to help debug
    error_message = f"⚠️ *Bot Crashed*\nError: `{str(e)}`"
    send_telegram(error_message)

finally:
    driver.quit()
