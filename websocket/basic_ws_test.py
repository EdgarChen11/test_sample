import asyncio
import websockets
from datetime import datetime

### 設定區 開始 ###

WS_URL = "wss://ws.postman-echo.com/raw"
MESSAGE_DELAY = 0.5  # 發送多條訊息時的延遲時間
IGNORE_PATTERNS = ["Request served by"]  # 忽略非測試訊息

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


# 過濾非測試訊息
async def recv_filtered(ws):
    while True:
        msg = await ws.recv()
        if any(msg.startswith(p) for p in IGNORE_PATTERNS):
            log(f'⚠️ 忽略非測試訊息: "{msg}"')
            continue
        return msg

# 單條訊息測試
async def single_message_test(ws):
    msg = "Hi Pikachu"
    await ws.send(msg)
    recv_msg = await recv_filtered(ws)
    if recv_msg == msg:
        log(f"單條訊息回應正確: '{recv_msg}'")
        return True
    else:
        log(f"單條訊息回應錯誤: 發送 '{msg}', 收到 '{recv_msg}'", success=False)
        return False

# 多條訊息順序測試
async def multi_message_test(ws):
    messages = ["Msg 1", "Msg 2", "Msg 3"]
    for m in messages:
        await ws.send(m)
    await asyncio.sleep(MESSAGE_DELAY)
    success = True
    for expected in messages:
        received = await recv_filtered(ws)
        if received != expected:
            log(f"訊息順序錯誤: 預期 '{expected}', 收到 '{received}'", success=False)
            success = False
    if success:
        log("多條訊息順序驗證成功")
    return success

# 訊息大小測試
async def large_message_test(ws):
    large_msg = "X" * 10000  # 10 KB 訊息
    await ws.send(large_msg)
    recv_msg = await recv_filtered(ws)
    if recv_msg == large_msg:
        log(f"訊息大小測試成功 (長度 {len(large_msg)})")
        return True
    else:
        log(f"訊息大小測試失敗", success=False)
        return False

# 主測試流程
async def main():
    success_count = 0
    fail_count = 0

    try:
        async with websockets.connect(WS_URL) as ws:
            log(f"WebSocket 連線建立成功: {WS_URL}")
            
            # 單條訊息測試
            if await single_message_test(ws):
                success_count += 1
            else:
                fail_count += 1

            # 多條訊息順序測試
            if await multi_message_test(ws):
                success_count += 1
            else:
                fail_count += 1

            # 訊息大小測試
            if await large_message_test(ws):
                success_count += 1
            else:
                fail_count += 1

            # 關閉連線
            await ws.close()
            log("WebSocket 連線成功關閉")

    except Exception as e:
        log(f"WebSocket 連線失敗: {e}", success=False)
        fail_count += 3  # 三個測試都沒跑

    # 測試總結
    log(f"測試完成 | 成功: {success_count}, 失敗: {fail_count}")

if __name__ == "__main__":
    asyncio.run(main())
