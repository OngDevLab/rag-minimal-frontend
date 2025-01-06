import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, ColumnsAutoSizeMode
# import psycopg2
import requests

st.set_page_config(layout="wide")
st.title("Magi-Cloud")
st.write("Error Management System Minimal Demo")

conn = st.connection("postgresql", type="sql")
df = conn.query('SELECT error_message, response, prompt, feedback, id::TEXT as uuid FROM public.magi_kb;', ttl="60")



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
            st.title("Error:")
            st.markdown(error_message)
            st.title("Enter Feedback:")
            with st.form(uuid):
                text_input = st.text_input("Enter your feedback:")
                submitted = st.form_submit_button("Submit feedback")
            if submitted:
                st.write("You entered:", text_input)
                # text_input = text_input.replace(",", " ")
                # write_conn = psycopg2.connect(
                #     host = st.secrets['connections']['postgresql']['host'],
                #     database = st.secrets['connections']['postgresql']['database'],
                #     user = st.secrets['connections']['postgresql']['username'],
                #     password = st.secrets['connections']['postgresql']['password']
                # )
                # write_cur = write_conn.cursor()
                # write_cur.execute(f"UPDATE public.magi_kb SET feedback = '{text_input}' WHERE id = '{uuid}';")
                # write_conn.commit()
                # write_cur.close()
                # write_conn.close()
                # Define the URL of the function
                url = "https://x7fyoha7quuo4zr2tv47dd4oai0kjejs.lambda-url.us-east-1.on.aws/"

                # Define the data to be sent in the POST request
                host = "nervously-brilliant-carp.data-1.use1.tembo.io"
                data = {
                    "host": st.secrets['connections']['postgresql']['host'],
                    "database": st.secrets['connections']['postgresql']['database'],
                    "username": st.secrets['connections']['postgresql']['username'],
                    "password": st.secrets['connections']['postgresql']['password'],
                    "uuid": uuid,
                    "feedback": text_input
                }

                # Send the POST request and get the response
                response = requests.post(url, json=data)

                # Print the status code of the response
                st.write("your changes are now in the database")
                st.write(response.status_code)

                # Print the response content
                st.write(response.text)

                st.write("updated feedback")
                df = conn.query('SELECT error_message, response, prompt, feedback, id::TEXT as uuid FROM public.magi_kb;', ttl="60")
            st.markdown("---")
            st.title("Feedback:")
            st.write(feedback)
        with response_col:
            st.title("LLM Response")
            st.write(response)

