"""Baseline event scoring engine."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict


MODEL_VERSION = "rule-score-v1"


def score_event(event: Dict) -> Dict:
    importance = float(event["importance"])
    polarity = float(event["polarity"])
    confidence = float(event["confidence"])

    impact_score = importance * (1 + polarity)
    decay_score = impact_score * 0.95
    composite_score = decay_score * confidence

    return {
        "event_id": event["event_id"],
        "score_ts": datetime.now(timezone.utc).isoformat(),
        "impact_score": round(impact_score, 3),
        "decay_score": round(decay_score, 3),
        "composite_score": round(composite_score, 3),
        "model_version": MODEL_VERSION,
    }
