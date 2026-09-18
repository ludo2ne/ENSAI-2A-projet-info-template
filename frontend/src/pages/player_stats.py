import pandas as pd
import streamlit as st

from utils.api_client import api_client
from utils.log_init import get_page_logger

st.set_page_config(page_title="Player Stats", page_icon="📊")

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
    h1 { font-family: 'Tahoma', sans-serif; color: white; text-shadow: 2px 2px #000000; }
    h3 { font-family: 'Tahoma', sans-serif; color: black; margin-top: 0; }
    
    /* Style pour le dataframe (aspect gris/blanc classique) */
    [data-testid="stDataFrame"] {
        border: 2px solid #808080;
    }
</style>
""",
    unsafe_allow_html=True,
)

st.title("📊 Player Statistics")
logger = get_page_logger("player_stats")
query_params = st.query_params
player_id = query_params.get("id_player")

if player_id is not None:
    try:
        player_id = int(player_id)
        player_res = api_client.get(f"/player/{player_id}")

        if player_res["status_code"] == 200:
            player = player_res["data"]

            # --- SECTION PROFIL ---
            st.markdown(
                '<div class="win98-window"><div class="win98-titlebar">Profile_View</div>',
                unsafe_allow_html=True,
            )
            st.subheader(f"👤 {player['username']}")

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Elo Rating", player["elo"])
            with col2:
                st.write(f"**Email:** {player['email']}")
                st.write(f"**Pokemon Fan:** {'Yes' if player['pokemon_fan'] else 'No'}")
            st.markdown("</div>", unsafe_allow_html=True)

            # --- SECTION HISTORIQUE ---
            st.markdown(
                '<div class="win98-window"><div class="win98-titlebar">Match_History.log</div>',
                unsafe_allow_html=True,
            )
            st.subheader("Game History")

            games_res = api_client.get(f"/game?id_player={player_id}")

            if games_res["status_code"] == 200:
                games_list = games_res["data"]
                if not games_list:
                    st.info("No games played yet.")
                else:
                    rows_for_df = []
                    for g in games_list:
                        opponent = (
                            g["player2"] if g["player1"]["id_player"] == player_id else g["player1"]
                        )
                        match g["winner"]:
                            case None:
                                result = "Draw"
                            case w if w["id_player"] == player_id:
                                result = "Win"
                            case _:
                                result = "Loss"
                        rows_for_df.append({
                            "Mode": g["game_mode"],
                            "Opponent": f"{opponent['username']} ({opponent['elo']})",
                            "Result": result,
                            "Date": g["timestamp"],
                        })
                    df = pd.DataFrame(rows_for_df)
                    st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.error("Could not fetch games history.")
            st.markdown("</div>", unsafe_allow_html=True)

        else:
            st.error("Player not found.")

    except Exception as e:
        st.error(f"An error occurred: {e}")
else:
    st.warning("No player selected.")
