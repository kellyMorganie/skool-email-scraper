thonpython
import json
import logging
from pathlib import Path

from extractors.skool_parser import SkoolParser
from outputs.exporters import Exporter
from config.settings import load_settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def main():
    base_path = Path(__file__).resolve().parent.parent
    settings = load_settings(base_path / "src" / "config" / "settings.example.json")

    input_file = base_path / "data" / "inputs.sample.json"
    if not input_file.exists():
        logging.error(f"Input file not found: {input_file}")
        return

    with open(input_file, "r") as f:
        tasks = json.load(f)

    parser = SkoolParser(
        proxies=settings.get("proxies"),
        domains=settings.get("allowed_domains", [])
    )

    all_results = []

    for task in tasks:
        keyword = task.get("keyword")
        location = task.get("location")
        logging.info(f"Scraping keyword='{keyword}' location='{location}'")

        results = parser.search(keyword=keyword, location=location)
        all_results.extend(results)

    output_path = base_path / "data" / "sample-output.json"
    Exporter.to_json(all_results, output_path)

    logging.info(f"Scraping complete. Saved {len(all_results)} results to {output_path}")

if __name__ == "__main__":
    main()