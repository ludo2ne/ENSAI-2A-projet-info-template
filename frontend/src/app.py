import streamlit as st

if "joueur" in st.session_state:
    st.switch_page("pages/menu_page.py")
else:
    st.switch_page("pages/main_page.py")
