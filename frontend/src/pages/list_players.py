"""
Streamlit page for listing all players.

Retrieves and displays a list of registered players in a table, excluding sensitive data like passwords.

Endpoint used:
    GET /player
"""

import pandas as pd
import streamlit as st

from utils.api_client import api_client
from utils.auth_guard import check_authentification
from utils.log_init import get_page_logger

logger = get_page_logger("list_players")

st.set_page_config(
    page_title="Coin Flip Game - Players",
    page_icon="🪙",
    layout="centered",
)

# ---------------------------------------------------------------------------
# AUTHENTICATION
# ---------------------------------------------------------------------------

check_authentification()


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

/* Make the table look like an old HTML table */
[data-testid="stDataFrame"] {
    border: 1px solid #555;
    background: white;
}

[data-testid="stDataFrame"] * {
    font-family: "Times New Roman", serif !important;
}

.retro-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 2px;
    background: #808080;
    color: black;
    font-family: "Times New Roman", serif;
    font-size: 14px;
}

.retro-table th {
    background: #d4d0c8;
    color: black;
    font-weight: bold;
    padding: 5px 8px;
    border-top: 2px solid white;
    border-left: 2px solid white;
    border-right: 2px solid #404040;
    border-bottom: 2px solid #404040;
}

.retro-table td {
    background: white;
    color: black;
    padding: 5px 8px;
    border: 1px solid #808080;
}

.retro-table tr:nth-child(even) td {
    background: #eeeeee;
}

.retro-table a {
    color: #0000ee;
    text-decoration: underline;
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

<h1>Player List</h1>

<p style="text-align:center;">
    <b>Coin Flip Game - Registered Players</b>
</p>

<p>
    <span class="new">NEW!</span>
    Browse the list of players registered on our service.
</p>

<hr>

<h2>Our Players</h2>

<p>
    Here you can find all the players currently registered.
</p>

</div>
""",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# PLAYER LIST
# ---------------------------------------------------------------------------

players = api_client.get("/player").get("data")

if players:
    if isinstance(players, list):
        df = pd.DataFrame(players)

        df["Stats"] = df["id_player"].apply(
            lambda player_id: f'<a href="/player_stats?id_player={player_id}">📊 Stats</a>'
        )

        st.markdown(
            """
<div class="retro">
""",
            unsafe_allow_html=True,
        )

        st.markdown(
            df.to_html(
                index=False,
                columns=["username", "elo", "email", "pokemon_fan", "Stats"],
                classes="retro-table",
                escape=False,
            ),
            unsafe_allow_html=True,
        )

        st.markdown(
            """
</div>
""",
            unsafe_allow_html=True,
        )
    else:
        logger.info("No players found.")
        st.info("No players found.")


# ---------------------------------------------------------------------------
# NAVIGATION
# ---------------------------------------------------------------------------

st.markdown(
    """
<hr>

<p class="center">
    <b>Finished browsing?</b>
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
