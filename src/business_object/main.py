"""Implémentation de la classe Main"""

from business_object.carte import Carte
from business_object.liste_cartes import AbstractListeCartes


class Main(AbstractListeCartes):
    """
    Représente la main d'un joueur au poker.

    Cette classe hérite de AbstractListeCartes et permet de gérer les cartes
    détenues par un joueur, ainsi que leur combinaison évaluée.
    """

    def __init__(self, cartes: list[Carte] = None, complet: bool = False):
        """
        Initialise une main avec une liste de cartes.

        Paramètres
        ----------
        cartes : list[Carte] | None
            Cartes initiales de la main. Peut être None pour une main vide.
        complet : bool
            Si True, initialise avec un jeu complet.

        Renvois
        -------
        Main
            Instance de la main créée.
        """

        super().__init__(cartes, complet)

    def affichage_main(self) -> str:
        """Retourne un affichage plus joli des cartes d'une main"""
        texte = ""
        for carte in self.cartes:
            texte += f"  {carte}  "

        for _ in range(2 - len(self)):
            texte += "   [?]   "

        return texte

    def intervertir_cartes(self):
        """
        Déplace la première carte de la main à la fin, inversant ainsi l'ordre.

        Paramètres
        ----------
        None

        Renvois
        -------
        None
        """

        self.ajouter_carte(self.retirer_carte())
