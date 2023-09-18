import streamlit as st

conn = st.experimental_connection("sql")

def render_operator_console():
    st.title("Operator console")
    st.markdown("Current day works: ")

    
