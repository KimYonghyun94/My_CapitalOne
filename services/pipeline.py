"""Ingestion pipeline for market data -> events -> scores -> predictions."""

from __future__ import annotations

from datetime import datetime, timezone
from statistics import mean
from typing import Dict, List

from collectors.market_collector import MarketCollector
from config.settings import settings
from db.database import Database
from models.direction_model import compute_direction_probabilities
from processors.event_classifier import classify_event
from processors.scoring_engine import score_event


class CofPipeline:
    def __init__(self, db: Database) -> None:
        self.db = db
        self.collector = MarketCollector(
            symbols=list(settings.market_symbols),
            period=settings.market_period,
            interval=settings.market_interval,
        )

    def run_market_cycle(self) -> Dict:
        prices = self.collector.collect()
        if not prices:
            return {"status": "no_data", "rows_inserted": 0}

        rows_inserted = self.db.insert_market_prices(prices)

        latest_by_symbol: Dict[str, Dict] = {}
        for row in prices:
            latest_by_symbol[row["symbol"]] = row

        cof = latest_by_symbol.get("COF")
        spy = latest_by_symbol.get("SPY")
        if not cof or not spy:
            return {"status": "partial", "rows_inserted": rows_inserted}

        event = self.collector.build_market_event(
            symbol="COF",
            close_price=cof["close"],
            ref_price=spy["close"],
            ts=datetime.now(timezone.utc).isoformat(),
        )
        event.update(classify_event(event["summary"]))
        event_id = self.db.insert_event(event)

        score_payload = score_event({**event, "event_id": event_id})
        self.db.insert_event_score(score_payload)

        prediction_payload = self._build_prediction_payload(cof["close"], spy["close"])
        for horizon in prediction_payload["horizons"]:
            self.db.insert_prediction(
                {
                    "symbol": "COF",
                    "prediction_ts": prediction_payload["prediction_ts"],
                    "horizon_days": horizon["horizon_days"],
                    "prob_up": horizon["prob_up"],
                    "regime": prediction_payload["regime"],
                    "model_version": prediction_payload["model_version"],
                    "feature_snapshot": {
                        "cof_close": cof["close"],
                        "spy_close": spy["close"],
                        "latest_composite_score": score_payload["composite_score"],
                    },
                }
            )

        return {"status": "ok", "rows_inserted": rows_inserted, "event_id": event_id}

    def _build_prediction_payload(self, cof_close: float, spy_close: float) -> Dict:
        recent_events = self.db.fetch_recent_events(limit=20)
        scores = [float(row["composite_score"]) for row in recent_events if row["composite_score"] is not None]
        avg_event_score = mean(scores) if scores else 50.0
        return compute_direction_probabilities(cof_close, spy_close, avg_event_score)
