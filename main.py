"""Entry point for initializing and running the local pipeline."""

from __future__ import annotations

import argparse
import time

from config.settings import settings
from db.database import Database
from services.pipeline import CofPipeline


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="COF intelligence local pipeline")
    parser.add_argument("--run-once", action="store_true", help="Run one ingestion cycle")
    parser.add_argument("--interval-seconds", type=int, default=60, help="Loop interval in seconds")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    db = Database(settings.db_path)
    db.initialize()
    pipeline = CofPipeline(db)

    if args.run_once:
        print(pipeline.run_market_cycle())
        return

    while True:
        print(pipeline.run_market_cycle())
        time.sleep(args.interval_seconds)


if __name__ == "__main__":
    main()
