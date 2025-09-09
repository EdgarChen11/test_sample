#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

# 指定要清空的 log 檔案
LOG_FILES = [
    "websocket_test.log",
    "websocket_error.log"
]

def clear_log(file_path):
    if os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            pass  # "w" 模式會覆寫檔案內容，保留檔案但清空舊資料
        print(f"✅ 已清空檔案內容: {file_path}")
    else:
        print(f"⚠️ 檔案不存在: {file_path}")

if __name__ == "__main__":
    for log_file in LOG_FILES:
        clear_log(log_file)
