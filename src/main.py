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
    
    if strategy["gold"]:
        msg.append("\n💰 **【五星級金礦】(雙倍薪/不計上限)**")
        for d in strategy["gold"]:
            msg.append(f"• {d.strftime('%m/%d')} - 建議報滿 8 小時")
            
    if strategy["silver"]:
        msg.append("\n🥈 **【優質礦脈】(休息日/高費率)**")
        # 取前三個週六
        for d in strategy["silver"][:3]:
            msg.append(f"• {d.strftime('%m/%d')} - 建議報 10 小時")
            
    msg.append("\n💡 *其餘時數建議由平日加班補足至 46 小時。*")
    msg.append(f"\n> 祝開發順利，ERP 手冊早日收工！")

    send_to_discord("\n".join(msg))

if __name__ == "__main__":
    main()