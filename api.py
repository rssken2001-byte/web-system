# ============================
# ✅ 匯入套件
# ============================

from fastapi import FastAPI
from fastapi.responses import FileResponse, Response
import sqlite3
import csv
import io  # ✅ 用來在記憶體建立檔案

# ============================
# ✅ 建立網站系統
# ============================

app = FastAPI()


# ============================
# ✅ 建立資料庫
# ============================

conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

# ✅ 建立資料表
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    phone TEXT
)
""")

conn.commit()


# ============================
# ✅ 首頁（顯示網頁）
# ============================

@app.get("/")
def home():
    return FileResponse("index.html")


# ============================
# ✅ 新增資料（Create）
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
# ✅ 查詢資料（Read）
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
# ✅ 刪除資料（Delete）
# ============================

@app.delete("/delete_user/{user_id}")
def delete_user(user_id: int):

    cursor.execute(
        "DELETE FROM users WHERE id = ?",
        (user_id,)
    )

    conn.commit()

    return {"status": "deleted"}


# ============================
# ✅ ✅ ✅ 匯出 CSV（新增功能🔥）
# ============================

@app.get("/download_csv")
def download_csv():

    # ✅ 1️⃣ 從資料庫抓資料
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    # ✅ 2️⃣ 在記憶體建立「CSV檔案」
    output = io.StringIO()

    writer = csv.writer(output)

    # ✅ 3️⃣ 寫表頭
    writer.writerow(["ID", "姓名", "電話"])

    # ✅ 4️⃣ 寫資料
    for r in rows:
        writer.writerow(r)

    # ✅ 5️⃣ 回傳下載檔案
    return Response(
        content=output.getvalue(),   # CSV內容
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=customers.csv"
        }
    )
