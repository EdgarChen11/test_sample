import os

LOG_FILE = "log/api_test.log"
ERROR_LOG_FILE = "log/api_error.log"

def clear_logs():
    for f in [LOG_FILE, ERROR_LOG_FILE]:
        if os.path.exists(f):
            open(f, "w", encoding="utf-8").close()
            print(f"已清除 {f}")
        else:
            print(f"{f} 不存在，略過")

if __name__ == "__main__":
    clear_logs()
