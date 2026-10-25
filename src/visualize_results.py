
import csv
from pathlib import Path
import matplotlib.pyplot as plt

PROJECT_DIR = Path(__file__).resolve().parent.parent
REPORT_FILE = PROJECT_DIR / "logs" / "detection_report.csv"

can_ids = []
message_counts = []
statuses = []

# Read the detection report
with open(REPORT_FILE, "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        can_ids.append(row["can_id"])
        message_counts.append(int(row["message_count"]))
        statuses.append(row["status"])

# Separate normal and suspicious messages
bar_colors = []

for status in statuses:
    if status == "SUSPICIOUS":
        bar_colors.append("red")
    else:
        bar_colors.append("green")

# Draw the graph
plt.figure(figsize=(8, 5))
plt.bar(can_ids, message_counts, color=bar_colors)

plt.title("CAN-Sentinel: Traffic Detection Results")
plt.xlabel("CAN ID")
plt.ylabel("Message Count")

plt.tight_layout()
plt.show()
