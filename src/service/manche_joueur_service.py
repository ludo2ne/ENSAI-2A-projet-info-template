"""Implémentation de la classe MancheJoeuurService"""

from business_object.joueur import Joueur
from dao.manche_joueur_dao import MancheJoueurDAO
from utils.log_decorator import log


class MancheJoueurService:
    """Gère le stockage des informations des joueurs dans une manche dans la base de données"""

    dao = MancheJoueurDAO()

    @log
    def sauvegarder_manche_joueur(self, id_manche: int, info_manche, gains = {}) -> bool:
        """Crée les participations des joueurs à une manche."""
        return MancheJoueurDAO().creer_manche_joueur(id_manche, info_manche, gains)

    def trouver_par_ids(self, id_manche: int, id_joueur: int) -> list[dict]:
        """Récupère les participations d’un joueur spécifique à une manche."""
        return MancheJoueurDAO().trouver_par_ids(id_manche, id_joueur)

    @log
    def supprimer_par_id_manche(self, id_manche: int) -> bool:
        """Supprime toutes les participations liées à une manche."""
        return MancheJoueurDAO().supprimer_par_id_manche(id_manche)

    @log
    def supprimer_participation(self, id_manche: int, id_joueur: int) -> bool:
        """Retire un joueur d’une manche"""
        return MancheJoueurDAO().supprimer_participation(id_manche, id_joueur)

    # Intéressant mais pas implémenté
    def obtenir_info_joueur(self, manche_id: int, joueur_id: int) -> Joueur | None:
        """Récupère les informations d’un joueur spécifique pour une manche"""
        res = self.dao.trouver_joueur_par_manche(manche_id, joueur_id)
        return Joueur(**res) if res else None
