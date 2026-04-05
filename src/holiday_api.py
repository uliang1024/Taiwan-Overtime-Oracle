import requests
from datetime import datetime

def get_holidays(year):
    # 使用政府公開資料 API (人事行政總處)
    # 這裡預設回傳一個包含國定假日的 list
    url = f"https://openapi.dgpa.gov.tw/api/v1/data/f093547b-88fb-4ae2-ad21-95f3134f043b/json"
    try:
        response = requests.get(url)
        data = response.json()
        # 過濾出「放假」且「不是週六日」的補假，或是標註為國定假日的天數
        holidays = [item['date'] for item in data if item['isHoliday'] == '是']
        return holidays
    except:
        # 如果 API 壞了，回傳空清單避免程式崩潰
        return []