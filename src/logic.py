from datetime import datetime

def analyze_month(year, month, holiday_info):
    import calendar
    cal = calendar.Calendar()
    days = cal.itermonthdates(year, month)
    
    strategy = {
        "gold": [],
        "silver": []
    }

    weekly_best = {}

    for day in days:
        if day.month != month: continue
        
        date_key = day.strftime('%Y-%m-%d')
        weekday = day.weekday() # 5=Sat, 6=Sun
        subject = holiday_info.get(date_key, "")
        week_num = day.isocalendar()[1]

        if subject and subject != "例假日":
            strategy["gold"].append({"date": day, "name": subject})
            continue

        # 目前邏輯依然優先推週六，若要改週日可改為 weekday == 6
        if weekday == 5: 
            if week_num not in weekly_best:
                weekly_best[week_num] = day

    for d in weekly_best.values():
        strategy["silver"].append(d)
            
    return strategy