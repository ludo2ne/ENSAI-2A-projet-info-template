import pandas as pd
import streamlit as st

from utils.api_client import api_client
from utils.log_init import get_page_logger

logger = get_page_logger("player_stats")

st.set_page_config(
    page_title="Coin Flip Game - Player Stats",
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

[data-testid="stDataFrame"] {
    border: 1px solid #555;
    background: white;
}

[data-testid="stDataFrame"] * {
    font-family: "Times New Roman", serif !important;
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

<h1>Player Stats</h1>

<p style="text-align:center;">
    <b>Coin Flip Game - Player Information</b>
</p>

<p>
    <span class="new">NEW!</span>
    View player information and game history.
</p>

</div>
""",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# PLAYER ID
# ---------------------------------------------------------------------------

query_params = st.query_params
player_id = query_params.get("id_player")

logger.info(f"Player {player_id} stats")


if player_id is not None:
    try:
        player_id = int(player_id)

        player_res = api_client.get(f"/player/{player_id}")

        if player_res["status_code"] == 200:
            player = player_res["data"]

            logger.info(f"Successfully retrieved profile for: {player['username']}")

            # ----------------------------------------------------------------
            # PROFILE
            # ----------------------------------------------------------------

            st.markdown(
                f"""
<div class="retro">

<h2>Player Profile</h2>

<p style="text-align:center;">
    <b>👤 {player["username"]}</b>
</p>

<hr>

""",
                unsafe_allow_html=True,
            )

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Elo Rating", player["elo"])

            with col2:
                st.write(f"**Email:** {player['email']}")
                st.write(f"**Pokemon Fan:** {'Yes' if player['pokemon_fan'] else 'No'}")
                st.checkbox(
                    "Pokemon Fan",
                    value=player["pokemon_fan"],
                    disabled=True,
                )

            st.markdown(
                """
</div>
""",
                unsafe_allow_html=True,
            )

            # ----------------------------------------------------------------
            # GAMES PLAYED
            # ----------------------------------------------------------------

            st.markdown(
                """
<div class="retro">

<h2>Game History</h2>

<p>
    Games played by this player:
</p>

""",
                unsafe_allow_html=True,
            )

            logger.info(f"Fetching match history for player: {player['username']}")

            games_res = api_client.get(f"/game?id_player={player_id}")

            if games_res["status_code"] == 200:
                games_list = games_res["data"]

                logger.info(f"Found {len(games_list)} games for player {player_id}")

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

                        row = {
                            "Mode": g["game_mode"],
                            "Opponent": (f"{opponent['username']} ({opponent['elo']})"),
                            "Result": result,
                            "Date": g["timestamp"],
                        }

                        rows_for_df.append(row)

                    df = pd.DataFrame(rows_for_df)

                    st.dataframe(
                        df,
                        use_container_width=True,
                        hide_index=True,
                    )

            else:
                logger.error(f"Failed to fetch games. Status: {games_res['status_code']}")
                st.error("Could not fetch games history.")

            st.markdown(
                """
</div>
""",
                unsafe_allow_html=True,
            )

        else:
            logger.warning(f"Player not found. Status: {player_res['status_code']}")
            st.error(f"Player not found (Status: {player_res['status_code']})")

    except ValueError:
        logger.error(f"Invalid ID format: {player_id}")
        st.error("Invalid Player ID format in URL.")

    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        st.error(f"An error occurred: {e}")

else:
    st.warning("No player selected. Please go back to the player list.")


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
