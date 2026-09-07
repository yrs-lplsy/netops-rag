import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import yaml

from netrag.config import Settings
from netrag.ingestion.fetcher import fetch_all


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True)
    args = ap.parse_args()
    s = Settings.from_env()
    paths = fetch_all(Path(args.manifest), s.data_dir / "raw", s.data_dir / "processed")
    print(f"done: {len(paths)} docs")


if __name__ == "__main__":
    main()
