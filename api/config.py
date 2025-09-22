from datetime import datetime
import os

# -------------------------------
# 彩色符號
# -------------------------------
def get_symbol(status):
    if status == "pass":
        return "\033[92m✅\033[0m"
    elif status == "fail":
        return "\033[91m❌\033[0m"
    elif status == "info":
        return "\033[94mℹ️\033[0m"
    else:
        return ""

# -------------------------------
# Log 檔案，指定路徑
# -------------------------------
def get_log_files():
    log_dir = "test_sample/api/log"
    os.makedirs(log_dir, exist_ok=True)  # 確保資料夾存在
    return {
        "log": os.path.join(log_dir, "api_test.log"),
        "error": os.path.join(log_dir, "api_error.log")
    }

# -------------------------------
# Report 檔案，指定路徑
# -------------------------------
def get_report_file(name="report.html"):
    report_dir = "test_sample/api/report"
    os.makedirs(report_dir, exist_ok=True)
    return os.path.join(report_dir, name)

# -------------------------------
# Log 功能
# -------------------------------
def log(message, success=True, info=False):
    files = get_log_files()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if info:
        symbol = get_symbol("info")
        plain_symbol = "[INFO]"
    else:
        symbol = get_symbol("pass") if success else get_symbol("fail")
        plain_symbol = "[PASS]" if success else "[FAIL]"

    console_msg = f"{timestamp} - {symbol} {message}"
    file_msg = f"{timestamp} - {plain_symbol} {message}"

    print(console_msg)
    with open(files["log"], "a", encoding="utf-8") as f:
        f.write(file_msg + "\n")

    if not success:
        with open(files["error"], "a", encoding="utf-8") as f:
            f.write(file_msg + "\n")

# -------------------------------
# 清除 log
# -------------------------------
def clear_logs():
    files = get_log_files()
    for f in files.values():
        if os.path.exists(f):
            open(f, "w", encoding="utf-8").close()
            print(f"已清除 {f}")
        else:
            print(f"{f} 不存在，略過")


