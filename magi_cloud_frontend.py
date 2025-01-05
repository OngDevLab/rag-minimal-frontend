import streamlit as st

st.title("hello world")

conn = st.connection("postgresql", type="sql")
df = conn.query('SELECT 1;', ttl="10m")