from datetime import datetime

def analyze_month(year, month, holiday_list):
    import calendar
    cal = calendar.Calendar()
    days = cal.itermonthdates(year, month)
    
    strategy = {
        "gold": [],      # 國定假日 (雙倍薪，不佔 46hr)
        "silver": [],    # 休息日 (週六，高加成，佔額度)
        "regular": []    # 平日 (一般加成，佔額度)
    }

    for day in days:
        if day.month != month: continue
        
        date_str = day.strftime('%Y%m%d')
        weekday = day.weekday() # 0=Mon, 5=Sat, 6=Sun

        # 判斷邏輯
        if date_str in holiday_list:
            strategy["gold"].append(day)
        elif weekday == 5: # 週六 (休息日)
            strategy["silver"].append(day)
        elif weekday < 5:  # 平日
            strategy["regular"].append(day)
            
    return strategy