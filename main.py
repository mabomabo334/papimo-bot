from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
import time
import gspread
from google.oauth2.service_account import Credentials

# ===== Google設定 =====
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

CREDS_FILE = "service_account.json"
SPREADSHEET_ID = "1DaL9_h-sTILEeoDRT637DC8Btg8EAdwGQ4AMZtoeISc"

creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
client = gspread.authorize(creds)
sheet = client.open_by_key(SPREADSHEET_ID).sheet1

# ===== スクレイピング =====
driver = webdriver.Chrome()

url = "https://papimo.jp/h/00041919/hit/index_machine/1-20-765071"
driver.get(url)

time.sleep(3)

today = datetime.now().strftime("%Y-%m-%d")

rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")

data = []

for row in rows:
    cols = row.find_elements(By.TAG_NAME, "td")

    if len(cols) >= 3:
        try:
            machine = cols[0].text
            unit = cols[1].text
            games = cols[2].text

            data.append([today, unit, machine, games])
        except:
            pass

driver.quit()

# ===== スプレッドシートへ書き込み =====
for r in data:
    sheet.append_row(r)

print("完了")
