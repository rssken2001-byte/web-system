# ============================
# ✅ 匯入套件
# ============================

from fastapi import FastAPI
from fastapi.responses import FileResponse
import sqlite3   # ✅ SQLite 資料庫

# ============================
# ✅ 建立網站系統
# ============================

app = FastAPI()


# ============================
# ✅ 建立資料庫（會自動建立 users.db）
# ============================

# 建立資料庫連線（users.db 如果不存在會自動生成）
conn = sqlite3.connect("users.db", check_same_thread=False)

# 建立操作工具（cursor = 滑鼠操作資料庫）
cursor = conn.cursor()


# ============================
# ✅ 建立資料表（如果沒有就建立）
# ============================

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- ✅ 自動編號
    name TEXT,                             -- ✅ 姓名
    phone TEXT                            -- ✅ 電話
)
""")

# ✅ 儲存變更（一定要）
conn.commit()


# ============================
# ✅ 首頁（顯示網頁）
# ============================

@app.get("/")
def home():
    # 回傳 index.html 當畫面
    return FileResponse("index.html")


# ============================
# ✅ 新增資料（Create）
# ============================

@app.post("/add_user")
async def add_user(data: dict):

    # ✅ 從前端拿資料
    name = data.get("name")
    phone = data.get("phone")

    # ✅ 寫入資料庫
    cursor.execute(
        "INSERT INTO users (name, phone) VALUES (?, ?)",
        (name, phone)
    )

    # ✅ 儲存
    conn.commit()

    return {"status": "ok"}


# ============================
# ✅ 查詢資料（Read）
# ============================

@app.get("/users")
def get_users():

    # ✅ 抓全部資料
    cursor.execute("SELECT * FROM users")

    rows = cursor.fetchall()

    # ✅ 轉成 JSON 格式給前端
    result = []
    for r in rows:
        result.append({
            "id": r[0],      # 編號
            "name": r[1],    # 姓名
            "phone": r[2]    # 電話
        })

    return result


# ============================
# ✅ 刪除資料（Delete）
# ============================

@app.delete("/delete_user/{user_id}")
def delete_user(user_id: int):

    # ✅ 根據ID刪除
    cursor.execute(
        "DELETE FROM users WHERE id = ?",   # SQLite 要用 ?
        (user_id,)
    )

    # ✅ 儲存
    conn.commit()

    return {"status": "deleted"}
