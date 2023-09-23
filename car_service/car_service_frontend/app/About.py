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
    st.markdown("Now you are able to choose pages from the left menu and use them. Try it!")
st.markdown("---")
render_about()

