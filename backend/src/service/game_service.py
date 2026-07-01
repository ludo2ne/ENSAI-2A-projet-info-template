import os
import secrets

from fastapi import HTTPException

from dao.player_dao import PlayerDao
from utils.log_utils import log


class GameService:
    """Service that manages games."""

    @log
    def play(self, id_player: int, id_opponent: int, choice="heads"):
        """Executes a single round of a coin-flip game between two players.
        Args:
            id_player (int): The unique identifier of the first player.
            id_opponent (int): The unique identifier of the opponent.
            choice (str, optional): The player's choice ('heads' or 'tails'). Defaults to "heads".
        Returns:
            dict: A dictionary containing the match details and new elo
        Raises:
            HTTPException: 400 if the two players are the same.
            HTTPException: 404 if one or both players are not found in the database.
        """
        if id_player == id_opponent:
            raise HTTPException(status_code=400, detail="Two different players required")

        p1 = PlayerDao().find_by_id(id_player)
        p2 = PlayerDao().find_by_id(id_opponent)

        if not p1 or not p2:
            raise HTTPException(status_code=404, detail="Player not found")

        result = secrets.choice(["heads", "tails"])
        winner = p1 if result == choice else p2

        self.update_elo(p1, p2, winner)

        return {
            "player1": p1.username,
            "player2": p2.username,
            "result": result,
            "winner": winner.username,
            "new_elo1": p1.elo,
            "new_elo2": p2.elo,
        }

    def expected_score(self, elo1, elo2):
        """Calculates the expected score (probability of winning) using the Elo formula.
        Args:
            elo1 (float): The current Elo rating of player 1.
            elo2 (float): The current Elo rating of player 2.

        Returns:
            float: The expected score for player 1 (between 0 and 1).
        """
        return 1 / (1 + 10 ** ((elo2 - elo1) / 400))

    def compute_elo(self, elo1, elo2, win1):
        """Computes the new Elo ratings for two players after a match.
        Args:
            elo1 (int): Current Elo of player 1.
            elo2 (int): Current Elo of player 2.
            win1 (bool): True if player 1 won, False if player 2 won.
        Returns:
            tuple[int, int]: A tuple containing (new_elo1, new_elo2).
        """
        K_FACTOR = int(os.environ["ELO_K_FACTOR"])

        s1, s2 = win1 * 1, 1 - win1 * 1

        new_elo1 = round(elo1 + K_FACTOR * (s1 - self.expected_score(elo1, elo2)))
        new_elo2 = round(elo2 + K_FACTOR * (s2 - self.expected_score(elo2, elo1)))

        return new_elo1, new_elo2

    def update_elo(self, player1, player2, winner):
        """Calculates and persists the new Elo ratings for both players.
        Args:
            player1 (Player): The first Player object.
            player2 (Player): The second Player object.
            winner (Player): The Player who won the match.
        """

        player1.elo, player2.elo = self.compute_elo(player1.elo, player2.elo, player1 == winner)

        PlayerDao().update(player1)
        PlayerDao().update(player2)
