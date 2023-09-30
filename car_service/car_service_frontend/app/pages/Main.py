import streamlit as st

from auth.StreamlitAuth import login_if_not_authorized
from pages.renders.render_main import render_main

is_authorized = login_if_not_authorized()
st.title("Главная")

if is_authorized:
    render_main()
else:
    st.markdown("Пожалуйста, авторизируйтесь, прежде чем использовать приложение")
