import pandas as pd

import streamlit as st
from st_aggrid import AgGrid

def get_table(conn, table_name: str, limit: int = 100) -> pd.DataFrame:
    """Fetches rows from specified table""" 
    df = pd.read_sql(table_name, con=conn)
    return df

def render_table_default(conn, table_name: str) -> None:
    """Renders information about table and funcs to modify it"""
    st.markdown("---")
    st.markdown(f"### {table_name}")
    st.dataframe(get_table(conn, table_name))


TABLES = {"masters", "cars", "services"}
def render_tables():
    conn = st.experimental_connection("car_service_db")
    for table_name in TABLES:
        render_table_default(conn, table_name)
