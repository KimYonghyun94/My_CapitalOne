"""Market data collector for COF and SPY using yfinance."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict, List

import yfinance as yf


class MarketCollector:
    def __init__(self, symbols: List[str], period: str = "1d", interval: str = "1m") -> None:
        self.symbols = symbols
        self.period = period
        self.interval = interval

    def collect(self) -> List[Dict]:
        rows: List[Dict] = []
        for symbol in self.symbols:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=self.period, interval=self.interval)
            if hist.empty:
                continue

            for ts, record in hist.iterrows():
                rows.append(
                    {
                        "symbol": symbol,
                        "ts": ts.to_pydatetime().astimezone(timezone.utc).isoformat(),
                        "open": float(record.get("Open", 0.0)),
                        "high": float(record.get("High", 0.0)),
                        "low": float(record.get("Low", 0.0)),
                        "close": float(record.get("Close", 0.0)),
                        "volume": float(record.get("Volume", 0.0)),
                        "source": "yfinance",
                    }
                )
        return rows

    @staticmethod
    def build_market_event(symbol: str, close_price: float, ref_price: float, ts: str) -> Dict:
        move_pct = ((close_price - ref_price) / ref_price) * 100 if ref_price else 0
        trend_word = "up" if move_pct >= 0 else "down"
        summary = f"{symbol} moved {trend_word} {abs(move_pct):.2f}% vs benchmark reference"
        return {
            "symbol": symbol,
            "event_ts": ts,
            "source_type": "market",
            "source_ref_id": None,
            "summary": summary,
            "key_metrics": {"move_pct": move_pct, "close": close_price, "benchmark": ref_price},
        }
