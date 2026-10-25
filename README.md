
# CAN-Sentinel: Automotive ECU Intrusion Detection System

## Project Overview

CAN-Sentinel is an educational cybersecurity project that analyzes simulated Controller Area Network (CAN) messages to identify potentially suspicious traffic patterns.

The project uses Python to process CAN message data, apply simple detection rules, generate alerts, and create visual reports.

## Objectives

- Analyze simulated CAN traffic.
- Identify unknown CAN IDs.
- Detect high total message counts.
- Detect unusually high message frequency.
- Generate detection reports.
- Record alerts in a log file.
- Visualize CAN message counts using graphs.
- Test detection rules using automated tests.

## Technologies Used

- Python
- CSV
- Matplotlib
- Python unittest
- Git and GitHub

## Project Structure

```text
CAN-Sentinel/
├── data/
│   └── can_data.csv
├── src/
│   ├── main.py
│   ├── generate_data.py
│   ├── detect_intrusion.py
│   ├── test_detection.py
│   └── visualize_results.py
├── logs/
│   ├── alerts.log
│   └── detection_report.csv
├── .gitignore
└── README.md
```

## Features

### CAN Message Analysis
Reads CAN messages from a CSV dataset and analyzes their CAN IDs and timestamps.

### Unknown CAN ID Detection
Flags CAN IDs that are not included in the configured allowed-ID list.

### Message Count Detection
Identifies CAN IDs whose total message count exceeds the configured threshold.

### Frequency-Based Detection
Checks whether too many messages occur within a configured time window.

### Detection Reports
Saves analysis results to `logs/detection_report.csv`.

### Alert Logging
Records detection alerts in `logs/alerts.log`.

### Traffic Visualization
Uses Matplotlib to display CAN message counts in a bar chart. Suspicious IDs are displayed in red and normal IDs in green.

### Automated Testing
Uses Python's unittest framework to test normal traffic, unknown IDs, high-frequency traffic, and high total message counts.

## Requirements

- Python installed on your computer
- Matplotlib installed for graph visualization

Install Matplotlib if it is not already installed:

```bash
python -m pip install matplotlib
```

## How to Run the Project

Run these commands from the main `CAN-Sentinel` project folder.

### 1. Generate Sample Data (Optional)

```bash
python src/generate_data.py
```

This creates the sample CAN dataset.

**Warning:** Running this script replaces the existing `data/can_data.csv` file with the built-in sample data.

### 2. Run Intrusion Detection

```bash
python src/detect_intrusion.py
```

This analyzes the dataset and generates detection results, alerts, and a CSV report.

### 3. Visualize Results

```bash
python src/visualize_results.py
```

This opens a graph showing the message counts for each CAN ID.

### 4. Run Automated Tests

```bash
python -m unittest src.test_detection -v
```

The tests check whether the configured detection rules work with the supplied test cases.

## Detection Rules

The current detector uses configurable rules, including:

- Allowed CAN IDs
- Maximum total message count
- Time window for frequency analysis
- Maximum messages allowed within that window

The actual values are defined in `src/detect_intrusion.py`.

## Limitations

- The project uses simulated CAN data.
- Detection is based on simple predefined rules.
- Unknown or high-frequency traffic is considered suspicious according to the configured rules; this does not prove an actual cyberattack.
- The system has not been validated for real vehicle networks.
- Real-world deployment would require representative data, validated thresholds, and additional safety and security testing.

## Disclaimer

CAN-Sentinel is intended for educational cybersecurity learning and experimentation. It is not a certified automotive security system and must not be used as a replacement for validated vehicle safety or security mechanisms.
