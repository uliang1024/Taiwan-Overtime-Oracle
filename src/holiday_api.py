import requests
import re

def get_latest_json_url(target_year):
    # 轉換成民國年，因為政府標題常用民國年 (例如 2026 -> 115)
    roc_year = target_year - 1911
    catalog_url = "https://data.gov.tw/dataset/14718"
    
    try:
        response = requests.get(catalog_url, timeout=10)
        html_content = response.text
        
        # 1. 先把網頁中所有包含 nid=14718 的 JSON 連結找出來
        # 格式通常是: ...dq_download_json.php?nid=14718&md5_url=XXXX
        pattern = r'https://quality\.data\.gov\.tw/dq_download_json\.php\?nid=14718&md5_url=[a-zA-Z0-9]+'
        all_links = re.findall(pattern, html_content)
        
        # 2. 這是關鍵：我們尋找包含「115年」或「2026年」字眼附近的連結
        # 實務上，最新的連結通常會排在 HTML 的前面
        # 我們直接取第一個，通常就是最新年度
        if all_links:
            # 這裡可以加一個簡單的邏輯：如果有多個，優先回傳第一個
            # 或者你可以根據 index 尋找 HTML 裡靠近 "115年" 字樣的連結
            return all_links[0] 
            
        return None
    except Exception as e:
        print(f"爬蟲抓取失敗: {e}")
        return None

def get_holidays(year):
    url = get_latest_json_url(year)
    
    if not url:
        return {} # 沒抓到網址就回傳空，觸發 main.py 的警告
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        holiday_info = {}
        found_current_year = False
        
        for item in data:
            date_str = item.get("Start Date")
            subject = item.get("Subject")
            if date_str and subject:
                parts = date_str.split('/')
                # 確認資料年份是否正確
                if int(parts[0]) == year:
                    formatted_date = f"{parts[0]}-{int(parts[1]):02d}-{int(parts[2]):02d}"
                    holiday_info[formatted_date] = subject
                    found_current_year = True
                    
        return holiday_info if found_current_year else {}
    except:
        return {}