import requests
import re

def get_latest_json_url(target_year):
    catalog_url = "https://data.gov.tw/dataset/14718"
    print(f"🔎 [Step 1] 開始掃描政府資料集頁面: {catalog_url}")
    
    try:
        response = requests.get(catalog_url, timeout=10)
        html_content = response.text
        
        # 尋找所有符合條件的 JSON 下載連結
        pattern = r'https://quality\.data\.gov\.tw/dq_download_json\.php\?nid=14718&md5_url=[a-zA-Z0-9]+'
        all_links = re.findall(pattern, html_content)
        
        print(f"📊 [Step 1] 網頁內找到的 JSON 連結總數: {len(all_links)}")
        
        if all_links:
            # 這裡我們打印出第一個網址，看看是不是我們想要的
            target_url = all_links[0]
            print(f"✅ [Step 1] 選擇使用的網址: {target_url}")
            return target_url
            
        print("❌ [Step 1] 錯誤：網頁中找不到任何符合格式的 JSON 連結")
        return None
    except Exception as e:
        print(f"💥 [Step 1] 爬蟲發生異常: {str(e)}")
        return None

def get_holidays(year):
    url = get_latest_json_url(year)
    
    if not url:
        return {}
    
    print(f"🌐 [Step 2] 開始下載並解析 JSON 資料...")
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        print(f"📦 [Step 2] JSON 資料下載成功，共 {len(data)} 筆原始紀錄")
        
        holiday_info = {}
        found_current_year = False
        
        # 為了除錯，我們打印前 3 筆資料的 Key 看看
        if len(data) > 0:
            print(f"🔍 [Step 2] 資料欄位樣例: {list(data[0].keys())}")

        for item in data:
            date_str = item.get("Start Date")
            subject = item.get("Subject")
            
            if date_str and subject:
                # 處理日期格式 (支援 2026/4/3 或 2026/04/03)
                parts = date_str.split('/')
                
                # 有些 API 會回傳民國年，有些是西元年，我們做個相容性判斷
                raw_year = int(parts[0])
                actual_year = raw_year if raw_year > 1900 else raw_year + 1911
                
                if actual_year == year:
                    formatted_date = f"{actual_year}-{int(parts[1]):02d}-{int(parts[2]):02d}"
                    holiday_info[formatted_date] = subject
                    found_current_year = True
                    
        if not found_current_year:
            print(f"⚠️ [Step 2] 警告：抓到了資料，但裡面沒有包含 {year} 年的日期！")
        else:
            print(f"✨ [Step 2] 成功！已過濾出 {len(holiday_info)} 筆 {year} 年的節慶資料")
            
        return holiday_info if found_current_year else {}
    except Exception as e:
        print(f"💥 [Step 2] JSON 解析發生異常: {str(e)}")
        return {}