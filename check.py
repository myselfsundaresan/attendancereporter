import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- CONFIGURATION ---
FILE_NAME = "last_attendance.txt"
LOGIN_URL = "https://arms.smc.saveetha.com/Login.aspx"
REPORT_URL = "https://arms.smc.saveetha.com/StudentPortal/AttendanceReport.aspx"

# 1. READ MEMORY (Format: "Total,Attended")
# We read the previous day's data to compare
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
driver = webdriver.Chrome(options=options)

try:
    print("🚀 Starting Attendance Check...")

    # 3. LOGIN PROCESS
    driver.get(LOGIN_URL)
    wait = WebDriverWait(driver, 20)
    
    # Wait for username field
    wait.until(EC.presence_of_element_located((By.ID, "txtusername")))
    
    # Enter Credentials
    driver.find_element(By.ID, "txtusername").send_keys(os.environ['USER_ID'])
    driver.find_element(By.ID, "txtpassword").send_keys(os.environ['PASSWORD'])
    driver.find_element(By.ID, "btnlogin").click()
    print("✅ Login submitted.")

    # 4. NAVIGATE & EXTRACT DATA
    # Jump directly to report page to save time
    driver.get(REPORT_URL)
    wait.until(EC.presence_of_element_located((By.ID, "tblStudent")))
    
    # Locate data in the first row of the table
    # Column 6 = Total Class | Column 4 = Class Attended
    total_xpath = "//table[@id='tblStudent']/tbody/tr[1]/td[6]"
    attended_xpath = "//table[@id='tblStudent']/tbody/tr[1]/td[4]"
    
    current_total = int(driver.find_element(By.XPATH, total_xpath).text)
    current_attended = int(driver.find_element(By.XPATH, attended_xpath).text)
    
    print(f"📊 Extracted -> Total: {current_total}, Attended: {current_attended}")

    # 5. SMART COMPARISON LOGIC
    bot_token = os.environ['BOT_TOKEN']
    chat_id = os.environ['CHAT_ID']
    new_data_str = f"{current_total},{current_attended}"
    
    # LOGIC A: Attendance was taken (Total classes increased)
    if current_total > last_total:
        
        diff_total = current_total - last_total
        diff_attended = current_attended - last_attended
        
        # Determine Status
        if diff_attended == diff_total:
            status = "Present ✅"
        elif diff_attended == 0:
            status = "Absent ❌"
        else:
            status = f"Partial ({diff_attended}/{diff_total} hrs) ⚠️"

        # Build Message
        msg = (f"📅 *Daily Attendance Update*\n"
               f"-----------------------------\n"
               f"Status: *{status}*\n"
               f"-----------------------------\n"
               f"🏫 Total Classes: {last_total} ➝ {current_total}\n"
               f"✅ Your Count: {last_attended} ➝ {current_attended}")

        # Send Telegram Notification
        requests.get(f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={msg}&parse_mode=Markdown")
        
        # Save new data to memory file
        with open(FILE_NAME, "w") as f:
            f.write(new_data_str)

    # LOGIC B: Data correction or weird reset (Total changed but not increased normally)
    elif current_total != last_total:
        print("⚠️ Data mismatch/correction detected. Updating memory silently.")
        with open(FILE_NAME, "w") as f:
            f.write(new_data_str)

    # LOGIC C: No change (Holiday or Sunday)
    else:
        print("💤 No new attendance marked today.")
        # Optional: Uncomment below if you want a daily message even on holidays
        # requests.get(f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text=No attendance marked today yet.")

except Exception as e:
    print(f"❌ Error: {e}")
    # Optional: Notify you if the script crashes
    try:
        bot_token = os.environ['BOT_TOKEN']
        chat_id = os.environ['CHAT_ID']
        requests.get(f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text=⚠️ Script Error: {str(e)}")
    except:
        pass

finally:
    driver.quit()