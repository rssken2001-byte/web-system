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

# 建立資料庫（users.db 不存在會自動建立）
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

# 建立資料表
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
# ✅ 查詢資料
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
# ✅ 刪除資料
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
# ✅ Excel下載（重點🔥）
# ============================

@app.get("/download_excel")
def download_excel():

    # ✅ 建立 Excel 檔案
    wb = Workbook()
    ws = wb.active
    ws.title = "customers"

    # ✅ 表頭
    ws.append(["ID", "姓名", "電話"])

    # ✅ 讀資料
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    # ✅ 寫入 Excel
    for r in rows:
        ws.append(r)

    # ✅ 存到記憶體
    file = io.BytesIO()
    wb.save(file)
    file.seek(0)

    # ✅ 回傳下載
    return StreamingResponse(
        file,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": "attachment; filename=customers.xlsx"
        }
    )
