import datetime
import time

import pandas as pd
from pandas.testing import assert_frame_equal

import streamlit as st
from st_aggrid import AgGrid
from streamlit_modal import Modal

import tomli
from sqlalchemy import create_engine, text 

def read_connection_string(secrets_toml: str = "secrets.toml", db_name: str = "car_service_db") -> dict:
    """Parses secrets.toml file and returns connection string for sqlalchemy"""
    with open("secrets.toml", "rb") as f:
        data = tomli.load(f)
    return data["connections"][db_name]["url"]

engine = create_engine(read_connection_string(), echo=False)

def show_modal(modal, df_change: pd.DataFrame, table_name): 
    with modal.container():
        st.markdown(f"{df_change=}")

def get_update_query(column, value, id, table_name):
    return f"UPDATE {table_name} SET {column} = '{value}' WHERE id = {id}"

def apply_modifications(engine, table_name: str, change_df: pd.DataFrame):
    """Apply modifications made in df"""
    col_to_idx = {v: k for (k, v) in enumerate(change_df.columns)}
    with engine.connect() as conn:
        for id, item in change_df.iterrows():
            for col in change_df.columns:
                value = item.iloc[col_to_idx[col]]
                query = get_update_query(col, value, id, table_name)
                result = conn.execute(text(query))
        conn.commit()
        
def add_entry(engine, table_name:str, entry):
    """Add entered entry to table_name"""
    cols = ', '.join(entry.columns)
    values = ', '.join([f"'{k}'" for k in entry.iloc[0]])
    query = f"INSERT INTO {table_name} ({cols}) VALUES ({values})"
    with engine.connect() as conn:
        try:
            result = conn.execute(text(query))
            conn.commit()
        except Exception as e:
            st.exception(e)


def remove_entry(engine, entry_id, table_name):
    """Remove entry with id specified from table_name"""
    query = f'DELETE FROM {table_name} WHERE id = {entry_id}'
    with engine.connect() as conn:
        try:
            result = conn.execute(text(query))
            conn.commit()
        except Exception as e:
            st.exception(e)



def render_table_default(engine, table_name: str):
    with st.expander(table_name.capitalize()):
        st.markdown("Для редактирования таблицы, нажмите дважды на ее ячейку")
        if 'key' not in st.session_state: 
            st.session_state.key = 0
        df = pd.read_sql(table_name, con=engine).set_index('id')
        edited_df = st.data_editor(
            df, 
            hide_index=False, 
            disabled=['id',],
            key=f'data-editor-{table_name}-{st.session_state.key}'
        )
        col1, col2= st.columns(2)
        remove_button = False
        add_button = False
        with col1:
            df_change = edited_df[~edited_df.isin(df).all(axis=1)]
            if df_change.shape[0] != 0:
                st.markdown(f"*Изменения в {df_change.shape[0]} строчках...*")
                st.dataframe(df_change, hide_index=False)
            st.button("Применить изменения",key=f'apply-{table_name}', on_click=apply_modifications, args=(engine, table_name, df_change), disabled=df_change.shape[0]==0)
        with col2:
            st.markdown("**Добавить**")
            row_entry = st.data_editor(pd.DataFrame([len(df.columns)*[None],],columns=df.columns), hide_index=True, disabled=['id',])
            add_button = st.button("Добавить запись", key=f'add-{table_name}', on_click=add_entry, args=(engine, table_name, row_entry), disabled=df_change.shape[0]!=0 and not remove_button)
            st.markdown("---")
            st.markdown("**Удалить**")
            remove_button_idx = st.selectbox(label="Id записи", options=sorted(list(df.index.values)), disabled=df_change.shape[0]!=0 )
            remove_button = st.button("Удалить запись", key=f'remove-{table_name}', on_click=remove_entry, args=(engine, remove_button_idx, table_name), disabled=df_change.shape[0]!=0 and remove_button_idx is not None)
        def reset():
            st.session_state.key += 1

        st.button("Сброс", key=f'reset-{table_name}', on_click=reset, disabled=df_change.shape[0]==0)


TABLES = {"masters", "cars", "services"}
def render_tables():
    for table_name in TABLES:
        render_table_default(engine, table_name)
