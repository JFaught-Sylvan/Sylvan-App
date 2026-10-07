"""Sylvan App - Streamlit entry point.

Run with:  streamlit run app.py
"""
import streamlit as st

st.set_page_config(
    page_title="Sylvan App",
    page_icon="assets/favicon.png" if __import__("os").path.exists("assets/favicon.png") else None,
    layout="wide",
)

# Each Power Apps screen becomes a Streamlit page.
# The `url_path` values double as the Navigate() targets used on the Home page.
home = st.Page("views/home.py", title="Home", icon=":material/home:", default=True)
abm_lookup = st.Page("views/abm_lookup.py", title="ABM Lookup", icon=":material/search:", url_path="abm_lookup")
material_order = st.Page("views/material_order_form.py", title="Material Order Form", icon=":material/shopping_cart:", url_path="material_order_form")
order_lookup = st.Page("views/abm_order_lookup.py", title="Order Tracking", icon=":material/local_shipping:", url_path="abm_order_lookup")
work_orders = st.Page("views/work_orders.py", title="Work Orders", icon=":material/assignment:", url_path="work_orders")

# Store pages so other modules can call st.switch_page() with them
st.session_state["pages"] = {
    "Home": home,
    "ABM Lookup": abm_lookup,
    "Material Order Form": material_order,
    "ABM Order Lookup": order_lookup,
    "Work Orders": work_orders,
}

pg = st.navigation([home, abm_lookup, material_order, order_lookup, work_orders], position="hidden")
pg.run()
