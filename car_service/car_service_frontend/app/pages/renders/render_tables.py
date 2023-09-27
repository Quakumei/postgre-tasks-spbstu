import pandas as pd

import streamlit as st
from st_aggrid import AgGrid

import tomli
from sqlalchemy import create_engine 

def read_connection_string(secrets_toml: str = "secrets.toml", db_name: str = "car_service_db") -> dict:
    """Parses secrets.toml file and returns connection string for sqlalchemy"""
    with open("secrets.toml", "rb") as f:
        data = tomli.load(f)
    return data["connections"][db_name]["url"]


engine = create_engine(read_connection_string(), echo=False)

def submit_changes(old_df: pd.DataFrame, edited_df: pd.DataFrame, table_name:str):
    """Appends changes to the db"""
    assert False, "DB changes are WIP"
    # 1. Remove removed rows
    ids_to_remove = [id for id in old_df.id if id not in edited_df and not id is None]
    ids_remove_query = f"DELETE FROM {table_name} WHERE id IN ({', '.join(map(str, ids_to_remove))})"
    result = engine.execute(ids_remove_query)

    # 2. Append new rows
    ids_to_add = [id for id in edited_df if id not in old_df and not id is None]
    for new_row in edited_df.loc[df.id.isin(ids_to_add)]:
        add_row_query = f"INSERT INTO {table_name} ({', '.join(map(str, old.df.columns))}) VALUES ({', '.join(map(str, new_row))}"
        result = engine.execute(add_row_query)

    # 3. Modify edited rows
    modified_result = old_df.merge(edited_df, on='id', suffixes=('_df1', '_df2'))
    new_df = pd.DataFrame()
    for column in edited_df.columns:
        if column.endswith('_df2'):
            new_df[column.replace('_df2', '')] =  modfied_result[column]
     



def render_table_default(engine, table_name: str):
    with st.expander(table_name.capitalize()):
        with st.form(f'edit-form-{table_name}'):
            df = pd.read_sql(table_name, con=engine)
            # st.dataframe(df)
            edited_df = st.data_editor(df, num_rows='dynamic', disabled=['id',])
            # st.markdown(f"Your change is {edited_df}")
            st.form_submit_button('Submit changes', on_click=lambda: submit_changes(df, edited_df, table_name))


TABLES = {"masters", "cars", "services"}
def render_tables():
    for table_name in TABLES:
        render_table_default(engine, table_name)
