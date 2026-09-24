"""
Streamlit page for playing a coin flip game.

Allows a player to select an opponent and play a game of Heads or Tails.

Endpoints used:
    GET /player
    POST /game
"""

import time

import streamlit as st

from utils.api_client import api_client
from utils.auth_guard import check_authentification
from utils.log_init import get_page_logger

logger = get_page_logger("play_game")

st.set_page_config(
    page_title="Coin Flip Game - Play",
    page_icon="🪙",
    layout="centered",
)

# ---------------------------------------------------------------------------
# AUTHENTICATION
# ---------------------------------------------------------------------------

check_authentification()

player = st.session_state.get("player")


# ---------------------------------------------------------------------------
# 1990s WEB STYLE
# ---------------------------------------------------------------------------

st.markdown(
    """
<style>
.stApp {
    background: #d8d6e5;
    color: black;
    font-family: "Times New Roman", serif;
}

.block-container {
    max-width: 760px;
    padding-top: 25px;
}

.retro {
    background: #eeeeee;
    border: 1px solid #555;
    padding: 15px 25px;
    box-shadow: 3px 3px #888;
}

h1 {
    font-family: "Times New Roman", serif !important;
    text-align: center;
    color: black !important;
}

h2 {
    font-size: 20px !important;
    color: #0000ee !important;
    text-decoration: underline;
}

a {
    color: #0000ee;
}

.stSelectbox label,
.stRadio label {
    color: black !important;
    font-family: "Times New Roman", serif !important;
}

.stSelectbox div,
.stRadio div {
    font-family: "Times New Roman", serif !important;
}

.stButton button {
    background: #d4d0c8 !important;
    color: black !important;
    border: 2px outset #fff !important;
    border-radius: 0 !important;
    box-shadow: none !important;
    font-family: "Times New Roman", serif !important;
    font-weight: bold !important;
}

.stButton button:active {
    border-style: inset !important;
}

.stAlert {
    border-radius: 0 !important;
}

.small {
    font-size: 12px;
}

.center {
    text-align: center;
}

.new {
    color: red;
    font-weight: bold;
}
</style>
""",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# PAGE HEADER
# ---------------------------------------------------------------------------

st.markdown(
    """
<div class="retro">

<h1>Play a Coin Flip</h1>

<p style="text-align:center;">
    <b>Heads or Tails?</b>
</p>

<p style="text-align:center;">
    Challenge another player and try your luck!
</p>

<hr>

<p>
    <span class="new">NEW!</span>
    Our online coin flip game is ready to play.
</p>

<h2>Choose Your Opponent</h2>

<p>
    Select a player from the list below.
</p>

</div>
""",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# LOAD PLAYERS
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# GAME FORM
# ---------------------------------------------------------------------------

opponent = st.selectbox(
    "Choose an opponent",
    opponents,
    format_func=lambda j: j["username"],
)

bet = st.radio(
    "Heads or Tails",
    ["heads", "tails"],
)


# ---------------------------------------------------------------------------
# PLAY
# ---------------------------------------------------------------------------

if st.button("Play"):
    logger.info("Play a game")

    with st.spinner("Wait for it..."):
        time.sleep(1)

    response = api_client.post(
        "/game/",
        json={
            "id_opponent": opponent["id_player"],
            "game_mode": "coinflip",
            "params": {"choice": bet},
        },
    )

    if response["status_code"] != 200:
        st.error(response["data"])
        st.stop()

    data = response["data"]

    st.markdown(
        """
<hr>

<div class="retro">

<h2>Game Result</h2>

""",
        unsafe_allow_html=True,
    )

    st.write(f"Result: **{data['description']}**")

    if data["winner"] == player["username"]:
        st.success(
            f"""🎉 **You win!**

Your new Elo rating is {data["new_elo1"]}"""
        )
        st.balloons()

    elif data["winner"] == opponent["username"]:
        st.warning(
            f"""😢 **You lose**

Your new Elo rating is {data["new_elo1"]}"""
        )

    else:
        st.info("Draw, no change in Elo rating")

    st.markdown(
        """
</div>
""",
        unsafe_allow_html=True,
    )

    logger.info("Game is over")


# ---------------------------------------------------------------------------
# NAVIGATION
# ---------------------------------------------------------------------------

st.markdown(
    """
<hr>

<p class="center">
    <b>Finished playing?</b>
</p>
""",
    unsafe_allow_html=True,
)

if st.button("Back to menu", type="primary"):
    st.switch_page("pages/player_menu.py")


# ---------------------------------------------------------------------------
# OLD WEB GIMMICKS
# ---------------------------------------------------------------------------

st.markdown(
    """
<hr>

<p class="center small">
    <a href="/404">Guestbook</a>
    &nbsp; | &nbsp;
    <a href="/404">About this site</a>
    &nbsp; | &nbsp;
    <a href="/404">What's new?</a>
</p>

<p class="center small">
    Best viewed with Netscape Navigator 3.0
    <br>
    Last updated: September 24, 1996
</p>
""",
    unsafe_allow_html=True,
)
