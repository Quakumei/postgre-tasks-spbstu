import streamlit as st

from auth.StreamlitAuth import login_if_not_authorized, get_access_level
from pages.renders.render_tables import render_tables

is_authorized = login_if_not_authorized()
st.title("Справочники")

if is_authorized:
    if get_access_level(st.session_state['username']) != 'admin':
        st.warning("У вас недостаточно прав, чтобы просматривать эту страницу")
    else:
        render_tables()
else:
    st.markdown("Пожалуйста, авторизируйтесь, прежде чем использовать приложение")
