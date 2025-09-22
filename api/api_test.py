import requests
import sys
from config import get_symbol, get_log_files, get_report_file, log, clear_logs
from html_config import generate_report
# -------------------------------
# 設定
# -------------------------------

# 要測試的 Pokémon 名稱，可以是英文名稱，也可以是編號
pokemon_input = "25ˇˇˇ" 

# 測試網址
API_URL = f"https://pokeapi.co/api/v2/pokemon/{pokemon_input}"

# -------------------------------
# API 測試
# -------------------------------
def run_tests():
    log("開始 API 測試", info=True)

    try:
        response = requests.get(API_URL)
        response_time_ms = response.elapsed.total_seconds() * 1000
    except Exception as e:
        log(f"API 請求失敗: {e}", success=False)
        return

    # 1. HTTP status code
    log("開始測試: HTTP status code", info=True)
    status = response.status_code
    if status == 200:
        log(f"HTTP status code 驗證成功 (取得: {status})")
    else:
        log(f"HTTP status code 驗證失敗 (取得: {status})", success=False)

    # 2. Content-Type
    log("開始測試: Content-Type", info=True)
    content_type = response.headers.get("Content-Type", "")
    if status == 200 and content_type == "application/json; charset=utf-8":
        log(f"Content-Type 驗證成功 (取得: {content_type})")
    else:
        log(f"Content-Type 驗證失敗 (取得: {content_type})", success=False)

    # 3. 大小寫敏感
    log("開始測試: 大小寫敏感", info=True)
    try:
        case_test = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_input.capitalize()}")
        case_status = case_test.status_code
        if case_status == 200:
            log("大小寫敏感驗證成功")
        else:
            log(f"大小寫敏感驗證失敗 (取得: {case_status})", success=False)
    except Exception as e:
        log(f"大小寫敏感測試發生錯誤: {e}", success=False)

    # 4. JSON 內容驗證 確認是否包含 id, name, height, weight
    log("開始測試: JSON 欄位", info=True)
    data = None
    if status == 200:
        try:
            data = response.json()
            if all(k in data for k in ["id", "name", "height", "weight"]):
                log("JSON 欄位驗證成功")
            else:
                log("JSON 欄位驗證失敗", success=False)
        except Exception as e:
            log(f"JSON 解析失敗: {e}", success=False)
    else:
        log("跳過 JSON 驗證，因為 HTTP status != 200", info=True)

    # 5. id/name 欄位驗證

    # 根據輸入的 pokemon_input 是數字還是名稱來驗證
    # isdigit：檢查字串是否由數字組成，只對0跟正整數有效
    log("開始測試: ID/Name 欄位驗證", info=True)
    
    # 瞎傳參數導致json不存在的情況下
    if data is None:
        log("JSON 資料不存在，無法驗證 id/name 欄位", success=False)
        
    else:
        if pokemon_input.isdigit():
            # 如果輸入的是數字 → 用 ID 驗證
            # 確保兩邊格式一致，所以兩邊都int 再比較
            if int(data.get("id")) == int(pokemon_input):
                log(f'ID 驗證成功 (取得: {data.get("id")})')
            else:
                log(f'ID 驗證失敗 (取得: {data.get("id")})', success=False)
        else:
            # 如果輸入的是名稱 → 用 name 驗證
            if data.get("name") == pokemon_input:
                log(f'name 驗證成功 (取得: {data.get("name")})')
            else:
                log(f'name 欄位驗證失敗 (取得: {data.get("name")})', success=False)
                
    # 6. 發送非法參數
    log("開始測試: 非法參數", info=True)
    invalid_url = "https://pokeapi.co/api/v2/pokemon/invalid_name"
    try:
        invalid_response = requests.get(invalid_url)
        invalid_status = invalid_response.status_code
        if invalid_status == 404:
            log(f"非法參數 HTTP status code 驗證成功 (取得: {invalid_status})")
        else:
            log(f"非法參數 HTTP status code 驗證失敗 (取得: {invalid_status})", success=False)
    except Exception as e:
        log(f"請求非法參數發生錯誤: {e}", success=False)

    # 7. 回應時間驗證
    log("開始測試: Response time", info=True)
    if response_time_ms < 500:
        log(f"Response time 驗證成功 (取得: {response_time_ms:.2f} ms)")
    else:
        log(f"Response time 驗證失敗 (取得: {response_time_ms:.2f} ms)", success=False)

    log("API 測試完成", info=True)

# -------------------------------
# 主程式
# -------------------------------
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--clear":
        clear_logs()
    else:
        run_tests()
        generate_report("api_report.html")

