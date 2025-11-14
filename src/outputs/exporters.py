thonpython
import json
import csv
import logging
from pathlib import Path

class Exporter:

    @staticmethod
    def to_json(data, filepath: Path):
        try:
            with open(filepath, "w") as f:
                json.dump(data, f, indent=4)
            logging.info(f"JSON exported: {filepath}")
        except Exception as e:
            logging.error(f"Failed to export JSON: {e}")

    @staticmethod
    def to_csv(data, filepath: Path):
        try:
            if not data:
                logging.warning("No data to export.")
                return

            with open(filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)

            logging.info(f"CSV exported: {filepath}")
        except Exception as e:
            logging.error(f"Failed to export CSV: {e}")