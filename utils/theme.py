"""Shared colors, CSS, and the header used on every page (mirrors the Power Apps styling)."""
import os
import streamlit as st

# Colors pulled from the Power Apps RGBA() values
PAGE_BG = "#939899"        # Home Page Container  RGBA(147,152,153,1)
ACCENT = "#F1562B"         # Navigation pill      RGBA(241,86,43,1)
HEADER_BG = "#333333"      # Header container     RGBA(51,51,51,1)
LINK_BLUE = "#2771C2"      # Help icon            RGBA(39,113,194,1)

APP_VERSION = "Rev 1.0"    # Replaces the "Sylvan App Rev Component"

HELP_URL = (
    "https://fmsylvan2.sharepoint.com/:w:/s/SylvanConveyorToolbox/"
    "IQCoIYdazZr5Src6GhcWYS-AAdJ9sIQaWSD4gYIe3ieuNdc?e=aK2hCc"
)
# TODO: point this at wherever the "Bug Report" component submits today (Form, List, flow, etc.)
BUG_REPORT_URL = ""

ASSETS = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")


def asset(name: str) -> str | None:
    """Return the path to an image in /assets if it exists, else None."""
    for ext in ("", ".png", ".jpg", ".jpeg", ".svg"):
        path = os.path.join(ASSETS, name + ext)
        if os.path.isfile(path):
            return path
    return None


def apply_css() -> None:
    st.markdown(
        f"""
        <style>
        .stApp {{ background-color: {PAGE_BG}; }}
        .block-container {{ padding-top: 1.5rem; max-width: 1400px; }}

        .sy-header {{
            background: {HEADER_BG}; border-radius: 8px; padding: 14px 22px;
            display: flex; align-items: center; gap: 18px; margin-bottom: 1.25rem;
        }}
        .sy-header h1 {{
            color: #fff; font-family: Verdana, sans-serif; font-weight: 700;
            font-size: 1.9rem; margin: 0; padding: 0;
        }}
        .sy-header .divider {{ width: 2px; height: 36px; background: #fff; }}

        .sy-pill {{
            display: inline-block; background: {ACCENT}; color: #fff;
            font-family: 'Segoe UI', sans-serif; font-weight: 700; font-size: 1.15rem;
            border-radius: 10px; padding: 6px 28px; margin-bottom: 1rem;
        }}

        .sy-card {{
            background: #fff; border-radius: 10px; padding: 8px 12px 12px;
            text-align: center; min-height: 105px;
        }}
        .sy-card h3 {{
            font-size: 1.1rem; font-weight: 700; font-style: italic;
            text-decoration: underline; margin: 0 0 4px; padding: 0; color: #222;
        }}
        .sy-card p {{ font-size: 0.85rem; margin: 0; color: #333; }}

        .sy-footer {{ color: #fff; text-align: right; font-size: 0.8rem; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def header(title: str) -> None:
    """Dark header bar with the Sylvan banner and page title."""
    apply_css()
    logo = asset("Sylvan Banner 2")
    left, right = st.columns([5, 1])
    with left:
        if logo:
            c1, c2 = st.columns([1, 3], vertical_alignment="center")
            c1.image(logo, width=212)
            c2.markdown(f'<div class="sy-header"><h1>{title}</h1></div>', unsafe_allow_html=True)
        else:
            st.markdown(
                f'<div class="sy-header"><h1 style="color:{ACCENT}">SYLVAN</h1>'
                f'<div class="divider"></div><h1>{title}</h1></div>',
                unsafe_allow_html=True,
            )
    with right:
        if BUG_REPORT_URL:
            st.link_button("Report a bug", BUG_REPORT_URL, icon=":material/bug_report:", width="stretch")
        else:
            st.button("Report a bug", icon=":material/bug_report:", disabled=True,
                      help="Set BUG_REPORT_URL in utils/theme.py", width="stretch")


def back_home() -> None:
    if st.button("Home", icon=":material/arrow_back:"):
        st.switch_page(st.session_state["pages"]["Home"])
