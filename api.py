# ============================
# ✅ 匯入套件
# ============================

from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse
import sqlite3
from openpyxl import Workbook
import io

# ============================
# ✅ 建立網站
# ============================

app = FastAPI()


# ============================
# ✅ 建立資料庫
# ============================

conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    phone TEXT
)
""")
conn.commit()


# ============================
# ✅ 首頁
# ============================

@app.get("/")
def home():
    return FileResponse("index.html")


# ============================
# ✅ 新增資料
# ============================

@app.post("/add_user")
async def add_user(data: dict):

    name = data.get("name")
    phone = data.get("phone")

    cursor.execute(
        "INSERT INTO users (name, phone) VALUES (?, ?)",
        (name, phone)
    )
    conn.commit()

    return {"status": "ok"}


# ============================
# ✅ 讀取資料（給前端）
# ============================

@app.get("/users")
def get_users():

    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    result = []
    for r in rows:
        result.append({
            "id": r[0],
            "name": r[1],
            "phone": r[2]
        })

    return result


# ============================
