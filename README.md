# 🚀 Taiwan Overtime Oracle (台灣加班神諭)

這是一個為台灣軟體工程師打造的自動化工具。結合 **勞基法加班費率邏輯** 與 **政府放假資料**，自動計算出每個月「CP 值最高」的加班時段，並透過 Discord 每日提醒。

## 💡 核心價值 (Why this project?)
身為開發者，常需因專案時程加班。本專案透過技術手段解決資訊不對稱，確保每小時的付出都能獲得法規下的最大化報酬。

## 🛠️ 技術棧 (Tech Stack)
- **Language:** Python 3.9
- **Automation:** GitHub Actions (CI/CD / Cron Job)
- **Data Source:** [政府資料開放平台 - 中華民國人事行政總處辦公日曆表](https://data.gov.tw/dataset/14718)
- **Notification:** Discord Webhook API
- **Deployment:** Serverless (Running on GitHub Infrastructure)

## ✨ 主要功能
- **動態爬蟲機制：** 自動偵測並抓取政府最新的年度 JSON 資料源，解決 URL 固定 NID 但 MD5 隨版本更動的問題。
- **智能費率分析：** - **金礦日 (Gold):** 自動識別國定假日與補假（加倍薪且不計入 46 小時上限）。
    - **精選日 (Silver):** 每週擇優推薦「休息日」時段，極大化邊際收益。
- **雙重提醒機制：** - **每月 1 號：** 發布全月完整加班攻略。
    - **每日 9:00：** 若當日為推薦加班日，自動推送提醒及「加班預計單」快速連結。
- **Fail-safe 機制：** 具備完善的 Log 日誌系統與異常處理，當政府 API 格式異動時會主動發送警告。

## 📸 運作截圖
> (此處可以貼上你 Discord 收到訊息的截圖，會非常有說服力！)

## ⚙️ 環境設定
1. 在 GitHub Secrets 中設定 `DISCORD_WEBHOOK`。
2. 系統將根據 `.github/workflows/daily_cron.yml` 自動執行。

## 📝 勞基法邏輯實作
本系統嚴格遵循中華民國《勞基法》第 24、39 條之規範：
- 國定假日：前 8 小時加倍發給工資。
- 休息日：採 1.34x, 1.67x, 2.67x 階梯式費率計算。