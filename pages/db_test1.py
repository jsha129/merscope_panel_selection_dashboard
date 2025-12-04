import streamlit as st
import pandas as pd
import pg8000

# --- Neon PostgreSQL connection details ---
HOST = "ep-icy-dawn-a7q2fmwh-pooler.ap-southeast-2.aws.neon.tech"
USER = "neondb_owner"
PASSWORD = "npg_2zsJAF3pECPo"
DATABASE = "neondb"
PORT = 5432

# --- Connect to Neon using pg8000 ---
conn = pg8000.connect(
    host=HOST,
    user=USER,
    password=PASSWORD,
    database=DATABASE,
    port=PORT,
    ssl_context=True  # Neon requires SSL
)

# --- Query ---
query = "SELECT * FROM home LIMIT 10;"

# --- Fetch data into pandas ---
df = pd.read_sql(query, conn)


#engine = create_engine("postgresql://neondb_owner:npg_2zsJAF3pECPo@ep-icy-dawn-a7q2fmwh-pooler.ap-southeast-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require")

# Static table
st.table(df)
