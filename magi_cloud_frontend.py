import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, ColumnsAutoSizeMode
import pandas as pd
st.set_page_config(layout="wide")
st.title("Magi-Cloud")
st.write("Error Management System Minimal Demo")

conn = st.connection("postgresql", type="sql")
df = conn.query('SELECT error_message, response, prompt, feedback FROM public.magi_kb;', ttl="10m")

grid_builder = GridOptionsBuilder.from_dataframe(df)
grid_builder.configure_selection(selection_mode="single", use_checkbox=True)
grid_builder.configure_side_bar(filters_panel=True, columns_panel=False)
grid_builder.configure_grid_options(autoHeight=True)
grid_builder.configure_columns(['error_message', 'response','prompt'], wrapText=True, autoHeight=True, width=420)
grid_options = grid_builder.build()
grid_return = AgGrid(data=df, gridOptions=grid_options, key='grid1', columns_auto_size_mode=ColumnsAutoSizeMode.FIT_ALL_COLUMNS_TO_VIEW)