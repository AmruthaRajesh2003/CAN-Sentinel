
import csv
from pathlib import Path

# Project folder location
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

file_path = DATA_DIR / "can_data.csv"

messages = [
    ["0.01", "0x100", "01 02 03 04"],
    ["0.02", "0x200", "10 20 30 40"],
    ["0.03", "0x100", "01 02 03 04"],
    ["0.04", "0x200", "10 20 30 40"],
    ["0.05", "0x100", "01 02 03 04"],
    ["0.06", "0x666", "FF FF FF FF"],
    ["0.07", "0x666", "FF FF FF FF"],
    ["0.08", "0x666", "FF FF FF FF"],
    ["0.09", "0x666", "FF FF FF FF"],
    ["0.10", "0x666", "FF FF FF FF"],
    ["0.11", "0x666", "FF FF FF FF"],
]

with open(file_path, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["timestamp", "can_id", "data"])
    writer.writerows(messages)

print("Sample CAN dataset created successfully!")
print(f"File location: {file_path}")
