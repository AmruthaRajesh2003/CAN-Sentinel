
import csv
from collections import Counter, defaultdict
from pathlib import Path
from datetime import datetime

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_DIR / "data" / "can_data.csv"
LOG_DIR = PROJECT_DIR / "logs"
LOG_FILE = LOG_DIR / "alerts.log"
REPORT_FILE = LOG_DIR / "detection_report.csv"

ALLOWED_IDS = {"0x100", "0x200"}

# Educational test thresholds
MAX_MESSAGES = 4
TIME_WINDOW = 0.1
MAX_MESSAGES_IN_WINDOW = 4

LOG_DIR.mkdir(exist_ok=True)

# Read CAN messages
with open(DATA_FILE, "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    messages = list(reader)

required_columns = {"timestamp", "can_id", "data"}

if not messages or not required_columns.issubset(
    messages[0].keys()
):
    raise ValueError(
        "Invalid CSV file. Check the header: "
        "timestamp,can_id,data"
    )

# Group timestamps by CAN ID
timestamps_by_id = defaultdict(list)

for message in messages:
    can_id = message["can_id"].strip()
    timestamp = float(message["timestamp"])
    timestamps_by_id[can_id].append(timestamp)

id_counts = Counter(
    message["can_id"].strip() for message in messages
)

alerts = []
report_rows = []

print("=" * 45)
print("CAN-Sentinel: CAN Message Analysis")
print("=" * 45)

print("\nMessage Count Report:")

for can_id, count in sorted(id_counts.items()):
    print(f"CAN ID: {can_id} | Count: {count}")

print("\nTime-Based Frequency Analysis:")

for can_id, timestamps in sorted(timestamps_by_id.items()):
    timestamps.sort()
    max_in_window = 0

    # Count messages inside each time window
    for start_time in timestamps:
        window_count = sum(
            1 for timestamp in timestamps
            if start_time <= timestamp < start_time + TIME_WINDOW
        )
        max_in_window = max(max_in_window, window_count)

    print(
        f"CAN ID: {can_id} | "
        f"Maximum in {TIME_WINDOW} seconds: {max_in_window}"
    )

    unknown_id = can_id not in ALLOWED_IDS
    high_total_count = count > MAX_MESSAGES
    high_frequency = max_in_window > MAX_MESSAGES_IN_WINDOW

    if unknown_id:
        alerts.append(
            f"Unknown CAN ID detected: {can_id}"
        )

    if high_total_count:
        alerts.append(
            f"High total message count for {can_id}: {count}"
        )

    if high_frequency:
        alerts.append(
            f"High message frequency for {can_id}: "
            f"{max_in_window} messages in {TIME_WINDOW} seconds"
        )

    if unknown_id or high_total_count or high_frequency:
        status = "SUSPICIOUS"
    else:
        status = "NORMAL"

    report_rows.append({
        "can_id": can_id,
        "message_count": count,
        "max_messages_in_window": max_in_window,
        "unknown_id": unknown_id,
        "high_total_count": high_total_count,
        "high_frequency": high_frequency,
        "status": status
    })

# Save the latest CSV report
fieldnames = [
    "can_id",
    "message_count",
    "max_messages_in_window",
    "unknown_id",
    "high_total_count",
    "high_frequency",
    "status"
]

with open(REPORT_FILE, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(report_rows)

# Display alerts and save history
print("\nDetection Results:")

with open(LOG_FILE, "a", encoding="utf-8") as log:
    log.write(
        f"\nDetection run: "
        f"{datetime.now().isoformat(timespec='seconds')}\n"
    )

    if alerts:
        for alert in alerts:
            message = f"ALERT: {alert}"
            print(message)
            log.write(message + "\n")
    else:
        print("No suspicious patterns detected.")
        log.write("No suspicious patterns detected.\n")

print(f"\nAlerts saved to: {LOG_FILE}")
print(f"CSV report saved to: {REPORT_FILE}")
