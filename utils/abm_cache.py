"""Replacement for the Power Automate flow `LoadABMCache` + the ParseJSON/ClearCollect logic.

Power Apps flow:  LoadABMCache.Run().abmcache  -> JSON string from ABMCache.json
Power Apps then:  ClearCollect(colABMMaster, ForAll(ParseJSON(...), {ABM, Description, ...}))

Here the same thing happens in load_abm_master(), which returns a pandas DataFrame
(the equivalent of colABMMaster). Data is fetched from, in order of preference:
  1. An HTTP-triggered Power Automate flow   (st.secrets["ABM_CACHE_FLOW_URL"])
  2. A local / network copy of ABMCache.json (st.secrets["ABM_CACHE_PATH"] or data/ABMCache.json)
"""
import json
import os

import pandas as pd
import requests
import streamlit as st

# Source key in ABMCache.json  ->  column name in colABMMaster
FIELD_MAP = {
    "ABM": "ABM",
    "Description": "Description",
    "Manufacturer": "Manufacturer",
    "Part Number": "PartNumber",
    "Lead Time": "LeadTime",
    "Series": "Series",
}

DEFAULT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "ABMCache.json")


def _secret(key: str):
    try:
        return st.secrets.get(key)
    except Exception:  # no secrets.toml present
        return None


def _fetch_raw():
    """Return the raw cache payload (str, list, or dict)."""
    flow_url = _secret("ABM_CACHE_FLOW_URL")
    if flow_url:
        resp = requests.post(flow_url, json={}, timeout=60)
        resp.raise_for_status()
        body = resp.json()
        # Flow responds with {"abmcache": "<json string>"} like the Power Apps version
        return body.get("abmcache", body) if isinstance(body, dict) else body

    path = _secret("ABM_CACHE_PATH") or DEFAULT_PATH
    with open(path, "r", encoding="utf-8-sig") as f:
        return f.read()


@st.cache_data(ttl=3600, show_spinner="Loading ABM catalog...")
def load_abm_master() -> pd.DataFrame:
    raw = _fetch_raw()
    records = json.loads(raw) if isinstance(raw, str) else raw
    if isinstance(records, dict):  # tolerate {"value": [...]} style wrappers
        records = next((v for v in records.values() if isinstance(v, list)), [])

    # Equivalent of: ForAll(Table(ParseJSON(...)), { ABM: Text(Value.ABM), ... })
    rows = [
        {dst: ("" if r.get(src) is None else str(r.get(src))) for src, dst in FIELD_MAP.items()}
        for r in records
    ]
    return pd.DataFrame(rows, columns=list(FIELD_MAP.values()))


def get_col_abm_master() -> pd.DataFrame:
    """Session-level collection, only loaded if empty (mirrors `If(IsEmpty(colABMMaster), ...)`)."""
    if st.session_state.get("colABMMaster") is None or st.session_state["colABMMaster"].empty:
        st.session_state["colABMMaster"] = load_abm_master()
    return st.session_state["colABMMaster"]
