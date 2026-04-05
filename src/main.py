import os
import requests
from datetime import datetime
from holiday_api import get_holidays
from logic import analyze_month

# 你提供的預計單連結
OVERTIME_LINK = "https://workflow2.systex.com/wf_worklist/OvertimeExpect:edit:001.page?actionType=viewTemplate&pageStyle=popup&popupFrame=true&popupTargetName=_blank"

def send_to_discord(content):
    webhook_url = os.getenv('DISCORD_WEBHOOK')
    if not webhook_url:
        print("🚨 [Discord] 未設定 Webhook URL")
        return
    
    payload = {"content": content}
    requests.post(webhook_url, json=payload)

def main():
    print("--- 🏁 加班攻略系統啟動 ---")
    now = datetime.now()
    year, month, today_day = now.year, now.month, now.day
    
    holidays = get_holidays(year)
    strategy = analyze_month(year, month, holidays)
    
    # 建立一個「建議加班日」的清單，方便判斷今天
    gold_days = [item['date'].day for item in strategy["gold"]]
    silver_days = [d.day for d in strategy["silver"]]
    
    msg = []
    is_notification_day = False

    # 判斷 A：每月 1 號發送全月總結
    if today_day == 1:
        is_notification_day = True
        msg.append(f"📅 **{year}年{month}月 全月加班賺錢攻略已產生！**")
        msg.append("請查看本月金礦日與週六精選，提早規劃行程。")
    
    # 判斷 B：如果是金礦日或週六精選日，發送今日提醒
    elif today_day in gold_days or today_day in silver_days:
        is_notification_day = True
        msg.append("🔔 **【今日加班提醒】**")
        
        if today_day in gold_days:
            # 找到對應的節慶名稱
            holiday_name = next(item['name'] for item in strategy["gold"] if item['date'].day == today_day)
            msg.append(f"今天 {now.strftime('%m/%d')} 是 **{holiday_name}**，別忘了報滿 8 小時雙倍薪！")
        else:
            weekday_name = "週六" if now.weekday() == 5 else "週日"
            msg.append(f"今天 {now.strftime('%m/%d')} ({weekday_name}休息日) 建議報 10 小時，把額度花在刀口上！")
        
        msg.append(f"\n🔗 **點我快速填寫預計單：**\n{OVERTIME_LINK}")

    # 如果是通知日才發送
    if is_notification_day:
        # 如果是 1 號，我們還是把原本的全月清單附加上去
        if today_day == 1:
            msg.append("\n" + "="*20)
            if strategy["gold"]:
                msg.append("\n💰 **【五星級金礦】**")
                for item in strategy["gold"]:
                    msg.append(f"• {item['date'].strftime('%m/%d')} ({item['name']}) - 報 8 小時")

            if strategy["silver"]:
                msg.append("\n🥈 **【每週精選】**")
                for d in strategy["silver"]:
                    w_name = "週六" if d.weekday() == 5 else "週日"
                    msg.append(f"• {d.strftime('%m/%d')} ({w_name}休息日) - 報 10 小時")
            
            msg.append(f"\n🔗 **加班預計單：** {OVERTIME_LINK}")

        send_to_discord("\n".join(msg))
        print(f"🚀 訊息已於 {now.strftime('%H:%M')} 發送")
    else:
        print(f"😴 今天 ({now.strftime('%m/%d')}) 不是攻略日，跳過通知。")

if __name__ == "__main__":
    main()