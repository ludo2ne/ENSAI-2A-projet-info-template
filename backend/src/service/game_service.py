import random

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

        resultat = random.choice(["heads", "tails"])
        gagnant = j1 if resultat == choice else j2

        return {
            "joueur1": j1.pseudo,
            "joueur2": j2.pseudo,
            "resultat": resultat,
            "gagnant": gagnant.pseudo,
        }
