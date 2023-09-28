import pandas as pd
from pandas.testing import assert_frame_equal

import streamlit as st
from st_aggrid import AgGrid
from streamlit_modal import Modal

import tomli
from sqlalchemy import create_engine 

def read_connection_string(secrets_toml: str = "secrets.toml", db_name: str = "car_service_db") -> dict:
    """Parses secrets.toml file and returns connection string for sqlalchemy"""
    with open("secrets.toml", "rb") as f:
        data = tomli.load(f)
    return data["connections"][db_name]["url"]

engine = create_engine(read_connection_string(), echo=False)

def show_modal(modal, df_change: pd.DataFrame, table_name): 
    with modal.container():
        st.markdown(f"{df_change=}")


def apply_modifications(engine, table_name: str, change_df: pd.DataFrame):
    """Apply modifications made in df"""
    assert change_df.shape[0] == 0


def render_table_default(engine, table_name: str):
    with st.expander(table_name.capitalize()):
        st.markdown("Для редактирования таблицы, нажмите дважды на ее ячейку")
        df = pd.read_sql(table_name, con=engine)
        edited_df = st.data_editor(
            df.copy(), 
            hide_index=True, 
            disabled=['id',]
        )
        df_change = edited_df[~edited_df.isin(df).all(axis=1)]
        if df_change.shape[0] != 0:
            st.markdown(f"*Изменения в {df_change.shape[0]} строчках...*")
            st.dataframe(df_change, hide_index=True)
        st.button("Применить изменения",key=f'apply-{table_name}', on_click=apply_modifications, args=(engine, table_name, df_change), disabled=df_change.shape[0]==0)


TABLES = {"masters", "cars", "services"}
def render_tables():
    for table_name in TABLES:
        render_table_default(engine, table_name)
