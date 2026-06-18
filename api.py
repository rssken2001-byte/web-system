# ============================
# ✅ 匯入套件（必要工具）
# ============================

from fastapi import FastAPI                # 建立網站API
from fastapi.responses import FileResponse # 回傳網頁檔

# ============================
# ✅ 建立系統（網站主體）
# ============================

app = FastAPI()   # 建立一個網站（後端系統）


# ============================
# ✅ 首頁（打開網址會顯示畫面）
# ============================

@app.get("/")
def home():
    # 回傳 index.html（畫面）
    return FileResponse("index.html")


# ============================
# ✅ API：新增資料（按按鈕會呼叫）
# ============================

@app.post("/add_user")
async def add_user(data: dict):

    # ✅ 取得前端傳來的資料
    name = data.get("name")     # 姓名
    phone = data.get("phone")   # 電話

    # ✅ 在後台印出（測試用）
    print("✅ 新增資料：", name, phone)

    # ✅ 回傳成功給前端
    return {"status": "ok"}
