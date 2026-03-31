"""SQLite access layer for the COF intelligence MVP."""

from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List, Optional


class Database:
    """Small helper around sqlite3 for schema setup and persistence."""

    def __init__(self, db_path: str = "data/cof_intel.db") -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    @contextmanager
    def connect(self) -> Iterator[sqlite3.Connection]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def initialize(self, schema_path: str = "db/schema.sql") -> None:
        with open(schema_path, "r", encoding="utf-8") as schema_file:
            schema_sql = schema_file.read()
        with self.connect() as conn:
            conn.executescript(schema_sql)

    def insert_market_prices(self, rows: Iterable[Dict[str, Any]]) -> int:
        query = """
            INSERT OR IGNORE INTO market_prices (symbol, ts, open, high, low, close, volume, source)
            VALUES (:symbol, :ts, :open, :high, :low, :close, :volume, :source)
        """
        with self.connect() as conn:
            cur = conn.executemany(query, list(rows))
            return cur.rowcount

    def insert_event(self, event: Dict[str, Any]) -> int:
        query = """
            INSERT INTO events (
                symbol, event_ts, source_type, source_ref_id, category, importance,
                polarity, confidence, summary, key_metrics_json
            ) VALUES (
                :symbol, :event_ts, :source_type, :source_ref_id, :category, :importance,
                :polarity, :confidence, :summary, :key_metrics_json
            )
        """
        payload = {**event, "key_metrics_json": json.dumps(event.get("key_metrics", {}))}
        with self.connect() as conn:
            cur = conn.execute(query, payload)
            return int(cur.lastrowid)

    def insert_event_score(self, score: Dict[str, Any]) -> int:
        query = """
            INSERT INTO event_scores (event_id, score_ts, impact_score, decay_score, composite_score, model_version)
            VALUES (:event_id, :score_ts, :impact_score, :decay_score, :composite_score, :model_version)
        """
        with self.connect() as conn:
            cur = conn.execute(query, score)
            return int(cur.lastrowid)

    def insert_prediction(self, prediction: Dict[str, Any]) -> int:
        query = """
            INSERT INTO model_predictions (
                symbol, prediction_ts, horizon_days, prob_up, regime, model_version, feature_snapshot_json
            ) VALUES (
                :symbol, :prediction_ts, :horizon_days, :prob_up, :regime, :model_version, :feature_snapshot_json
            )
        """
        payload = {
            **prediction,
            "feature_snapshot_json": json.dumps(prediction.get("feature_snapshot", {})),
        }
        with self.connect() as conn:
            cur = conn.execute(query, payload)
            return int(cur.lastrowid)

    def fetch_recent_events(self, limit: int = 50) -> List[sqlite3.Row]:
        query = """
            SELECT e.*, s.composite_score
            FROM events e
            LEFT JOIN event_scores s ON s.event_id = e.id
            ORDER BY datetime(e.event_ts) DESC
            LIMIT ?
        """
        with self.connect() as conn:
            return list(conn.execute(query, (limit,)).fetchall())

    def fetch_latest_prices(self, symbols: Optional[List[str]] = None) -> List[sqlite3.Row]:
        filter_clause = ""
        params: List[Any] = []
        if symbols:
            placeholders = ",".join(["?"] * len(symbols))
            filter_clause = f"WHERE symbol IN ({placeholders})"
            params.extend(symbols)

        query = f"""
            SELECT mp.*
            FROM market_prices mp
            INNER JOIN (
                SELECT symbol, MAX(datetime(ts)) AS max_ts
                FROM market_prices
                {filter_clause}
                GROUP BY symbol
            ) latest
                ON latest.symbol = mp.symbol AND datetime(mp.ts) = latest.max_ts
            ORDER BY mp.symbol
        """
        with self.connect() as conn:
            return list(conn.execute(query, params).fetchall())

    def fetch_latest_predictions(self, symbol: str = "COF") -> List[sqlite3.Row]:
        query = """
            SELECT * FROM model_predictions
            WHERE symbol = ?
            ORDER BY datetime(prediction_ts) DESC
        """
        with self.connect() as conn:
            return list(conn.execute(query, (symbol,)).fetchall())
