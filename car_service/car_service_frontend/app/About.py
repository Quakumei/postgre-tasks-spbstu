import streamlit as st

from auth.StreamlitAuth import login_if_not_authorized
from pages.renders.render_about import render_about

from PIL import Image

st.title("car_service")
st.markdown("---")
st.image(Image.open("app/pages/resources/car_service_banner.jpg"))
st.markdown("---")
is_authorized = login_if_not_authorized()
if is_authorized:
    st.markdown("Используйте элементы меню слева (в сайдбаре) для обзора приложения")
st.markdown("---")
render_about()

