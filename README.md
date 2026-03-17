# COF Real-Time Intelligence MVP

Local-first Python MVP for monitoring **Capital One (COF)** with a benchmark view against **SPY**.

## What this MVP includes

- Modular Python project structure
- SQLite storage layer with reusable helper class
- Market collector (COF + SPY via `yfinance`)
- Event storage pipeline (market -> event -> score -> prediction)
- Baseline rule-based event classifier
- Baseline scoring engine
- Initial directional probability model (1/5/20 day)
- Streamlit dashboard for UI only

## Project structure

```text
.
├── collectors/
│   └── market_collector.py
├── config/
│   └── settings.py
├── dashboard/
│   └── streamlit_app.py
├── db/
│   ├── database.py
│   └── schema.sql
├── models/
│   └── direction_model.py
├── processors/
│   ├── event_classifier.py
│   └── scoring_engine.py
├── services/
│   └── pipeline.py
├── data/
│   ├── raw/
│   └── processed/
├── main.py
└── requirements.txt
```

## Data model (SQLite)

Core tables:
- `market_prices`
- `filings`
- `news_items`
- `events`
- `event_scores`
- `model_predictions`
- `pipeline_runs`

Schema file: `db/schema.sql`

## Quick start

### 1) Create environment and install deps

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2) Run one ingestion cycle (creates DB + writes data)

```bash
python main.py --run-once
```

### 3) Run collector loop locally

```bash
python main.py --interval-seconds 60
```

### 4) Launch Streamlit dashboard

```bash
streamlit run dashboard/streamlit_app.py
```

## Notes

- Streamlit is UI only; ingestion runs through `main.py`.
- Pipeline currently uses market data events as the baseline event stream.
- Filings/news/event adapters are scaffolded in schema for next iteration.
