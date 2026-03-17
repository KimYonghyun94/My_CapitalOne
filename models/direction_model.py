"""Initial direction model using simple event and relative strength heuristics."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict


MODEL_VERSION = "direction-baseline-v1"


def compute_direction_probabilities(cof_close: float, spy_close: float, avg_event_score: float) -> Dict:
    relative_strength = ((cof_close - spy_close) / spy_close) if spy_close else 0
    base = 0.5 + (0.08 * relative_strength) + (0.004 * avg_event_score)
    prob_up_1d = min(max(base, 0.05), 0.95)
    prob_up_5d = min(max(base + 0.03, 0.05), 0.95)
    prob_up_20d = min(max(base + 0.06, 0.05), 0.95)

    regime = "risk_on" if avg_event_score >= 50 else "risk_off"
    if 40 <= avg_event_score < 50:
        regime = "balanced"

    now = datetime.now(timezone.utc).isoformat()
    return {
        "prediction_ts": now,
        "model_version": MODEL_VERSION,
        "regime": regime,
        "horizons": [
            {"horizon_days": 1, "prob_up": round(prob_up_1d, 3)},
            {"horizon_days": 5, "prob_up": round(prob_up_5d, 3)},
            {"horizon_days": 20, "prob_up": round(prob_up_20d, 3)},
        ],
    }
