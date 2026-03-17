PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS market_prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL,
    ts TEXT NOT NULL,
    open REAL,
    high REAL,
    low REAL,
    close REAL,
    volume REAL,
    source TEXT NOT NULL,
    inserted_at TEXT DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(symbol, ts, source)
);

CREATE TABLE IF NOT EXISTS filings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL,
    filing_type TEXT,
    accession_no TEXT UNIQUE,
    filing_ts TEXT,
    title TEXT,
    url TEXT,
    raw_text TEXT,
    source TEXT,
    inserted_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS news_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL,
    published_ts TEXT,
    source_name TEXT,
    title TEXT,
    url TEXT UNIQUE,
    body TEXT,
    author TEXT,
    inserted_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL,
    event_ts TEXT NOT NULL,
    source_type TEXT NOT NULL,
    source_ref_id TEXT,
    category TEXT,
    importance INTEGER,
    polarity REAL,
    confidence REAL,
    summary TEXT,
    key_metrics_json TEXT,
    inserted_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS event_scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER NOT NULL,
    score_ts TEXT NOT NULL,
    impact_score REAL,
    decay_score REAL,
    composite_score REAL,
    model_version TEXT,
    FOREIGN KEY(event_id) REFERENCES events(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS model_predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL,
    prediction_ts TEXT NOT NULL,
    horizon_days INTEGER NOT NULL,
    prob_up REAL NOT NULL,
    regime TEXT NOT NULL,
    model_version TEXT NOT NULL,
    feature_snapshot_json TEXT,
    inserted_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS pipeline_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_ts TEXT NOT NULL,
    stage TEXT NOT NULL,
    status TEXT NOT NULL,
    details_json TEXT,
    inserted_at TEXT DEFAULT CURRENT_TIMESTAMP
);
