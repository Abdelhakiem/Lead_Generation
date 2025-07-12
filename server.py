# root_app.py
import streamlit as st
import pandas as pd
from campaign_targeting.app import run_campaign_targeting_page
from user_profiling.st2 import user_directory_page

# --- Main Entry Point ---
st.set_page_config(page_title="Lead Gen System", layout="wide")

# Sidebar multipage navigation
page = st.sidebar.selectbox("Navigate", ["Campaign Targeting", "User Directory"])

if page == "Campaign Targeting":
    run_campaign_targeting_page()
elif page == "User Directory":
    user_directory_page()


