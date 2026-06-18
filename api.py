# ============================
# ✅ 匯入套件
# ============================

from fastapi import FastAPI
from fastapi.responses import FileResponse
import sqlite3   # ✅ SQLite（輕量資料庫）

app = FastAPI()

# ============================
# ✅ 建立資料庫（第一次會自動建立）
# ============================

conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

# ✅ 建表（如果沒有就自動建立）
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

    # ✅ 存進SQL資料庫
    cursor.execute(
        "INSERT INTO users (name, phone) VALUES (?, ?)",
        (name, phone)
    )

    conn.commit()  # ✅ 一定要儲存！

    print("✅ 已存SQL：", name, phone)

    return {"status": "ok"}


# ============================
# ✅ 查詢資料（進階）
# ============================

@app.get("/users")
def get_users():

    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    # ✅ 轉成JSON格式
    result = []
    for r in rows:
        result.append({
            "id": r[0],
            "name": r[1],
            "phone": r[2]
        })

    return result
