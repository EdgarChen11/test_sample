import asyncio
import websockets
from datetime import datetime

### 設定區 開始 ###

USE_SERVERS = [1, 2, 3]
MESSAGE_DELAY = 0.5
IGNORE_PATTERNS = ["Request served by"]

# ANSI 顏色控制碼
GREEN_CHECK = "\033[92m✅\033[0m"
RED_CROSS = "\033[91m❌\033[0m"

### 設定區 結束 ###


# log 函式（同時寫入測試與錯誤 log）
def log(message, success=True):
    symbol = GREEN_CHECK if success else RED_CROSS
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_message = f"{timestamp} - {symbol} {message}"

    # 終端機輸出
    print(log_message)

    # 所有測試結果
    with open("websocket_test.log", "a", encoding="utf-8") as f:
        f.write(log_message + "\n")

    # 失敗記到 error log
    if not success:
        with open("websocket_error.log", "a", encoding="utf-8") as f:
            f.write(log_message + "\n")

# WebSocket 伺服器設定
servers = {
    1: "wss://ws.postman-echo.com/raw", # echo server
    2: "wss://echo.websocket.org/", #不是單純的echo server，會回一個東西
    3: "wss://wwww.123.123/",  # 故意錯誤的網址
}



async def recv_filtered(ws):
    while True:
        msg = await ws.recv()
        if any(msg.startswith(p) for p in IGNORE_PATTERNS):
            log(f'⚠️ 忽略非測試訊息: "{msg}"')
            continue
        return msg

async def websocket_test(url):
    success_count = 0
    fail_count = 0
    try:
        async with websockets.connect(url) as ws:
            log(f"WebSocket 連線建立成功: {url}")
            success_count += 1

            # 單條訊息
            msg = "Hi Pikachu"
            try:
                await ws.send(msg)
                recv_msg = await recv_filtered(ws)
                if recv_msg == msg:
                    log(f'訊息回應正確: "{recv_msg}" ({url})')
                    success_count += 1
                else:
                    log(f'訊息回應錯誤: 發送 "{msg}", 收到 "{recv_msg}" ({url})', success=False)
                    fail_count += 1
            except Exception as e:
                log(f"單條訊息測試失敗 ({url}): {e}", success=False)
                fail_count += 1

            # 多條訊息
            await asyncio.sleep(MESSAGE_DELAY)
            messages = ["Message 1", "Message 2", "Message 3"]
            success_order = True
            try:
                for m in messages:
                    await ws.send(m)
                for expected in messages:
                    received = await recv_filtered(ws)
                    if received != expected:
                        log(f'訊息順序錯誤: 預期 "{expected}", 收到 "{received}" ({url})', success=False)
                        success_order = False
                        fail_count += 1
                if success_order:
                    log(f"多訊息順序驗證成功 ({url})")
                    success_count += 1
            except Exception as e:
                log(f"多訊息順序測試失敗 ({url}): {e}", success=False)
                fail_count += 1

            # 關閉連線
            try:
                await ws.close()
                log(f"WebSocket 連線成功關閉 ({url})")
                success_count += 1
            except Exception as e:
                log(f"關閉連線失敗 ({url}): {e}", success=False)
                fail_count += 1

    except Exception as e:
        log(f"WebSocket 連線失敗 ({url}): {e}", success=False)
        fail_count += 4

    log(f"測試完成 ({url}) | 成功: {success_count}, 失敗: {fail_count}")
    return url, success_count, fail_count  # 回傳統計結果

# 主流程：多網址並行測試
async def main():
    tasks = [websocket_test(servers[s]) for s in USE_SERVERS]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # 印出總結
    print("\n=== 測試總結 ===")
    for res in results:
        if isinstance(res, tuple):
            url, success, fail = res
            print(f"{url} 成功: {success}, 失敗: {fail}")
        else:
            # 如果發生未捕捉的例外
            print(f"未知錯誤: {res}")

if __name__ == "__main__":
    asyncio.run(main())

