"""
Streamlit page for player account registration.

Allows users to create a new player profile with username, password, Elo, email, etc.

Endpoint used:
    POST /player
"""

import os

import streamlit as st

from utils.api_client import api_client
from utils.log_init import get_page_logger

logger = get_page_logger("create_player")

st.set_page_config(
    page_title="Coin Flip Game - New Player",
    page_icon="🪙",
    layout="centered",
)

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

.stTextInput label,
.stNumberInput label,
.stCheckbox label {
    color: black !important;
    font-family: "Times New Roman", serif !important;
}

.stTextInput input,
.stNumberInput input {
    border: 1px solid #555 !important;
    border-radius: 0 !important;
    background: white !important;
    color: black !important;
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

<h1>Create a Player Account</h1>

<p style="text-align:center;">
    <b>Welcome to the Coin Flip Game!</b>
</p>

<p style="text-align:center;">
    Create your player account and start playing online.
</p>

<hr>

<p>
    <span class="new">NEW!</span>
    Registration is quick and easy.
</p>

<h2>New Player Registration</h2>

<p>
    Please fill in the information below to create your account.
</p>

</div>
""",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# REGISTRATION FORM
# ---------------------------------------------------------------------------

username = st.text_input(
    "Username",
    max_chars=30,
)

password = st.text_input(
    "Password (e.g. 123456)",
    type="password",
)

password_min_length = int(os.getenv("PASSWORD_MIN_LENGTH", 12))
is_pwd_long_enough = len(password) >= password_min_length

st.write(
    "✅" if is_pwd_long_enough else "❌",
    f"At least {password_min_length} characters",
)

elo = st.number_input(
    "Elo",
    min_value=1000,
    max_value=3000,
)

email = st.text_input("Email (e.g. mamy.zinzin@club-internet.fr)")

pokemon_fan = st.checkbox("Pokemons fan?")


# ---------------------------------------------------------------------------
# CREATE ACCOUNT
# ---------------------------------------------------------------------------

with st.container(horizontal_alignment="center"):
    if st.button(
        "Create",
        width=150,
        disabled=not username or not is_pwd_long_enough,
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
                logger.info("Player created successfully")
            else:
                st.error(f"Error: {response['data']}")
                logger.info("Error while creating player")


# ---------------------------------------------------------------------------
# NAVIGATION
# ---------------------------------------------------------------------------

st.markdown(
    """
<hr>

<p class="center">
    Already have an account?
</p>
""",
    unsafe_allow_html=True,
)

if st.button("Back to homepage", type="primary"):
    st.switch_page("pages/home.py")


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
