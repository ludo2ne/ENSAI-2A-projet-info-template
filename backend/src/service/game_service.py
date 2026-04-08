import os
import secrets

from fastapi import HTTPException

from dao.player_dao import PlayerDao
from utils.log_decorator import log


class GameService:
    @log
    def play(self, player_id: int, opponent_id: int, choice="heads"):
        if player_id == opponent_id:
            raise HTTPException(status_code=400, detail="Two different players required")

        p1 = PlayerDao().find_by_id(player_id)
        p2 = PlayerDao().find_by_id(opponent_id)

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
        return 1 / (1 + 10 ** ((elo2 - elo1) / 400))

    def compute_elo(self, elo1, elo2, win1):

        K_FACTOR = int(os.environ["ELO_K_FACTOR"])

        s1, s2 = win1 * 1, 1 - win1 * 1

        new_elo1 = round(elo1 + K_FACTOR * (s1 - self.expected_score(elo1, elo2)))
        new_elo2 = round(elo2 + K_FACTOR * (s2 - self.expected_score(elo2, elo1)))

        return new_elo1, new_elo2

    def update_elo(self, p1, p2, winner):
        p1.elo, p2.elo = self.compute_elo(p1.elo, p2.elo, p1 == winner)

        PlayerDao().update(p1)
        PlayerDao().update(p2)
