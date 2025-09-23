import asyncio
import sys
import websockets
from datetime import datetime
from config import get_symbol, get_log_files, get_report_file, log, clear_logs
from html_config import generate_report

### 設定區 開始 ###
USE_SERVERS = [1, 2, 3]
MESSAGE_DELAY = 0.5
IGNORE_PATTERNS = ["Request served by"]
### 設定區 結束 ###

# WebSocket 伺服器設定
servers = {
    1: "wss://ws.postman-echo.com/raw",  # echo server
    2: "wss://echo.websocket.org/",      # 不是單純的 echo server
    3: "wss://wwww.123.123/",            # 故意錯誤的網址
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
    return url, success_count, fail_count


# 主流程：多網址並行測試
async def main():
    tasks = [websocket_test(servers[s]) for s in USE_SERVERS]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    print("\n=== 測試總結 ===")
    for res in results:
        if isinstance(res, tuple):
            url, success, fail = res
            print(f"{url} 成功: {success}, 失敗: {fail}")
        else:
            print(f"未知錯誤: {res}")
    return results


def run_tests():
    """封裝 async main()，方便呼叫"""
    return asyncio.run(main())


# -------------------------------
# 主程式
# -------------------------------
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--clear":
        clear_logs()
    else:
        run_tests()
        generate_report("api_report.html")
