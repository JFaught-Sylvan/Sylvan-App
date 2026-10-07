"""ABM Lookup - search colABMMaster by ABM number or description."""
import streamlit as st

from utils.abm_cache import get_col_abm_master
from utils.theme import back_home, header

header("ABM Lookup")
back_home()

if err := st.session_state.pop("abm_load_error", None):
    st.error(f"Could not load ABM cache: {err}")

try:
    df = get_col_abm_master()
except Exception as e:
    st.error(f"Could not load ABM cache: {e}")
    st.info("Set ABM_CACHE_FLOW_URL or ABM_CACHE_PATH in .streamlit/secrets.toml, "
            "or place ABMCache.json in the data/ folder.")
    st.stop()

c1, c2 = st.columns([3, 1])
query = c1.text_input("Search by ABM number or description", placeholder="e.g. 10045 or roller")
series = c2.selectbox("Series", ["All"] + sorted(s for s in df["Series"].unique() if s))

result = df
if query:
    q = query.strip()
    result = result[
        result["ABM"].str.contains(q, case=False, na=False, regex=False)
        | result["Description"].str.contains(q, case=False, na=False, regex=False)
    ]
if series != "All":
    result = result[result["Series"] == series]

st.caption(f"{len(result):,} of {len(df):,} ABMs")
st.dataframe(result, width="stretch", hide_index=True, height=520)

if st.button("Refresh catalog", icon=":material/refresh:"):
    st.cache_data.clear()
    st.session_state.pop("colABMMaster", None)
    st.rerun()
