import requests
import time
from datetime import datetime

# Discord Webhook URL（你的專屬 Webhook）
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1367376262309613598/WnzNjfBfZnklLCvkYrlR_lWDMdAIoU_2gHBVX1m-piD6tSrfNtcf8fU0F-xCFNjLph1h"

# 監控幣種與資金費率門檻（百分比）
MONITOR_LIST = {
    "BTCUSDT": 10.0,
    "DOGEUSDT": -0.5,
    "1000PEPEUSDT": -0.6,
    "ALPACAUSDT": -0.5,
    "RNDRUSDT": -0.5
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
    requests.post(DISCORD_WEBHOOK_URL, json=payload)

def check_all_funding_rates():
    for symbol, threshold in MONITOR_LIST.items():
        try:
            url = f"https://fapi.binance.com/fapi/v1/premiumIndex?symbol={symbol}"
            response = requests.get(url)
            data = response.json()
            rate = float(data['lastFundingRate']) * 100
            print(f"{symbol} 資金費率：{rate:.3f}%")
            if rate <= threshold:
                send_discord_alert(symbol, rate)
        except Exception as e:
            print(f"錯誤：{symbol} 無法獲取資金費率：{e}")

while True:
    print("開始檢查資金費率...")
    check_all_funding_rates()
    print("休息 30 分鐘")
    time.sleep(60 * 30)
