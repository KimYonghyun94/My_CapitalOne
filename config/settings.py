"""App configuration."""

from dataclasses import dataclass
import os


@dataclass
class Settings:
    db_path: str = os.getenv("COF_DB_PATH", "data/cof_intel.db")
    market_symbols: tuple[str, ...] = ("COF", "SPY")
    market_period: str = os.getenv("COF_MARKET_PERIOD", "1d")
    market_interval: str = os.getenv("COF_MARKET_INTERVAL", "1m")


settings = Settings()
