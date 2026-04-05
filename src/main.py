import os
import requests
from datetime import datetime
from holiday_api import get_holidays
from logic import analyze_month

def send_to_discord(content):
    webhook_url = os.getenv('DISCORD_WEBHOOK')
    if not webhook_url:
        print("未設定 Webhook URL")
        return
    
    payload = {"content": content}
    requests.post(webhook_url, json=payload)

def main():
    now = datetime.now()
    year, month = now.year, now.month
    
    holidays = get_holidays(year)
    strategy = analyze_month(year, month, holidays)
    
    # 建立 Discord 訊息
    msg = [f"🚀 **{year}年{month}月 加班賺錢攻略**"]
    
    if not strategy["gold"]:
        # 這裡發送警告，但依然提供週六的建議
        msg.append("\n⚠️ **注意：本月系統未偵測到國定假日/補假！**")
        msg.append("> 請確認政府 API 網址是否異動，或本月確實無國定假日。")
    else:
        msg.append("\n💰 **【五星級金礦】(雙倍薪/不計上限)**")
        for item in strategy["gold"]:
            msg.append(f"• {item['date'].strftime('%m/%d')} ({item['name']}) - 報 8 小時")

    if strategy["silver"]:
        msg.append("\n🥈 **【每週精選】(本週六最划算)**")
        msg.append("這幾天建議挑一天報 10 小時：")
        for d in strategy["silver"]:
            # 如果這天剛好跟金礦重複了就不顯示
            if any(g['date'] == d for g in strategy['gold']): continue
            msg.append(f"• {d.strftime('%m/%d')} (週六休息日) - 報 10 小時")

    msg.append("\n💡 *其餘時數建議由平日加班補足至 46 小時。*")
    send_to_discord("\n".join(msg))

if __name__ == "__main__":
    main()