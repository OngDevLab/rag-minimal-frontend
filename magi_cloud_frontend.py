import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, ColumnsAutoSizeMode
import psycopg2

st.set_page_config(layout="wide")
st.title("Magi-Cloud")
st.write("Error Management System Minimal Demo")

# conn = st.connection("postgresql", type="sql")
# df = conn.query('SELECT error_message, response, prompt, feedback, id::TEXT as uuid FROM public.magi_kb;', ttl="10m")
@st.cache_data(ttl=600)  # Cache for 10 minutes
def get_data():
    conn = st.connection("postgresql", type="sql")
    df = conn.query('SELECT error_message, response, prompt, feedback, id::TEXT as uuid FROM public.magi_kb;')
    return df


df = get_data()  # Initial fetch
grid_builder = GridOptionsBuilder.from_dataframe(df)
grid_builder.configure_selection(selection_mode="multiple", use_checkbox=True)
grid_builder.configure_side_bar(filters_panel=True, columns_panel=False)
grid_builder.configure_grid_options(autoHeight=True)
grid_builder.configure_columns(['error_message', 'response','prompt','feedback','uuid'], wrapText=True, autoHeight=True, width=420)
grid_options = grid_builder.build()
grid_return = AgGrid(data=df, gridOptions=grid_options, key='grid1', columns_auto_size_mode=ColumnsAutoSizeMode.FIT_ALL_COLUMNS_TO_VIEW)

selected_rows = grid_return['selected_rows']

if selected_rows is not None:
    for index, row in selected_rows.iterrows():
        st.markdown("---")
        error_col, response_col = st.columns([1,1])
        error_message = row['error_message']
        response = row['response']
        feedback = row['feedback']
        uuid = row['uuid']
        with error_col:
            st.markdown(error_message)
            with st.form(uuid):
                text_input = st.text_input("Enter your feedback:")
                submitted = st.form_submit_button("Submit feedback")
            if submitted:
                st.write("You entered:", text_input)
                write_conn = psycopg2.connect(
                    host = st.secrets['connections']['postgresql']['host'],
                    database = st.secrets['connections']['postgresql']['database'],
                    user = st.secrets['connections']['postgresql']['username'],
                    password = st.secrets['connections']['postgresql']['password']
                )
                write_cur = write_conn.cursor()
                write_cur.execute(f"UPDATE public.magi_kb SET feedback = '{text_input}' WHERE id = '{uuid}';")
                write_conn.commit()
                write_cur.close()
                write_conn.close()

                st.write("updated feedback")
                df.clear()
        with response_col:
            st.write(response)
            st.markdown("---")
            st.write(feedback)