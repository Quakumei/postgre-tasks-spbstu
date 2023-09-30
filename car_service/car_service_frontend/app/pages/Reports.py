import streamlit as st

from auth.StreamlitAuth import login_if_not_authorized
from pages.renders.render_reports import render_reports

is_authorized = login_if_not_authorized()
st.title("Отчёты")

if is_authorized:
    render_reports()
else:
    st.markdown("Пожалуйста, авторизируйтесь прежде чем использовать приложение")
