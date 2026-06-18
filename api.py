# ============================
# ✅ 匯入套件（系統基本功能）
# ============================
from fastapi import FastAPI
from fastapi.responses import FileResponse

# 建立網站 (API伺服器)
app = FastAPI()


# ============================
# ✅ 首頁（打開會看到網頁）
# ============================
@app.get("/")
def home():
    # 回傳 index.html（前端畫面）
    return FileResponse("index.html")


# ============================
# ✅ 新增資料（按按鈕時觸發）
# ============================
@app.post("/add_user")
async def add_user(data: dict):

    # ✅ 從前端拿使用者輸入的資料
    name = data.get("name")   # 取得姓名
    phone = data.get("phone") # 取得電話

    # ✅ 目前先「印出來」（測試系統是否正常）
    print("✅ 新增資料：", name, phone)

    # ✅ 回傳成功訊息給前端
    return {"status": "ok"}
