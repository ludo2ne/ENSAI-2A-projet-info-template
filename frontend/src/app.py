import streamlit as st

from utils.log_init import initialiser_logs

initialiser_logs("Streamlit App")

if "joueur" in st.session_state:
    st.switch_page("pages/menu_page.py")
else:
    st.switch_page("pages/main_page.py")
