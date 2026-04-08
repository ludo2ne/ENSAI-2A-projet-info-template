import os
import secrets

from fastapi import HTTPException

from dao.joueur_dao import JoueurDao
from utils.log_decorator import log


class GameService:
    @log
    def play(self, player_id: int, opponent_id: int, choice="heads"):
        if player_id == opponent_id:
            raise HTTPException(status_code=400, detail="Deux joueurs différents requis")

        j1 = JoueurDao().trouver_par_id(player_id)
        j2 = JoueurDao().trouver_par_id(opponent_id)

        if not j1 or not j2:
            raise HTTPException(status_code=404, detail="Joueur non trouvé")

        resultat = secrets.choice(["heads", "tails"])
        winner = j1 if resultat == choice else j2

        self.update_elo(j1, j2, winner)

        return {
            "player1": j1.pseudo,
            "player2": j2.pseudo,
            "result": resultat,
            "winner": winner.pseudo,
            "new_elo1": j1.elo,
        }

    def expected_score(self, elo1, elo2):
        return 1 / (1 + 10 ** ((elo2 - elo1) / 400))

    def compute_elo(self, elo1, elo2, win1):

        K_FACTOR = int(os.environ["ELO_K_FACTOR"])

        e1 = self.expected_score(elo1, elo2)

        s1, s2 = win1 * 1, 1 - win1 * 1

        new_elo1 = round(elo1 + K_FACTOR * (s1 - e1))
        new_elo2 = round(elo2 + K_FACTOR * (s2 - (1 - e1)))

        return new_elo1, new_elo2

    def update_elo(self, j1, j2, winner):
        j1.elo, j2.elo = self.compute_elo(j1.elo, j2.elo, j1 == winner)

        JoueurDao().modifier(j1)
        JoueurDao().modifier(j2)
