import requests
import re

def get_latest_json_url():
    # 這是資料集的介紹頁面（固定不變）
    catalog_url = "https://data.gov.tw/dataset/14718"
    try:
        response = requests.get(catalog_url)
        # 使用正規表達式 (Regex) 尋找包含 nid=14718 且格式為 JSON 的下載連結
        # 匹配範例：https://quality.data.gov.tw/dq_download_json.php?nid=14718&md5_url=...
        pattern = r'https://quality\.data\.gov\.tw/dq_download_json\.php\?nid=14718&md5_url=[a-zA-Z0-9]+'
        match = re.search(pattern, response.text)
        
        if match:
            return match.group(0)
        else:
            # 如果沒抓到，回傳你目前已知的這個保底
            return ""
    except:
        return ""

def get_holidays(year):
    # 第一步：先去問現在最更新的網址是什麼
    url = get_latest_json_url()
    
    try:
        response = requests.get(url, timeout=10) # 加入 timeout 避免 GitHub Actions 卡死
        response.raise_for_status() # 如果 404 或 500 會直接跳到 except
        data = response.json()
        
        holiday_info = {}
        for item in data:
            date_str = item.get("Start Date")
            subject = item.get("Subject")
            if date_str and subject:
                # 轉換格式為 2026-04-03
                parts = date_str.split('/')
                formatted_date = f"{parts[0]}-{int(parts[1]):02d}-{int(parts[2]):02d}"
                holiday_info[formatted_date] = subject
        return holiday_info
    except Exception as e:
        print(f"CRITICAL ERROR: 無法獲取資料源 {e}")
        return {}