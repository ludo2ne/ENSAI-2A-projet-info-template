import time

import streamlit as st

from utils.api_client import api_client
from utils.auth_guard import check_authentification
from utils.log_init import get_page_logger

st.set_page_config(page_title="Dice Game", page_icon="🎲")

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
        margin-bottom: 20px;
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
        font-family: 'Tahoma', sans-serif !important;
        box-shadow: 1px 1px 0px #000000 !important;
    }
    h1 { font-family: 'Tahoma', sans-serif; color: white; text-shadow: 2px 2px #000000; }
</style>
""",
    unsafe_allow_html=True,
)

st.title("🎲 Play a Dice Game")
logger = get_page_logger("play_dice")
check_authentification()
player = st.session_state.get("player")

# Fetch available players
response = api_client.get("/player/")

if response["status_code"] != 200:
    st.error("Error loading players")
    st.stop()

players = response["data"]
opponents = [
    j for j in players if j["id_player"] != player["id_player"] and j["username"] != "admin"
]

if not opponents:
    st.warning("No opponents available")
    st.stop()

# UI layout with Windows 98 style
st.markdown(
    '<div class="win98-window"><div class="win98-titlebar">Dice_Game_Setup</div>',
    unsafe_allow_html=True,
)

opponent = st.selectbox("Choose an opponent", opponents, format_func=lambda j: j["username"])

if st.button("Roll the Dice", use_container_width=True):
    logger.info("Playing a dice game")
    with st.spinner("Rolling the dice..."):
        time.sleep(1)

    response = api_client.post(
        "/game/",
        json={
            "id_opponent": opponent["id_player"],
            "game_mode": "dice",
        },
    )

    if response["status_code"] != 200:
        st.error(response["data"])
        st.stop()

    data = response["data"]
    st.write(f"**{data['description']}**")

    if data["winner"] == player["username"]:
        st.success(f"🎉 **You win!**\n\nNew Elo: {data['new_elo1']}")
        st.balloons()
    elif data["winner"] == opponent["username"]:
        st.warning(f"😢 **You lose**\n\nNew Elo: {data['new_elo1']}")
    else:
        st.info("Draw, no change in Elo rating")

    logger.info("Dice game is over")

st.markdown("</div>", unsafe_allow_html=True)

if st.button("Back to menu"):
    st.switch_page("pages/player_menu.py")
