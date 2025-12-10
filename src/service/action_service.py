"""Implémentation de la classe ActionService"""

from business_object.manche import Manche
from service.credit_service import CreditService
from service.joueur_service import JoueurService
from service.table_service import TableService


class ActionService:
    """Actions possibles d'un joueur dans une Manche"""

    def manche_joueur(self, id_joueur: int) -> Manche:
        """
        Fonction qui renvoie la manche dans laquelle le joueur joue

        Paramètres
        ----------
        id_joueur : int
            l'identifiant du jouur

        Renvois
        -------
        Manche
            la manche dans laquelle est le jouur

        Exceptions
        ----------
        ValueError
            si le joueur n'est pas à une table
            si aucune manche n'est en cours sur la table du joueur
            si le joueur n'est pas dans la manche en cours
        """
        joueur_service = JoueurService()
        table_service = TableService()
        joueur = joueur_service.trouver_par_id(id_joueur)
        table = table_service.table_par_numero(joueur.numero_table)

        if joueur.numero_table is None:
            raise ValueError(
                f"Le joueur {joueur.pseudo} n'est à aucune table et ne peut effectuer d'action"
            )

        if table.manche is None:
            raise ValueError(
                f"Le joueur {joueur.pseudo} est dans une table mais aucune manche n'est en cours"
            )

        if id_joueur not in table.manche.info.joueurs:
            raise ValueError(f"Le joueur {joueur.pseudo} ne participe pas à la manche en cours")

        return table.manche

    def all_in(self, id_joueur: int) -> None:
        """
        Fonction qui gère toutes les modifications engendrées par le all-in d'un joueur

        Paramètres
        ----------
        id_joueur : int
            l'identifiant du jouur qui réalise l'action

        Renvois
        -------
        None

        Exceptions
        ----------
        Exception
            si ce n'est pas au tour du joueur de jouer
        """

        joueur = JoueurService().trouver_par_id(id_joueur)

        manche = self.manche_joueur(id_joueur)

        if not manche.est_tour(id_joueur):
            raise Exception(f"Ce n'est pas à {joueur.pseudo} de jouer")

        montant = manche.action(id_joueur, "all-in", joueur.credit)
        CreditService().debiter(id_joueur, montant)

    def checker(self, id_joueur: int) -> None:
        """
        Fonction qui gère toutes les modifications engendrées par l'action de checker d'un joueur

        Paramètres
        ----------
        id_joueur : int
            l'identifiant du jouur qui réalise l'action

        Renvois
        -------
        None

        Exceptions
        ----------
        Exception
            si ce n'est pas au tour du joueur de jouer
        """

        manche = self.manche_joueur(id_joueur)

        manche.action(id_joueur, "checker")

    def se_coucher(self, id_joueur: int) -> None:
        """
        Fonction qui gère toutes les modifications engendrées par l'action de se coucher d'un joueur

        Paramètres
        ----------
        id_joueur : int
            l'identifiant du jouur qui réalise l'action

        Renvois
        -------
        None

        Exceptions
        ----------
        Exception
            si ce n'est pas au tour du joueur de jouer
        """

        manche = self.manche_joueur(id_joueur)

        manche.action(id_joueur, "se coucher")

    def suivre(self, id_joueur: int, relance: int = 0) -> None:
        """
        Fonction qui gère toutes les modifications engendrées par le suivi d'un joueur

        Paramètres
        ----------
        id_joueur : int
            l'identifiant du jouur qui réalise l'action

        Renvois
        -------
        None

        Exceptions
        ----------
        Exception
            si ce n'est pas au tour du joueur de jouer
        """

        joueur = JoueurService().trouver_par_id(id_joueur)

        manche = self.manche_joueur(id_joueur)

        montant = manche.action(id_joueur, "suivre", joueur.credit, relance)
        CreditService().debiter(id_joueur, montant)
