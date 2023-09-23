import streamlit as st

from auth.StreamlitAuth import login_if_not_authorized
from pages.renders.render_tables import render_tables

is_authorized = login_if_not_authorized()
st.title("Справочники")

if is_authorized:
    render_tables()
else:
    st.markdown("Пожалуйста, авторизируйтесь, прежде чем использовать приложение")
