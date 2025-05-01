import requests
import time
from datetime import datetime

# ✅ 你的 Discord Webhook URL
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1367376262309613598/WnzNjfBfZnklLCvkYrlR_lWDMdAIoU_2gHBVX1m-piD6tSrfNtcf8fU0F-xCFNjLph1h"

# ✅ Binance 中文站 Proxy API
BINANCE_PROXY_BASE = "https://api-gateway.binancezh.pro"

# ✅ 監控清單（測試用 BTC 設定為 10% 保證觸發）
MONITOR_LIST = {
    "BTCUSDT": 10.0,
    # 可加回：
    # "DOGEUSDT": -0.5,
    # "1000PEPEUSDT": -0.6,
    # "ALPACAUSDT": -0.5,
    # "RNDRUSDT": -0.5
}

def send_discord_alert(symbol, funding_rate):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    message = (
        f"🚨 資金費套利機會出現！\n"
        f"幣種：**{symbol}**\n"
        f"資金費率：`{funding_rate:.2f}%`\n"
        f"時間：{now}\n"
        f"[查看合約](https://www.binance.com/en/futures/{symbol})"
    )
    payload = {"content": message}
    try:
        res = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        print(f"✅ Discord 通知發送成功：狀態碼 {res.status_code}")
    except Exception as e:
        print(f"❌ 發送 Discord 失敗：{e}")

def check_all_funding_rates():
    print("🚀 開始檢查資金費率...")
    for symbol, threshold in MONITOR_LIST.items():
        try:
            url = f"{BINANCE_PROXY_BASE}/fapi/v1/premiumIndex?symbol={symbol}"
            response = requests.get(url)
            data = response.json()

            if "lastFundingRate" not in data:
                print(f"⚠️ 無法獲取 {symbol} 資金費率，API 回傳：{data}")
                continue

            rate = float(data['lastFundingRate']) * 100
            print(f"{symbol} 資金費率為：{rate:.3f}%（門檻 {threshold}）")

            if rate <= threshold:
                print(f"📣 符合條件！通知 {symbol}")
                send_discord_alert(symbol, rate)
            else:
                print(f"🔍 尚未觸發：{rate:.3f}% > {threshold}")
        except Exception as e:
            print(f"❌ 例外錯誤（{symbol}）：{e}")
    print("✅ 資金費檢查結束\n")

# ✅ 每 60 秒掃描一次
while True:
    check_all_funding_rates()
    print("⏳ 等待 60 秒...\n")
    time.sleep(60)
