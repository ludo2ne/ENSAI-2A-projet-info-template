import pandas as pd
import streamlit as st

from utils.api_client import api_client
from utils.auth_guard import check_authentification
from utils.log_init import get_page_logger

st.set_page_config(page_title="Player List", page_icon="👥")

# --- WINDOWS 98 CSS ---
st.markdown(
    """
<style>
    .stApp { background-color: #008080; }
    .win98-window {
        background-color: #c0c0c0;
        border: 2px solid;
        border-color: #ffffff #808080 #808080 #ffffff;
        padding: 10px;
    }
    .win98-titlebar {
        background: linear-gradient(90deg, #000080, #1084d0);
        color: white;
        padding: 3px 10px;
        font-family: 'Tahoma', sans-serif;
        font-weight: bold;
        margin-bottom: 10px;
    }
    /* Style pour le dataframe (on simule un aspect gris) */
    [data-testid="stDataFrame"] {
        border: 2px solid #808080;
        background-color: white;
    }
    .stButton button {
        background-color: #c0c0c0 !important;
        border: 2px solid !important;
        border-color: #ffffff #808080 #808080 #ffffff !important;
        border-radius: 0px !important;
        font-family: 'Tahoma', sans-serif !important;
    }
</style>
""",
    unsafe_allow_html=True,
)

logger = get_page_logger("list_players")
check_authentification()

st.title("Player Database")

st.markdown(
    '<div class="win98-window"><div class="win98-titlebar">Explorer - Players</div>',
    unsafe_allow_html=True,
)

players = api_client.get("/player").get("data")

if players:
    if isinstance(players, list):
        df = pd.DataFrame(players)
        df["url"] = df.apply(lambda row: f"/player_stats?id_player={row['id_player']}", axis=1)

        st.dataframe(
            df,
            column_config={
                "url": st.column_config.LinkColumn(label="Stats", display_text="📊"),
            },
            hide_index=True,
        )
    else:
        st.info("No players found.")
else:
    st.info("No players found.")

st.markdown("</div>", unsafe_allow_html=True)

st.write("")  # Spacer
if st.button("⬅️ Back to menu"):
    st.switch_page("pages/player_menu.py")
