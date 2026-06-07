import os
import requests
import time
from datetime import datetime

CHART_NAME = os.getenv("HELM_CHART_NAME", "my-fastapi-app")
LOKI_BASE_URL = os.getenv("LOKI_URL", "http://localhost:3100")
LOKI_URL = f"{LOKI_BASE_URL}/loki/api/v1/query_range"
QUERY = os.getenv("LOKI_QUERY", '{pod=~"fastapi.*"}')
LOG_FILE = os.getenv("LOG_FILE", "warning_error_logs.txt")

seen_logs = set()

def fetch_latest_logs():
    params = {
        "query": QUERY,
        "limit": 5,
        "direction": "backward"
    }
    response = requests.get(LOKI_URL, params=params)
    response.raise_for_status()
    data = response.json()
    logs = []
    for stream in data["data"]["result"]:
        for timestamp, log_line in stream["values"]:
            logs.append(log_line)
    return logs[:5]

def save_if_warning_or_error(logs):
    global seen_logs
    with open(LOG_FILE, "a") as file:
        for log in logs:
            lower_log = log.lower()
            if ("warning" in lower_log or "error" in lower_log) and log not in seen_logs:
                seen_logs.add(log)
                file.write(f"\n[{datetime.now()}] {log}\n")
                print("Saved warning/error:", log)

while True:
    try:
        latest_logs = fetch_latest_logs()
        print("\nLatest 5 logs:")
        for log in latest_logs:
            print(log)
        save_if_warning_or_error(latest_logs)
    except Exception as e:
        print("Error while fetching logs:", e)
    time.sleep(5)
