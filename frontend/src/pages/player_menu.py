import streamlit as st

from utils.auth_guard import check_authentification
from utils.log_init import get_page_logger

st.set_page_config(page_title="Main Menu", page_icon="🎮")

# --- WINDOWS 98 CSS ---
st.markdown(
    """
<style>
    .stApp { background-color: #008080; }
    .win98-window {
        background-color: #c0c0c0;
        border: 2px solid;
        border-color: #ffffff #808080 #808080 #ffffff;
        padding: 15px;
        box-shadow: 2px 2px 0px #000000;
    }
    .win98-titlebar {
        background: linear-gradient(90deg, #000080, #1084d0);
        color: white;
        padding: 3px 10px;
        font-family: 'Tahoma', sans-serif;
        font-weight: bold;
        margin-bottom: 15px;
    }
    .stButton button {
        background-color: #c0c0c0 !important;
        color: black !important;
        border: 2px solid !important;
        border-color: #ffffff #808080 #808080 #ffffff !important;
        border-radius: 0px !important;
        width: 100%;
        font-family: 'Tahoma', sans-serif !important;
        box-shadow: 1px 1px 0px #000000 !important;
    }
    .stButton button:active {
        border-color: #808080 #ffffff #ffffff #808080 !important;
    }
    h1 { font-family: 'Tahoma', sans-serif; color: white; text-shadow: 2px 2px #000000; }
</style>
""",
    unsafe_allow_html=True,
)

logger = get_page_logger("player_menu")
check_authentification()
player = st.session_state.get("player")

st.title("Main Menu")

# Simulation de fenêtre
st.markdown(
    '<div class="win98-window"><div class="win98-titlebar">Player_Menu</div>',
    unsafe_allow_html=True,
)

st.write(f"**User:** `{player['username']}`")
st.info("Select an action from the list below:")

if st.button("📋 List all players"):
    st.switch_page("pages/list_players.py")

if st.button("🪙 Play Coin Flip"):
    st.switch_page("pages/play_coinflip.py")

if st.button("🎲 Play Dice Game"):
    st.switch_page("pages/play_dice.py")

st.markdown("---")

if st.button("🚪 Log out", type="primary"):
    logger.info("Log out")
    del st.session_state["player"]
    st.switch_page("pages/home.py")

st.markdown("</div>", unsafe_allow_html=True)
