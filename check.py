import os
import time
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
# Add User-Agent to prevent bot detection
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")

driver = webdriver.Chrome(options=options)

try:
    print("🚀 Starting Attendance Check...")

    # 3. LOGIN PROCESS
    driver.get(LOGIN_URL)
    wait = WebDriverWait(driver, 25) # Increased wait time
    
    # Wait for username field
    wait.until(EC.presence_of_element_located((By.ID, "txtusername")))
    
    # Enter Credentials
    driver.find_element(By.ID, "txtusername").send_keys(os.environ['USER_ID'])
    driver.find_element(By.ID, "txtpassword").send_keys(os.environ['PASSWORD'])
    driver.find_element(By.ID, "btnlogin").click()
    print("⏳ Login submitted. Waiting for dashboard...")

    # CRITICAL FIX: Wait for login to actually finish
    # We wait until the URL changes to something with "StudentPortal"
    # OR wait for the "Log Out" button to appear
    try:
        wait.until(EC.url_contains("StudentPortal"))
        print("✅ Login Successful! Redirected to Portal.")
    except:
        # If URL didn't change, maybe we are still on login page?
        print(f"⚠️ Warning: URL is still {driver.current_url}")
        # Check for error message on screen
        try:
            error_msg = driver.find_element(By.ID, "lblError").text
            raise Exception(f"Login Failed: {error_msg}")
        except:
            pass

    # 4. NAVIGATE & EXTRACT DATA
    print("➡️ Navigating to Attendance Report...")
    driver.get(REPORT_URL)
    
    # Wait specifically for the TABLE ROW to be visible, not just the table
    # This ensures data is actually loaded
    row_xpath = "//table[@id='tblStudent']/tbody/tr[1]"
    wait.until(EC.visibility_of_element_located((By.XPATH, row_xpath)))
    
    # Locate data
    total_xpath = "//table[@id='tblStudent']/tbody/tr[1]/td[6]"
    attended_xpath = "//table[@id='tblStudent']/tbody/tr[1]/td[4]"
    
    current_total = int(driver.find_element(By.XPATH, total_xpath).text)
    current_attended = int(driver.find_element(By.XPATH, attended_xpath).text)
    
    print(f"📊 Extracted -> Total: {current_total}, Attended: {current_attended}")

    # 5. SMART COMPARISON LOGIC
    bot_token = os.environ['BOT_TOKEN']
    chat_id = os.environ['CHAT_ID']
    new_data_str = f"{current_total},{current_attended}"
    
    if current_total > last_total:
        diff_total = current_total - last_total
        diff_attended = current_attended - last_attended
        
        if diff_attended == diff_total:
            status = "Present ✅"
        elif diff_attended == 0:
            status = "Absent ❌"
        else:
            status = f"Partial ({diff_attended}/{diff_total} hrs) ⚠️"

        msg = (f"📅 *Daily Attendance Update*\n"
               f"-----------------------------\n"
               f"Status: *{status}*\n"
               f"-----------------------------\n"
               f"🏫 Total Classes: {last_total} ➝ {current_total}\n"
               f"✅ Your Count: {last_attended} ➝ {current_attended}")

        requests.get(f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={msg}&parse_mode=Markdown")
        
        with open(FILE_NAME, "w") as f:
            f.write(new_data_str)

    elif current_total != last_total:
        print("⚠️ Data correction detected.")
        with open(FILE_NAME, "w") as f:
            f.write(new_data_str)

    else:
        print("💤 No new attendance marked today.")

except Exception as e:
    print(f"❌ Error: {e}")
    # Print page source to debug if needed (optional)
    # print(driver.page_source[:500]) 
    
    try:
        bot_token = os.environ['BOT_TOKEN']
        chat_id = os.environ['CHAT_ID']
        requests.get(f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text=⚠️ Script Error: {str(e)}")
    except:
        pass

finally:
    driver.quit()
