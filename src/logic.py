from datetime import datetime

def analyze_month(year, month, holiday_info):
    import calendar
    cal = calendar.Calendar()
    days = cal.itermonthdates(year, month)
    
    strategy = {
        "gold": [],      # 國定假日 & 補假 (最划算)
        "silver": []     # 休息日推薦 (六日選一天)
    }

    # 記錄每一週哪天最划算
    weekly_best = {} # 格式: {week_number: {"date": date, "score": score}}

    for day in days:
        if day.month != month: continue
        
        date_key = day.strftime('%Y-%m-%d')
        weekday = day.weekday() # 0=Mon, 5=Sat, 6=Sun
        subject = holiday_info.get(date_key, "")
        week_num = day.isocalendar()[1]

        # 1. 判定【金礦】：只要 Subject 不是空字串且不是「例假日」
        # (補假、兒童節、清明節都屬於這類)
        if subject and subject != "例假日":
            strategy["gold"].append({"date": day, "name": subject})
            continue

        # 2. 判定【六日擇一】：
        # 我們優先推薦「週六 (休息日)」，因為週日在法律上是例假日，報加班程序較繁瑣。
        if weekday == 5: # 週六
            if week_num not in weekly_best:
                weekly_best[week_num] = day

    # 將每週選出的那一天放入 silver
    for d in weekly_best.values():
        strategy["silver"].append(d)
            
    return strategy