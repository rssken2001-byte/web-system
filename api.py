from fastapi import FastAPI
from fastapi.responses import FileResponse
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta
import json
import os

app = FastAPI()

# ✅ Google Sheet 連線
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

google_key = json.loads(os.environ["GOOGLE_KEY"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(google_key, scope)
client = gspread.authorize(creds)

sheet = client.open("linebot-log").worksheet("web-data")

# ✅ 首頁（顯示網頁）
@app.get("/")
def home():
    return FileResponse("index.html")

# ✅ 新增資料
@app.post("/add_user")
async def add_user(data: dict):

    name = data.get("name")
    phone = data.get("phone")

    sheet.append_row([
        str(datetime.now() + timedelta(hours=8)),
        name,
        phone
    ])

    return {"status": "ok"}
