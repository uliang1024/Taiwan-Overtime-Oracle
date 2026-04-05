import requests
import re

def get_latest_json_url(target_year):
    catalog_url = "https://data.gov.tw/dataset/14718"
    print(f"🔎 [Step 1] 開始掃描政府資料集頁面: {catalog_url}")
    
    try:
        response = requests.get(catalog_url, timeout=10)
        html_content = response.text
        
        pattern = r'https://quality\.data\.gov\.tw/dq_download_json\.php\?nid=14718&md5_url=[a-zA-Z0-9]+'
        all_links = re.findall(pattern, html_content)
        
        print(f"📊 [Step 1] 網頁內找到的 JSON 連結總數: {len(all_links)}")
        
        if all_links:
            # 改為取最後一個 [-1]，通常是網頁上最新更新的年度
            target_url = all_links[-1]
            print(f"✅ [Step 1] 選擇使用最後一個網址 (最新年度): {target_url}")
            return target_url
            
        print("❌ [Step 1] 錯誤：網頁中找不到任何符合格式的 JSON 連結")
        return None
    except Exception as e:
        print(f"💥 [Step 1] 爬蟲發生異常: {str(e)}")
        return None

def get_holidays(year):
    url = get_latest_json_url(year)
    if not url: return {}
    
    print(f"🌐 [Step 2] 開始下載並解析 JSON 資料...")
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        print(f"📦 [Step 2] JSON 下載成功，共 {len(data)} 筆原始紀錄")
        
        holiday_info = {}
        found_current_year = False

        for item in data:
            # 動態偵測日期欄位 (相容 Start Date 或 西元日期)
            date_str = item.get("Start Date") or item.get("西元日期")
            # 動態偵測內容欄位 (相容 Subject 或 備註)
            subject = item.get("Subject") or item.get("備註")
            # 動態偵測是否放假 (有些格式會寫在 '是否放假')
            is_holiday = item.get("是否放假")
            
            if date_str:
                # 處理日期分隔符號 (可能為 / 或 -)
                date_val = date_str.replace('/', '-')
                parts = date_val.split('-')
                
                raw_year = int(parts[0])
                actual_year = raw_year if raw_year > 1900 else raw_year + 1911
                
                if actual_year == year:
                    # 如果備註是空的，但標註為「是」放假，則補上一個名稱
                    if not subject and is_holiday == "是":
                        subject = "國定假日"
                    
                    if subject and subject != "例假日":
                        formatted_date = f"{actual_year}-{int(parts[1]):02d}-{int(parts[2]):02d}"
                        holiday_info[formatted_date] = subject
                        found_current_year = True
                    
        if not found_current_year:
            print(f"⚠️ [Step 2] 警告：抓到的資料中仍未包含 {year} 年！")
        else:
            print(f"✨ [Step 2] 成功！已過濾出 {len(holiday_info)} 筆 {year} 年的節慶資料")
            
        return holiday_info
    except Exception as e:
        print(f"💥 [Step 2] JSON 解析發生異常: {str(e)}")
        return {}