# Funding Rate Alert (Discord)

這是一個自動監控幣圈資金費率套利機會的 Python 腳本。部署於雲端（如 Render）後，將每 30 分鐘檢查一次指定幣種，若資金費率低於設定門檻，就會發送 Discord 通知。

## 使用幣種與門檻（已設定）

- BTCUSDT：-0.3%
- DOGEUSDT：-0.5%
- 1000PEPEUSDT：-0.6%
- ALPACAUSDT：-0.5%
- RNDRUSDT：-0.5%

## 部署方式（Render）

1. 將此專案上傳至你的 GitHub。
2. 登入 [https://render.com](https://render.com)
3. 點「New」→ 「Web Service」
4. 選擇你上傳的 repo
5. 設定如下：

- Build Command: *(空白)*
- Start Command: `python funding_alert.py`
- Plan: Free

即可自動啟動並持續執行。

