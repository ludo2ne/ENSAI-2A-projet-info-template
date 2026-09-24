"""
Streamlit 404 error page - 1990s Web Edition.
"""

import streamlit as st

from utils.log_init import get_page_logger

logger = get_page_logger("404")

st.set_page_config(
    page_title="404 - Page Not Found",
    page_icon="❌",
    layout="centered",
)

logger.warning("404 page displayed")


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

.error-box {
    background: white;
    border: 3px double #555;
    padding: 20px;
    margin-top: 20px;
    text-align: center;
}

.error-code {
    font-family: "Courier New", monospace;
    font-size: 72px;
    font-weight: bold;
    color: #0000aa;
    margin: 5px 0;
}

.error-title {
    font-size: 28px;
    font-weight: bold;
    color: #aa0000;
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

.warning {
    color: #aa0000;
    font-weight: bold;
}
</style>
""",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# PAGE
# ---------------------------------------------------------------------------

st.markdown(
    """
<div class="retro">

<h1>Coin Flip Game</h1>

<hr>

<div class="error-box">

<div class="error-code">404</div>

<div class="error-title">
Page Not Found!
</div>

<p>
    <b>Oops! The page you requested could not be found.</b>
</p>

<p>
    The page may have been moved, deleted,
    or perhaps it never existed in the first place.
</p>

<hr>

<p>
    <span class="new">ERROR!</span>
    Our server looked everywhere...
</p>

<p>
    Unfortunately, there was nothing here.
</p>

</div>

<h2>What can you do?</h2>

<p>
    Please check the address you entered or return
    to the Coin Flip Game homepage.
</p>

</div>
""",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# NAVIGATION
# ---------------------------------------------------------------------------

if st.button("Back to homepage", use_container_width=True):
    st.switch_page("pages/home.py")


# ---------------------------------------------------------------------------
# OLD WEB GIMMICKS
# ---------------------------------------------------------------------------

st.markdown(
    """
<hr>

<p class="center">
    <span class="warning">
        *** ERROR 404 ***
    </span>
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
