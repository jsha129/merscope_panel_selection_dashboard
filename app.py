import streamlit as st
import pandas as pd

st.set_page_config(page_title="Uploader", layout="wide")

st.title("📁 Upload Excel File")

uploaded = st.file_uploader("Choose Excel file", type=["xlsx", "xls"])

if uploaded:
    df = pd.read_excel(uploaded, sheet_name = "Sheet1")
    df = df.sort_values(by = 'Gene')
    st.session_state["df"] = df
    st.success("File loaded successfully!")

    # Move to next page
    st.page_link("pages/2_Form_Page.py", label="Go to Form Page →")
