from typing import List, Tuple

from business_object.carte import Carte

from .combinaison import AbstractCombinaison


class Simple(AbstractCombinaison):
    """
    Représente une combinaison 'Simple' (carte haute seule).

    La combinaison se caractérise par la carte la plus haute et
    ses kickers (les cartes restantes triées par valeur décroissante).
    """

    def __init__(self, hauteur: str, kicker: Tuple[str, ...]) -> None:
        """
        Initialise une combinaison Simple.

        Paramètres
        ----------
        hauteur : str
            Valeur de la carte la plus haute.
        kicker : tuple[str, ...]
            Cartes restantes triées par valeur décroissante pour départager.

        Renvois
        -------
        None
        """
        super().__init__(hauteur, kicker)

    @classmethod
    def FORCE(cls) -> int:
        """
        Renvoie la force hiérarchique de la combinaison Simple.

        Renvois
        -------
        int
            Valeur entière représentant la force de la combinaison (0).
        """
        return 0

    @classmethod
    def est_present(cls, cartes: List[Carte]) -> bool:
        """
        Vérifie si une combinaison Simple est présente.

        Paramètres
        ----------
        cartes : list[Carte]
            Liste de cartes à analyser.

        Renvois
        -------
        bool
            True si la liste contient au moins une carte, False sinon.
        """
        return len(cartes) >= 1

    @classmethod
    def from_cartes(cls, cartes: List[Carte]) -> "Simple":
        """
        Construit une instance de Simple à partir d'une liste de cartes.

        Paramètres
        ----------
        cartes : list[Carte]
            Liste de cartes à partir de laquelle on sélectionne la carte haute.

        Renvois
        -------
        Simple
            Instance représentant la carte la plus haute et ses kickers.

        Exceptions
        ----------
        ValueError
            Si la liste de cartes est vide.
        """
        cls.verifier_min_cartes(cartes)
        cartes_triees = sorted(cartes, key=lambda c: Carte.VALEURS().index(c.valeur), reverse=True)
        hauteur = cartes_triees[0].valeur
        kickers = tuple(c.valeur for c in cartes_triees[1:5])
        return cls(hauteur=hauteur, kicker=kickers)

    def __str__(self) -> str:
        """
        Renvoie une représentation lisible de la combinaison Simple.

        Renvois
        -------
        str
            Chaîne lisible pour le joueur, exemple : "Simple".
        """
        return f"Simple {self.hauteur}"

    def __repr__(self) -> str:
        """
        Renvoie une représentation technique de la combinaison Simple.

        Renvois
        -------
        str
            Chaîne détaillant la hauteur et les kickers, exemple :
            "Simple(hauteur='As', kicker=('Roi', 'Dame', 'Valet', '10'))".
        """
        return f"Simple(hauteur='{self.hauteur}', kicker={self.kicker})"
