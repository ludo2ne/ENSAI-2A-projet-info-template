import os

import streamlit as st

from utils.api_client import api_client
from utils.log_init import get_page_logger

st.set_page_config(page_title="Registration", page_icon="📝")

# --- WINDOWS 98 CSS ---
st.markdown(
    """
<style>
    .stApp { background-color: #008080; }
    .win98-window {
        background-color: #c0c0c0;
        border: 2px solid;
        border-color: #ffffff #808080 #808080 #ffffff;
        padding: 20px;
    }
    .win98-titlebar {
        background: linear-gradient(90deg, #000080, #1084d0);
        color: white;
        padding: 3px 10px;
        font-family: 'Tahoma', sans-serif;
        font-weight: bold;
        margin-bottom: 20px;
    }
    /* Inset effect for inputs */
    .stTextInput input, .stNumberInput input, .stSelectbox div {
        background-color: white !important;
        border: 2px solid !important;
        border-color: #808080 #ffffff #ffffff #808080 !important;
        border-radius: 0px !important;
    }
    .stButton button {
        background-color: #c0c0c0 !important;
        border: 2px solid !important;
        border-color: #ffffff #808080 #808080 #ffffff !important;
        border-radius: 0px !important;
        font-family: 'Tahoma', sans-serif !important;
        box-shadow: 1px 1px 0px #000000 !important;
    }
</style>
""",
    unsafe_allow_html=True,
)

st.title("User Registration")
logger = get_page_logger("create_player")

st.markdown(
    '<div class="win98-window"><div class="win98-titlebar">Setup Wizard - New Account</div>',
    unsafe_allow_html=True,
)

username = st.text_input("Username", max_chars=30)
password = st.text_input("Password", type="password")

password_min_length = int(os.environ.get("PASSWORD_MIN_LENGTH", 6))
is_pwd_long_enough = len(password) >= password_min_length
st.write("✅" if is_pwd_long_enough else "❌", f"At least {password_min_length} characters")

elo = st.number_input("Elo", min_value=1000, max_value=3000)
email = st.text_input("Email")
pokemon_fan = st.checkbox("Pokemons fan?")

if st.button(
    "Create Account", use_container_width=True, disabled=not username or not is_pwd_long_enough
):
    logger.info("Create a player")
    player = {
        "username": username,
        "password": password,
        "elo": elo,
        "email": email,
        "pokemon_fan": pokemon_fan,
    }

    response = api_client.post("/player/", json=player)

    if response:
        if response["status_code"] == 200:
            st.success(f"Player {username} successfully created! 🎉")
        else:
            st.error(f"Error: {response['data']}")

st.markdown("</div>", unsafe_allow_html=True)

if st.button("Back to homepage"):
    st.switch_page("pages/home.py")
