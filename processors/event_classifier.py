"""Rule-based baseline event classifier for COF events."""

from __future__ import annotations

from typing import Dict


RULES = {
    "charge_off": ["charge-off", "charge off", "net charge"],
    "delinquency": ["delinquency", "30+ day", "90+ day"],
    "earnings": ["earnings", "eps", "quarter results"],
    "guidance": ["guidance", "outlook", "forecast"],
    "regulation": ["federal reserve", "occ", "fdic", "capital rule", "stress test"],
    "m&a": ["acquisition", "integration", "discover", "merger"],
    "litigation": ["lawsuit", "settlement", "litigation", "consent order"],
    "macro": ["inflation", "rate hike", "fed funds", "unemployment"],
    "market_move": ["moved up", "moved down", "gap", "volatility"],
}


def classify_event(summary: str) -> Dict[str, float | int | str]:
    text = summary.lower()
    category = "general"
    confidence = 0.45
    importance = 45
    polarity = 0.0

    for label, keywords in RULES.items():
        if any(keyword in text for keyword in keywords):
            category = label
            confidence = 0.75
            break

    if any(word in text for word in ["beat", "improved", "up", "strong", "raised"]):
        polarity = 0.4
    elif any(word in text for word in ["miss", "decline", "down", "weak", "lowered"]):
        polarity = -0.4

    if category in {"earnings", "guidance", "charge_off", "delinquency", "regulation", "m&a"}:
        importance = 75

    if category == "litigation":
        importance = 65
        polarity = polarity if polarity != 0 else -0.3

    return {
        "category": category,
        "confidence": confidence,
        "importance": importance,
        "polarity": polarity,
    }
