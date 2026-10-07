"""Home screen - rebuilt from the Power Apps `Home` screen."""
import streamlit as st

from utils.abm_cache import get_col_abm_master
from utils.theme import APP_VERSION, HELP_URL, asset, header

header("App Home Page")

st.markdown('<div class="sy-pill">Navigation</div>', unsafe_allow_html=True)

# (title, description, image asset name, target page, on-click hook)
# "New ABM Request" is Visible=false in Power Apps, so it's kept here but disabled.
SHOW_NEW_ABM_REQUEST = False


def _open_abm_lookup():
    # Mirrors ABM Lookup Button.OnSelect: load cache into colABMMaster if empty, then Navigate
    try:
        get_col_abm_master()
    except Exception as e:
        st.session_state["abm_load_error"] = str(e)


CARDS = [
    ("ABM Lookup",
     "This App function can be utilized to search for existing catelogued ABMs by number or description.",
     "ABM Lookup Icon", "ABM Lookup", _open_abm_lookup),
    ("Material Order Form",
     "Utilize this App function to complete ABM orders from existing items within our catalog.",
     "ChatGPT Image Jan 27, 2026, 06_43_39 AM", "Material Order Form", None),
    ("Order Tracking",
     "Utilize this function to search tracking information for existing order, modify orders, and create shippers.",
     "Order Tracking", "ABM Order Lookup", None),
    ("Work Orders",
     "Utilize this function to lookup existing work orders, assigned vendors, and status.",
     "Work Orders Logo", "Work Orders", None),
]

if SHOW_NEW_ABM_REQUEST:
    CARDS.insert(1, (
        "New ABM Request",
        "This function will allow users to generate new ABM numbers and intake related documentation "
        "such as cut sheets or drawings.",
        "WIP App Buttons_Page 1", None, None,
    ))

cols = st.columns(len(CARDS), gap="large")
for col, (title, desc, img, target, hook) in zip(cols, CARDS):
    with col:
        img_path = asset(img)
        if img_path:
            st.image(img_path, width="stretch")
        else:
            st.container(height=200, border=False)  # keeps layout when image isn't present yet

        if st.button(f"Open {title}", key=f"btn_{title}", width="stretch",
                     type="primary", disabled=target is None):
            if hook:
                hook()
            st.switch_page(st.session_state["pages"][target])

        st.markdown(f'<div class="sy-card"><h3>{title}</h3><p>{desc}</p></div>', unsafe_allow_html=True)

st.write("")
_, help_col = st.columns([6, 1])
with help_col:
    st.link_button("Instructions", HELP_URL, icon=":material/help:", width="stretch")
    with st.popover(APP_VERSION, width="stretch"):
        # Replaces the transparent Changelog Button sitting over the Rev component
        st.markdown("**Changelog**")
        st.caption("Add release notes here (or load from a CHANGELOG.md).")
