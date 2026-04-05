import requests

def get_holidays(year):
    # 這是你在截圖中看到的 JSON 下載網址（請替換成實際的 JSON 連結）
    url = "https://quality.data.gov.tw/dq_download_json.php?nid=14718&md5_url=713c14f57b1e04df52a67767628ba177" 
    
    try:
        response = requests.get(url)
        data = response.json()
        
        holiday_info = {} # 格式: {"2026-04-03": "補假"}
        
        for item in data:
            date_str = item.get("Start Date")
            subject = item.get("Subject")
            
            # 只有當日期和主題都有值時才處理
            if date_str and subject:
                # 處理斜線並統一格式為 2026-04-03
                parts = date_str.split('/')
                formatted_date = f"{parts[0]}-{int(parts[1]):02d}-{int(parts[2]):02d}"
                holiday_info[formatted_date] = subject
                
        return holiday_info
    except Exception as e:
        print(f"解析錯誤: {e}")
        return {}