"""Implémentation de la classe MancheService"""

from business_object.manche import Manche
from dao.manche_dao import MancheDao


class MancheService:
    """Gère le stockage des manches dans la base de données"""

    def sauvegarder_manche(self, manche: Manche) -> None:
        """Crée une manche et l’enregistre via le DAO."""
        return MancheDao().sauvegarder(manche)

    def supprimer_manche(self, manche: Manche) -> bool:
        """
        Supprime une manche existante.

        Paramètres
        ----------
        id_manche : int
            l'identifiant de la manche à supprimer

        Renvois
        -------
        bool
            True si la suppression a réussi, False sinon
        """

        return MancheDao().supprimer(manche)
