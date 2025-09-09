# WebSocket 測試檔案說明

## 📌 檔案列表
| 檔名 | 用途 |
|------|------|
| `websocket_test.py` | 執行 WebSocket 測試（單條訊息、多條訊息順序、大訊息測試） |
| `clear_logs.py` | 清除 `websocket_test.log` 與 `websocket_error.log` 內容 |

---

## 🚀 測試項目
1. **單條訊息回應測試**  
   發送一條訊息，檢查伺服器回應是否正確。
2. **多條訊息順序測試**  
   發送多條訊息，檢查伺服器是否按順序回傳。
3. **訊息大小測試**  
   發送大資料量訊息（例如 10KB），檢查伺服器是否正確處理。

---

## 📄 Log 檔案說明
- **`websocket_test.log`**  
  記錄所有測試結果（成功與失敗）。
- **`websocket_error.log`**  
  只記錄失敗的測試結果，方便快速排錯。

---

## 🖥 執行方法
```bash
python websocket_test.py
```

---

## 🧹 清除檔案方法
```bash
python clear_logs.py
```

執行後會清空：
websocket_test.log
websocket_error.log

---

## ⚙️ 參數設定
```python
WS_URL = "wss://ws.postman-echo.com/raw"  # 測試 WebSocket 伺服器網址
MESSAGE_DELAY = 0.5                       # 多訊息測試的延遲時間
IGNORE_PATTERNS = ["Request served by"]   # 過濾非測試訊息
```

---
## 📌 注意事項
測試需要網路連線，若伺服器無回應會直接記錄為失敗。
若要測試多個伺服器，可以改寫成伺服器清單批次執行。

---
