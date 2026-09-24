"""
Streamlit home page - 1990s Web Edition.
"""

import streamlit as st

from utils.api_client import api_client
from utils.log_init import get_page_logger

logger = get_page_logger("home")

if "player" in st.session_state:
    st.switch_page("pages/player_menu.py")

if "visitor_registered" not in st.session_state:
    try:
        response = api_client.post("/visitor")
        if response and response.get("status_code") == 200:
            st.session_state["visitor_count"] = response["data"]["visitor_count"]

        st.session_state["visitor_registered"] = True

    except Exception as e:
        logger.exception(f"Critical error during API call: {str(e)}")
        st.error(f"Connection error: {str(e)}")


st.set_page_config(
    page_title="Coin Flip Game",
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

.stTextInput label {
    color: black !important;
    font-family: "Times New Roman", serif !important;
}

.stTextInput input {
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

<h1>Welcome to Coin Flip Game!</h1>

<p style="text-align:center;">
    <b>One game. Two players. 50% chance of winning.</b>
</p>

<p style="text-align:center;">
    Welcome to our online coin flipping service.
</p>

<hr>

<p>
    <span class="new">NEW!</span>
    Our coin flip game is now online!
</p>

<p>
    Play against other players and try your luck.
    <a href="#">What's new?</a>
</p>

<hr>

<h2>Member Login</h2>

<p>
    Please enter your username and password below.
</p>

</div>
""",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# LOGIN
# ---------------------------------------------------------------------------

username = st.text_input(
    "Username",
    placeholder="your username",
)

password = st.text_input(
    "Password",
    type="password",
    placeholder="your password",
)

if st.button("Log in", use_container_width=True):
    logger.info(f"Attempting login for user: {username}")

    try:
        response = api_client.post(
            "/login",
            json={
                "username": username,
                "password": password,
            },
        )

        if response:
            status_code = response.get("status_code")
            data = response.get("data")

            if status_code == 200:
                logger.info(f"User {username} successfully logged in.")

                player = data
                st.session_state["player"] = player
                st.session_state["access_token"] = player["access_token"]

                st.success(f"Welcome {player['username']}!")
                st.switch_page("pages/player_menu.py")

            elif status_code == 401:
                logger.warning(f"Login failed: 401 Unauthorized for user {username}.")
                st.error("Invalid username or password.")

            else:
                logger.error(f"Login failed: Status {status_code}, Data: {data}")
                st.error("Server error. Please try again later.")

        else:
            logger.error("API returned None or empty response")
            st.error("No response from server.")

    except Exception as e:
        logger.exception(f"Critical error during API call: {str(e)}")
        st.error(f"Connection error: {str(e)}")


# ---------------------------------------------------------------------------
# SIGN UP
# ---------------------------------------------------------------------------

st.markdown(
    """
<div class="retro">

<hr>

<h2>New Users</h2>

<p>
    Don't have an account yet?
</p>

</div>
""",
    unsafe_allow_html=True,
)

if st.button("Create a new account", use_container_width=True):
    st.switch_page("pages/create_player.py")


# ---------------------------------------------------------------------------
# OLD WEB GIMMICKS
# ---------------------------------------------------------------------------


visitor_count = st.session_state.get("visitor_count")

st.markdown(
    f"""
<hr>

<p class="center">
    You are visitor #{visitor_count}
</p>

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
