import requests
from datetime import datetime

API_URL = "https://pokeapi.co/api/v2/pokemon/pikachu"

GREEN_CHECK = "\033[92m✅\033[0m"
RED_CROSS = "\033[91m❌\033[0m"

def log(message, success=True):
    symbol = GREEN_CHECK if success else RED_CROSS
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {symbol} {message}")

def run_tests():
    log("開始 API 測試")

    try:
        response = requests.get(API_URL)
    except Exception as e:
        log(f"API 請求失敗: {e}", success=False)
        return

    # 1. HTTP status code
    try:
        assert response.status_code == 200
        log("HTTP status code 驗證成功")
    except AssertionError:
        log(f"HTTP status code 驗證失敗 (取得: {response.status_code})", success=False)

    # 2. Content-Type 驗證
    try:
        assert response.headers.get("Content-Type") == "application/json; charset=utf-8"
        log("Content-Type 驗證成功")
    except AssertionError:
        log(f"Content-Type 驗證失敗 (取得: {response.headers.get('Content-Type')})", success=False)

    # 3. 大小寫敏感測試
    try:
        case_test = requests.get("https://pokeapi.co/api/v2/pokemon/Pikachu")
        assert case_test.status_code == 200
        log("大小寫敏感驗證成功")
    except AssertionError:
        log(f"大小寫敏感驗證失敗 (取得: {case_test.status_code})", success=False)

    # 4. JSON 內容驗證
    try:
        data = response.json()
        assert all(k in data for k in ["id", "name", "height", "weight"])
        log("JSON 欄位驗證成功")
    except AssertionError:
        log("JSON 欄位驗證失敗", success=False)

    # 5. name 欄位等於 "pikachu"
    try:
        assert data.get("name") == "pikachu"
        log('name="pikachu" 驗證成功')
    except AssertionError:
        log(f'name 欄位驗證失敗 (取得: {data.get("name")})', success=False)

    # 6. 發送非法參數
    try:
        invalid_response = requests.get("https://pokeapi.co/api/v2/pokemon/invalid_name")
        assert invalid_response.status_code == 404
        log("非法參數 HTTP status code 驗證成功")
    except AssertionError:
        log(f"非法參數 HTTP status code 驗證失敗 (取得: {invalid_response.status_code})", success=False)

    # 7. 驗證回應時間 < 500ms
    try:
        assert response.elapsed.total_seconds() < 0.5
        log("Response time 驗證成功")
    except AssertionError:
        log(f"Response time 驗證失敗 (取得: {response.elapsed.total_seconds()*1000:.2f} ms)", success=False)

    log("API 測試完成")

if __name__ == "__main__":
    run_tests()
