import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://neondb_owner:npg_2zsJAF3pECPo@ep-icy-dawn-a7q2fmwh-pooler.ap-southeast-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require")

df = pd.read_sql("SELECT * FROM home LIMIT 10;", engine)

# Static table
st.table(df)
