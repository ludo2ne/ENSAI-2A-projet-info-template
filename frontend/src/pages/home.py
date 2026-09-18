"""
Streamlit home page - Windows 98 Edition.

Provides options to log in, sign up for a new account, or reset the database.

Endpoints used:
    POST /login
    GET /reset_database
"""

import streamlit as st

from utils.api_client import api_client
from utils.log_init import get_page_logger

if "player" in st.session_state:
    st.switch_page("pages/player_menu.py")

st.set_page_config(page_title="Coin flip game", page_icon="🪙", layout="centered")

# --- WINDOWS 98 CSS ---
st.markdown(
    """
<style>
    /* Fond de l'application */
    .stApp {
        background-color: #008080; /* Le célèbre vert-bleu de Windows 98 */
    }

    /* Simulation d'une fenêtre Windows 98 */
    .win98-window {
        background-color: #c0c0c0;
        border: 2px solid;
        border-color: #ffffff #808080 #808080 #ffffff;
        padding: 10px;
        margin-bottom: 20px;
        box-shadow: 2px 2px 0px #000000;
    }

    /* Barre de titre */
    .win98-titlebar {
        background: linear-gradient(90deg, #000080, #1084d0);
        color: white;
        padding: 3px 10px;
        font-weight: bold;
        font-family: 'Tahoma', sans-serif;
        font-size: 14px;
        margin-bottom: 15px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    /* Stylisation des inputs et boutons pour l'effet "Inset" */
    .stTextInput input {
        background-color: #ffffff !important;
        border: 2px solid !important;
        border-color: #808080 #ffffff #ffffff #808080 !important;
        border-radius: 0px !important;
        color: black !important;
    }

    /* Boutons style Windows 98 */
    .stButton button {
        background-color: #c0c0c0 !important;
        color: black !important;
        border: 2px solid !important;
        border-color: #ffffff #808080 #808080 #ffffff !important;
        border-radius: 0px !important;
        padding: 5px 20px !important;
        font-family: 'Tahoma', sans-serif !important;
        text-transform: none !important;
        box-shadow: 1px 1px 0px #000000 !important;
    }

    .stButton button:active {
        border-color: #808080 #ffffff #ffffff #808080 !important;
        box-shadow: none !important;
    }

    /* Suppression des marges inutiles de Streamlit */
    [data-testid="stVerticalBlock"] > div:has(div.stTextInput) {
        background-color: #c0c0c0;
        padding: 20px;
        border: 2px solid;
        border-color: #ffffff #808080 #808080 #ffffff;
    }
    
    h1 {
        font-family: 'Tahoma', sans-serif;
        color: black !important;
        text-shadow: 1px 1px #ffffff;
    }
</style>
""",
    unsafe_allow_html=True,
)

# --- UI CONTENT ---

# Titre principal style rétro
st.markdown('<h1 style="text-align:center;">🪙 Coin Flip Game v1.0</h1>', unsafe_allow_html=True)

logger = get_page_logger("home")

# Fenêtre de Login
st.markdown(
    """
    <div class="win98-window">
        <div class="win98-titlebar">
            <span>Login</span>
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

# On utilise un container pour grouper les inputs dans la "fenêtre"
with st.container():
    username = st.text_input("Username", placeholder="Enter username")
    password = st.text_input("Password", type="password", placeholder="Enter password")

    if st.button("Log in", use_container_width=True):
        logger.info(f"Attempting login for user: {username}")

        try:
            response = api_client.post("/login", json={"username": username, "password": password})

            if response:
                status_code = response.get("status_code")
                data = response.get("data")

                if status_code == 200:
                    logger.info(f"User {username} successfully logged in.")
                    player = data
                    st.session_state["player"] = player
                    st.session_state["access_token"] = player["access_token"]
                    st.success(f"Welcome {player['username']} ! 🎉")
                    st.switch_page("pages/player_menu.py")
                elif status_code == 401:
                    logger.warning(f"Login failed: 401 Unauthorized for user {username}.")
                    st.error("Invalid credentials")
                else:
                    logger.error(f"Login failed: Status {status_code}, Data: {data}")
                    st.error("Server error, see logs.")
            else:
                logger.error("API returned None or empty response")
                st.error("No response from server.")

        except Exception as e:
            logger.exception(f"Critical error during API call: {str(e)}")
            st.error(f"Connection error: {str(e)}")

st.write("---")

if st.button("Sign Up", use_container_width=True):
    st.switch_page("pages/create_player.py")
