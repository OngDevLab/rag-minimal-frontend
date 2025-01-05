import streamlit as st
from st_aggrid import AgGrid
import pandas as pd
st.title("Magi-Cloud")
st.write("Error Management System Minimal Demo")

conn = st.connection("postgresql", type="sql")
df = conn.query('SELECT error_message, response, prompt, feedback FROM public.magi_kb;', ttl="10m")
grid_return = AgGrid(df)