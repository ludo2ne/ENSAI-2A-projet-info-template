import os
import secrets

from fastapi import HTTPException

from dao.player_dao import PlayerDao
from utils.log_decorator import log


class GameService:
    """
    Service that manages game logic and calculates Elo ratings.
    """

    @log
    def play(self, id_player: int, id_opponent: int, choice="heads"):
        """
        Executes a single round of a coin-flip game between two players.

        Parameters
        ----------
        id_player : int
            The unique identifier of the first player.
        id_opponent : int
            The unique identifier of the opponent.
        choice : str, optional
            The player's choice ('heads' or 'tails'), by default "heads".

        Returns
        -------
        dict
            A dictionary containing the match details:
            - player1 (str): Username of the first player.
            - player2 (str): Username of the second player.
            - result (str): The winning side ('heads' or 'tails').
            - winner (str): Username of the winner.
            - new_elo1 (int): Updated Elo for player 1.
            - new_elo2 (int): Updated Elo for player 2.

        Raises
        ------
        HTTPException
            400 if the two players are the same.
            404 if one or both players are not found in the database.
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
        Parameters
        ----------
        elo1 : float
            The current Elo rating of player 1.
        elo2 : float
            The current Elo rating of player 2.

        Returns
        -------
        float
            The expected score for player 1 (between 0 and 1)."""
        return 1 / (1 + 10 ** ((elo2 - elo1) / 400))

    def compute_elo(self, elo1, elo2, win1):
        """Computates the new Elo ratings for two players after a match.

        Parameters
        ----------
        elo1 : int
            Current Elo of player 1.
        elo2 : int
            Current Elo of player 2.
        win1 : bool
            True if player 1 won, False if player 2 won.

        Returns
        -------
        tuple[int, int] containing (new_elo1, new_elo2)."""
        K_FACTOR = int(os.environ["ELO_K_FACTOR"])

        s1, s2 = win1 * 1, 1 - win1 * 1

        new_elo1 = round(elo1 + K_FACTOR * (s1 - self.expected_score(elo1, elo2)))
        new_elo2 = round(elo2 + K_FACTOR * (s2 - self.expected_score(elo2, elo1)))

        return new_elo1, new_elo2

    def update_elo(self, p1, p2, winner):
        """
        Calculates and persists the new Elo ratings for both players.
        Parameters
        ----------
        p1 : first Player object.
        p2 : second Player object.
        winner : Player who won the match."""

        p1.elo, p2.elo = self.compute_elo(p1.elo, p2.elo, p1 == winner)

        PlayerDao().update(p1)
        PlayerDao().update(p2)
