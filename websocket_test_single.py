import asyncio
import websockets
from datetime import datetime

WS_URL = "wss://ws.postman-echo.com/raw"  # echo server
# WS_URL = "wss://echo.websocket.org/" #不是單純的echo server

GREEN_CHECK = "\033[92m✅\033[0m"
RED_CROSS = "\033[91m❌\033[0m"

def log(message, success=True):
    symbol = GREEN_CHECK if success else RED_CROSS
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {symbol} {message}")

async def websocket_test():
    success_count = 0
    fail_count = 0

    try:
        async with websockets.connect(WS_URL) as ws:
            log("WebSocket 連線建立成功")
            success_count += 1

            # 單條訊息
            msg = "Hi Pikachu"
            try:
                await ws.send(msg)
                recv_msg = await ws.recv()
                if recv_msg == msg:
                    log(f'訊息回應正確: "{recv_msg}"')
                    success_count += 1
                else:
                    log(f'訊息回應錯誤: 發送 "{msg}", 收到 "{recv_msg}"', success=False)
                    fail_count += 1
            except Exception as e:
                log(f"單條訊息測試失敗: {e}", success=False)
                fail_count += 1
            
            # 等一下再發送多條訊息
            await asyncio.sleep(0.5)  # 等待 0.5 秒

            # 多條訊息
            messages = ["Message 1", "Message 2", "Message 3"]
            success_order = True
            try:
                for m in messages:
                    await ws.send(m)
                for expected in messages:
                    received = await ws.recv()
                    if received != expected:
                        log(f'訊息順序錯誤: 預期 "{expected}", 收到 "{received}"', success=False)
                        success_order = False
                        fail_count += 1
                if success_order:
                    log("多訊息順序驗證成功")
                    success_count += 1
            except Exception as e:
                log(f"多訊息順序測試失敗: {e}", success=False)
                fail_count += 1

            # 關閉連線
            try:
                await ws.close()
                if ws.close_code is not None:
                    log("WebSocket 連線成功關閉")
                    success_count += 1
                else:
                    log("WebSocket 關閉失敗", success=False)
                    fail_count += 1
            except Exception as e:
                log(f"關閉連線失敗: {e}", success=False)
                fail_count += 1

    except Exception as e:
        log(f"WebSocket 連線失敗: {e}", success=False)
        fail_count += 4

    # 測試總結
    log(f"測試完成 | 成功: {success_count}, 失敗: {fail_count}")

if __name__ == "__main__":
    asyncio.run(websocket_test())