"""Implémentation de la classe Board"""

from business_object.carte import Carte
from business_object.liste_cartes import AbstractListeCartes


class Board(AbstractListeCartes):
    """Modélisation du board de poker"""

    def __init__(self, cartes: list[Carte] = None, complet: bool = False):
        """
        Instanciation d'un board

        Paramètres
        ----------
        cartes : list[Carte]
            Liste de cartes
        complet : bool
            si le board doit contenir toutes les cartes d'un jeu de cartes

        Renvois
        -------
        Board
            Instance de 'Board'

        Exceptions
        ----------
        ValueError
            si le board contient plus de 5 cartes
        """

        if cartes is not None and len(cartes) > 5:
            raise ValueError(f"Le nombre de cartes dans le board est trop grand : {len(cartes)}")

        super().__init__(cartes, complet)

    def affichage_board(self) -> str:
        """Retourne un affichge plus joli des cartes d'un board"""
        texte = ""
        for carte in self.cartes:
            texte += f"  {carte}  "

        for _ in range(5 - len(self)):
            texte += "   [?]   "

        return texte

    def ajouter_carte(self, carte: Carte) -> None:
        """
        Ajoute une carte dans le board. Et vérifie que le nombre de cartes reste en dessous de 5

        Paramètres
        ----------
        carte : Carte
            carte à ajouter au board

        Renvois
        -------
        None

        Exceptions
        ----------
        ValueError
            si le board a déjà plus de 5 cartes
        """

        if carte is not None and len(self.cartes) > 4:
            raise ValueError(
                f"Le nombre de cartes dans le board est trop grand : {len(self.cartes) + 1}"
            )

        super().ajouter_carte(carte)
