
import subprocess
import sys
import unittest
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_DIR / "data" / "can_data.csv"
DETECTOR_FILE = PROJECT_DIR / "src" / "detect_intrusion.py"


class TestCANDetection(unittest.TestCase):

    def setUp(self):
        # Keep a backup of the current dataset
        self.original_data = DATA_FILE.read_bytes()

    def tearDown(self):
        # Restore the original dataset after each test
        DATA_FILE.write_bytes(self.original_data)

    def run_detector(self, csv_data):
        # Create test data and run the detector
        DATA_FILE.write_text(csv_data, encoding="utf-8")

        result = subprocess.run(
            [sys.executable, str(DETECTOR_FILE)],
            cwd=PROJECT_DIR,
            capture_output=True,
            text=True
        )

        self.assertEqual(
            result.returncode,
            0,
            msg=result.stderr
        )

        return result.stdout

    def test_normal_traffic(self):
        data = (
            "timestamp,can_id,data\n"
            "0.01,0x100,01 02 03 04\n"
            "0.20,0x200,10 20 30 40\n"
        )

        output = self.run_detector(data)

        self.assertIn(
            "No suspicious patterns detected.",
            output
        )

    def test_unknown_can_id(self):
        data = (
            "timestamp,can_id,data\n"
            "0.01,0x666,FF FF FF FF\n"
        )

        output = self.run_detector(data)

        self.assertIn(
            "Unknown CAN ID detected: 0x666",
            output
        )

    def test_high_frequency(self):
        data = (
            "timestamp,can_id,data\n"
            "0.01,0x100,01 02 03 04\n"
            "0.02,0x100,01 02 03 04\n"
            "0.03,0x100,01 02 03 04\n"
            "0.04,0x100,01 02 03 04\n"
            "0.05,0x100,01 02 03 04\n"
        )

        output = self.run_detector(data)

        self.assertIn(
            "High message frequency for 0x100",
            output
        )

    def test_high_total_message_count(self):
        data = (
            "timestamp,can_id,data\n"
            "0.01,0x100,01 02 03 04\n"
            "0.20,0x100,01 02 03 04\n"
            "0.40,0x100,01 02 03 04\n"
            "0.60,0x100,01 02 03 04\n"
            "0.80,0x100,01 02 03 04\n"
        )

        output = self.run_detector(data)

        self.assertIn(
            "High total message count for 0x100: 5",
            output
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
