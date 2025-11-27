# ---- File: app.py ----
import streamlit as st
import pandas as pd


@st.cache_data
def load_data(uploaded_file):
    df = pd.read_excel(uploaded_file,sheet_name = "Sheet1", nrows = 1000)
    df = df.rename(columns={'DE_in_some': 'DE_in_some_cells', 'is_DE_BS_EC': 'DE_in_Bstem_Endothelial'})
    df = df.sort_values(by = 'gene').reset_index()
    df = df.drop(columns = 'index')
    return df


st.set_page_config(page_title="Merscope gene selection app")


st.title("Upload File")
uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx", "xls"])


if uploaded_file:
    st.session_state.df = load_data(uploaded_file)
    st.session_state.idx = 0
    st.switch_page("pages/record_view.py")
