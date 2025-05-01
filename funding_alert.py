import requests
import time
from datetime import datetime

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1367376262309613598/WnzNjfBfZnklLCvkYrlR_lWDMdAIoU_2gHBVX1m-piD6tSrfNtcf8fU0F-xCFNjLph1h"

MONITOR_LIST = {
    "BTCUSDT": 10.0  # 強制觸發測試用
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
    res = requests.post(DISCORD_WEBHOOK_URL, json=payload)
    print(f"✅ 發送 Discord 通知狀態碼：{res.status_code}")

def check_all_funding_rates():
    print("🚀 開始檢查資金費率...")
    for symbol, threshold in MONITOR_LIST.items():
        try:
            url = f"https://fapi.binance.com/fapi/v1/premiumIndex?symbol={symbol}"
            response = requests.get(url)
            data = response.json()
            rate = float(data['lastFundingRate']) * 100
            print(f"{symbol} 資金費率為：{rate:.3f}%（門檻 {threshold}）")
            if rate <= threshold:
                print(f"📣 符合條件！準備通知 {symbol}")
                send_discord_alert(symbol, rate)
            else:
                print(f"🔍 尚未觸發條件：{rate:.3f}% > {threshold}")
        except Exception as e:
            print(f"❌ 錯誤：{symbol} 無法獲取資金費率：{e}")
    print("✅ 本輪檢查結束\n")

while True:
    check_all_funding_rates()
    print("⏳ 等待 5 秒後再次檢查...\n")
    time.sleep(5)
