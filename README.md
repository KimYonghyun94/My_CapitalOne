# Capital One Real-Time Intelligence System — Codex Handoff

## Goal

Build a local-fi([openai.com](https://openai.com/codex/get-started/?utm_source=chatgpt.com))r **Capital One (COF)** that continuously collects and analyzes:

* market data
* SEC filings
* earnings releases
* company investor-relations updates
* major news
* monthly credit-quality metrics
* macro/rates context

The system should prioritize **decision support**, not naive point-price prediction.

## Product definition

This is **not** a simple stock app.
It is a **Capital One real-time intelligence and monitoring platform** with:

1. real-time / near-real-time data collection
2. event classification and summarization
3. COF-specific scoring engine
4. direction/risk models
5. Streamlit dashboard for visualization

## Important constraints

* Use **local backend + local DB + Streamlit dashboard**.
* Do **not** rely on Streamlit as the always-on collector.
* Streamlit is the UI layer only.
* The collector and analysis workers must run independently.
* Start with SQLite for local development, but design code so PostgreSQL can be added later.
* Keep architecture modular.
* Write clean Python with comments, type hints where practical, and clear folder separation.

## Why this architecture

Streamlit is good for interactive dashboards, but the always-on collection/processing loop should live outside the Streamlit app. The dashboard reads from the database and refreshes periodically.

## Business / domain context for COF

Capital One should not be treated like a generic tech stock.
It is heavily influenced by:

* consumer credit quality
* charge-off trends
* delinquency trends
* interest-rate environment
* bank regulation
* earnings/guidance
* M&A integration and strategic actions

The system must treat the following as high-priority events:

* earnings beat/miss
* guidance changes
* 8-K investor updates
* monthly charge-off / delinquency updates
* Discover integration developments
* Brex-related developments
* major regulatory / capital-rule news
* material litigation / compliance items

## Target outputs

The system should produce:

* latest COF monitoring dashboard
* event feed with priority labels
* event summaries
* bullish / neutral / bearish impact scoring
* 1-day / 5-day / 20-day directional probability
* risk regime tag
* model and event audit trail

## Folder structure

```text
cof-intel/
  README.md
  requirements.txt
  .env.example
  main.py

  config/
    settings.py

  db/
    schema.sql
    database.py

  collectors/
    market_collector.py
    sec_collector.py
    news_collector.py
    ir_collector.py
    macro_collector.py

  processors/
    deduper.py
    event_classifier.py
    summarizer.py
    sentiment_engine.py
    feature_builder.py
    scoring_engine.py

  models/
    direction_model.py
    risk_model.py
    backtest.py

  services/
    scheduler.py
    pipeline.py

  dashboard/
    streamlit_app.py

  utils/
    logging_utils.py
    time_utils.py
    text_utils.py

  data/
    raw/
    processed/

  tests/
    test_collectors.py
    test_processors.py
    test_models.py
```

## Database design

Use SQLite initially.
Create tables such as:

* `market_prices`
* `filings`
* `news_items`
* `ir_events`
* `macro_series`
* `events`
* `event_scores`
* `model_features`
* `model_predictions`
* `pipeline_runs`

Suggested fields:

### market_prices

* id
* symbol
* ts
* open
* high
* low
* close
* volume
* source

### filings

* id
* symbol
* filing_type
* accession_no
* filing_ts
* title
* url
* raw_text
* source
* inserted_at

### news_items

* id
* symbol
* published_ts
* source_name
* title
* url
* body
* author
* inserted_at

### events

* id
* symbol
* event_ts
* source_type
* source_ref_id
* category
* importance
* polarity
* summary
* key_metrics_json
* inserted_at

### model_predictions

* id
* symbol
* prediction_ts
* horizon_days
* prob_up
* regime
* model_version
* feature_snapshot_json

## Pipeline stages

### 1. Ingestion

Collectors fetch data from sources and store raw data.

### 2. Normalization

Normalize timestamps, remove duplicates, standardize symbols and source metadata.

### 3. Event extraction

Convert filings/news/IR items into structured events.

### 4. Event classification

Classify into categories such as:

* earnings
* guidance
* charge_off
* delinquency
* m&a
* regulation
* litigation
* macro
* market_move
* management

### 5. Scoring

Each event gets:

* importance score (0-100)
* polarity score (-1 to +1)
* confidence score
* decay logic over time

### 6. Feature building

Create model-ready features using:

* technicals
* market relative strength
* rolling volatility
* event scores
* macro variables
* credit-quality trends

### 7. Prediction

Generate probabilities for 1 / 5 / 20 trading days.

### 8. Dashboard display

Streamlit shows current state and recent events.

## Initial data-source priorities

Phase 1 should focus on sources that are reliable and structured.

Priority order:

1. market data
2. SEC filings / 8-K / 10-Q / 10-K
3. Capital One investor relations / earnings releases
4. monthly credit metrics from company disclosures
5. major financial news headlines
6. macro / rates series

## Scoring philosophy

Do not treat all headlines equally.
COF-specific event weighting should be stronger for:

* charge-off deterioration/improvement
* delinquency trend changes
* earnings surprise
* guidance revisions
* regulatory capital changes affecting banks
* acquisition integration risks/opportunities

Lower weight for:

* generic media repetition
* low-information commentary
* duplicated summaries

## Model philosophy

Avoid promising exact price prediction.
Prefer:

* directional probability
* event-driven risk score
* regime labeling

Recommended initial models:

* logistic regression baseline
* random forest baseline
* gradient boosting / xgboost later

## Scheduling

Design the local pipeline with configurable intervals:

* market data: every 1 minute
* SEC/IR: every 5 minutes
* news: every 2 to 5 minutes
* feature refresh: on new data or every 5 minutes
* prediction refresh: every 5 minutes

## Dashboard pages

Create Streamlit tabs/pages:

1. Overview
2. Live Event Feed
3. Filings & IR
4. Credit Metrics Monitor
5. Macro / Rates Context
6. Prediction & Risk
7. Backtest / Audit
8. Settings / Source Status

## Phase 1 implementation target

Implement a working local MVP that includes:

* SQLite database
* market collector
* SEC collector skeleton
* news collector skeleton
* event table population
* simple rule-based classifier
* simple scoring engine
* baseline prediction model
* Streamlit dashboard with overview + recent events + prediction panel

## Deliverables Codex should create first

1. complete folder structure
2. `requirements.txt`
3. `README.md`
4. SQLite schema
5. database helper module
6. market collector
7. SEC collector placeholder with adapter interface
8. event classifier baseline
9. scoring engine baseline
10. feature builder baseline
11. baseline direction model
12. Streamlit dashboard MVP
13. local run instructions

## Code quality requirements

* Python 3.11+
* modular functions/classes
* docstrings on important modules
* avoid monolithic single-file app
* no hardcoded secrets
* use environment variables where appropriate
* include logging
* gracefully handle missing data / failed requests

## What Codex should do now

1. scaffold the repository
2. write the SQLite schema and DB helper
3. implement a market data collector for COF and benchmark SPY
4. implement an events table pipeline
5. create a simple rule-based event classifier
6. create a simple scoring engine
7. build a Streamlit dashboard MVP
8. write a README with setup and run commands

## Suggested kickoff instruction for Codex

Use this repository brief to build the initial local MVP of a Capital One real-time intelligence platform. Start by scaffolding the project structure, then implement SQLite storage, market data ingestion, structured event storage, a rule-based event classifier, a baseline scoring engine, and a Streamlit dashboard. Optimize for maintainability and local execution. Use Python. Keep the code modular and production-minded. Do not over-focus on exact price prediction; focus on reliable ingestion, event structuring, and decision-support outputs.

## Suggested follow-up task sequence in Codex

* Task 1: Scaffold repo and write requirements/README/schema.
* Task 2: Build DB helper and market collector.
* Task 3: Build event ingestion and normalization pipeline.
* Task 4: Build baseline classifier and scoring engine.
* Task 5: Build baseline model and dashboard.
* Task 6: Improve source adapters and add tests.
