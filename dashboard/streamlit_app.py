"""Streamlit MVP dashboard for COF intelligence."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from config.settings import settings
from db.database import Database


st.set_page_config(page_title="COF Intelligence MVP", layout="wide")
st.title("Capital One (COF) Real-Time Intelligence MVP")


db = Database(settings.db_path)

df_prices = pd.DataFrame([dict(row) for row in db.fetch_latest_prices(["COF", "SPY"])])
df_events = pd.DataFrame([dict(row) for row in db.fetch_recent_events(limit=25)])
df_preds = pd.DataFrame([dict(row) for row in db.fetch_latest_predictions("COF")])

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Latest Prices")
    if df_prices.empty:
        st.info("No market data yet. Run `python main.py --run-once`.")
    else:
        st.dataframe(df_prices[["symbol", "ts", "close", "volume"]], use_container_width=True)

with col2:
    st.subheader("Direction Probabilities")
    if df_preds.empty:
        st.info("No predictions yet.")
    else:
        piv = df_preds.drop_duplicates(subset=["horizon_days"], keep="first")
        st.dataframe(piv[["horizon_days", "prob_up", "regime", "prediction_ts"]], use_container_width=True)

with col3:
    st.subheader("Recent COF Events")
    if df_events.empty:
        st.info("No events yet.")
    else:
        st.dataframe(
            df_events[["event_ts", "category", "importance", "polarity", "composite_score", "summary"]],
            use_container_width=True,
            height=300,
        )

st.markdown("---")
st.caption("MVP scope: local SQLite + market ingestion + rule-based event classifier + baseline scoring and direction model")
