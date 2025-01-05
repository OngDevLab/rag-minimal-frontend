import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
import pandas as pd
st.set_page_config(layout="wide")
st.title("Magi-Cloud")
st.write("Error Management System Minimal Demo")

conn = st.connection("postgresql", type="sql")
df = conn.query('SELECT error_message, response, prompt, feedback FROM public.magi_kb;', ttl="10m")

grid_builder = GridOptionsBuilder.from_dataframe(df)
grid_builder.configure_selection(selection_mode="multiple", use_checkbox=True)
grid_builder.configure_side_bar(filters_panel=True, columns_panel=False)
grid_options = grid_builder.build()

grid_return = AgGrid(data=df, gridOptions=grid_options, key='grid1')