import requests
from datetime import datetime
import os
import sys

# -------------------------------
# 設定
# -------------------------------

# 要測試的 Pokémon 名稱，可以是英文名稱，也可以是編號
pokemon_name = "pikachu" 

# 測試網址
API_URL = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"

# 彩色符號
GREEN_CHECK = "\033[92m✅\033[0m"
RED_CROSS = "\033[91m❌\033[0m"
INFO = "\033[94mℹ️\033[0m"

# Log 檔案
LOG_FILE = "api_test.log"
ERROR_LOG_FILE = "api_error.log"

# -------------------------------
# Log 功能
# -------------------------------
def log(message, success=True, info=False):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if info:
        symbol = INFO
        plain_symbol = "[INFO]"
    else:
        symbol = GREEN_CHECK if success else RED_CROSS
        plain_symbol = "[PASS]" if success else "[FAIL]"

    console_msg = f"{timestamp} - {symbol} {message}"
    file_msg = f"{timestamp} - {plain_symbol} {message}"

    print(console_msg)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(file_msg + "\n")

    if not success:
        with open(ERROR_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(file_msg + "\n")

# -------------------------------
# 清除 log
# -------------------------------
def clear_logs():
    for f in [LOG_FILE, ERROR_LOG_FILE]:
        if os.path.exists(f):
            open(f, "w", encoding="utf-8").close()
            print(f"已清除 {f}")
        else:
            print(f"{f} 不存在，略過")

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
        case_test = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.capitalize()}")
        case_status = case_test.status_code
        if case_status == 200:
            log("大小寫敏感驗證成功")
        else:
            log(f"大小寫敏感驗證失敗 (取得: {case_status})", success=False)
    except Exception as e:
        log(f"大小寫敏感測試發生錯誤: {e}", success=False)

    # 4. JSON 內容驗證
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

    # 5. name 欄位驗證
    log("開始測試: name 欄位", info=True)
    if data:
        if data.get("name") == pokemon_name:
            log(f'name="{pokemon_name}" 驗證成功')
        else:
            log(f'name 欄位驗證失敗 (取得: {data.get("name")})', success=False)
    else:
        log("跳過 name 欄位驗證，data 為 None", info=True)

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
