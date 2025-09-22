import os
from config import get_log_files

# -------------------------------
# 產生 HTML 報表
# -------------------------------
def generate_report(report_name="api_report.html"):
    report_dir = "test_sample/api/report"
    os.makedirs(report_dir, exist_ok=True)  # 確保資料夾存在
    report_path = os.path.join(report_dir, report_name)

    log_files = get_log_files()  # 取得字典
    log_path = log_files["log"]  # 取得 log 檔案路徑

    if not os.path.exists(log_path):
        print("沒有找到 log 檔案，無法產生報告")
        return

    # 讀取 log
    with open(log_path, encoding="utf-8") as f:
        lines = f.readlines()

    # HTML 樣板
    html = """<html>
<head>
    <meta charset="utf-8">
    <title>API 測試報告</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; background: #f9f9f9; }
        h1 { color: #333; }
        .pass { color: green; }
        .fail { color: red; }
        .info { color: blue; }
        pre { background: #fff; padding: 10px; border: 1px solid #ccc; margin: 0; white-space: pre-wrap; }
    </style>
</head>
<body>
    <h1>API 測試報告</h1>
    <pre>"""  # <- 這裡不要換行或縮排

    # 生成 log 內容
    for line in lines:
        text = line.strip()
        if "[PASS]" in text:
            html += f"<span class='pass'>{text}</span><br>"
        elif "[FAIL]" in text:
            html += f"<span class='fail'>{text}</span><br>"
        elif "[INFO]" in text:
            html += f"<span class='info'>{text}</span><br>"
        else:
            html += text + "<br>"

    html += """</pre>
</body>
</html>"""

    # 寫入 HTML 檔案
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ 已產生報告：{report_path}")
