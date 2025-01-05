import streamlit as st

st.title("hello world")

conn = st.connection("postgresql", type="sql")
df = conn.query('SELECT error_message, response, prompt, feedback FROM public.magi_kb;', ttl="10m")
st.dataframe(df)