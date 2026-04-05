import os
import requests
from datetime import datetime
from holiday_api import get_holidays
from logic import analyze_month

def send_to_discord(content):
    webhook_url = os.getenv('DISCORD_WEBHOOK')
    if not webhook_url:
        print("🚨 [Discord] 未設定 Webhook URL (DISCORD_WEBHOOK)")
        return
    
    payload = {"content": content}
    try:
        res = requests.post(webhook_url, json=payload)
        if res.status_code == 204 or res.status_code == 200:
            print("🚀 [Discord] 訊息發送成功！")
        else:
            print(f"❌ [Discord] 發送失敗，狀態碼: {res.status_code}")
    except Exception as e:
        print(f"💥 [Discord] 發送過程發生異常: {str(e)}")

def main():
    print("--- 🏁 加班攻略系統啟動 ---")
    now = datetime.now()
    year, month = now.year, now.month
    
    print(f"📅 目標時段: {year} 年 {month} 月")
    
    holidays = get_holidays(year)
    
    print("🧠 [Step 3] 正在執行勞基法加班邏輯分析...")
    strategy = analyze_month(year, month, holidays)
    
    # 建立 Discord 訊息
    msg = [f"🚀 **{year}年{month}月 加班賺錢攻略**"]
    
    if not strategy["gold"]:
        msg.append("\n⚠️ **注意：本月系統未偵測到國定假日/補假！**")
        msg.append("> 請確認政府 API 網址是否異動，或本月確實無國定假日。")
        print("📢 狀態：本月無國定假日。")
    else:
        msg.append("\n💰 **【五星級金礦】(雙倍薪/不計上限)**")
        for item in strategy["gold"]:
            msg.append(f"• {item['date'].strftime('%m/%d')} ({item['name']}) - 報 8 小時")
        print(f"📢 狀態：偵測到 {len(strategy['gold'])} 個金礦日。")

    if strategy["silver"]:
        msg.append("\n🥈 **【每週精選】(本週六最划算)**")
        msg.append("這幾天建議挑一天報 10 小時：")
        silver_count = 0
        for d in strategy["silver"]:
            if any(g['date'] == d for g in strategy['gold']): continue
            msg.append(f"• {d.strftime('%m/%d')} (週六休息日) - 報 10 小時")
            silver_count += 1
        print(f"📢 狀態：偵測到 {silver_count} 個週六推薦。")

    msg.append("\n💡 *其餘時數建議由平日加班補足至 46 小時。*")
    
    print("📡 [Step 4] 準備將攻略發送至 Discord...")
    send_to_discord("\n".join(msg))
    print("--- 🏁 加班攻略系統結束 ---")

if __name__ == "__main__":
    main()