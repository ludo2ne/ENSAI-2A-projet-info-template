from typing import List

from business_object.carte import Carte

from .combinaison import AbstractCombinaison


class Quinte(AbstractCombinaison):
    """
    Représente une Quinte au poker (suite de 5 cartes consécutives).

    La combinaison se caractérise par la carte la plus haute de la suite.
    Le kicker n'est pas utilisé pour cette combinaison.
    """

    def __init__(self, hauteur: str, kicker=None) -> None:
        """
        Initialise une Quinte.

        Paramètres
        ----------
        hauteur : str
            Carte la plus haute de la suite.
        kicker : None
            Non utilisé pour Quinte.

        Renvois
        -------
        None
        """
        super().__init__(hauteur, ())

    @classmethod
    def FORCE(cls) -> int:
        """
        Force hiérarchique de la Quinte.

        Renvois
        -------
        int
            Valeur entière représentant la force de la combinaison (4).
        """
        return 4

    @classmethod
    def est_present(cls, cartes: List[Carte]) -> bool:
        """
        Vérifie si une Quinte est présente dans la main.

        Paramètres
        ----------
        cartes : list[Carte]
            Liste de cartes à analyser.

        Renvois
        -------
        bool
            True si une Quinte est présente, False sinon.
        """
        valeurs = sorted({Carte.VALEURS().index(c.valeur) for c in cartes})
        if 12 in valeurs:  # gérer As bas pour A-2-3-4-5
            valeurs = [-1 if v == 12 else v for v in valeurs] + valeurs
        valeurs = sorted(set(valeurs))

        for i in range(len(valeurs) - 4):
            if valeurs[i : i + 5] == list(range(valeurs[i], valeurs[i] + 5)):
                return True
        return False

    @classmethod
    def from_cartes(cls, cartes: List[Carte]) -> "Quinte":
        """
        Construit une Quinte à partir d'une main de cartes.

        Paramètres
        ----------
        cartes : list[Carte]
            Liste de cartes à partir de laquelle on cherche une Quinte.

        Renvois
        -------
        Quinte
            Instance représentant la Quinte détectée.

        Exceptions
        ----------
        ValueError
            Si aucune Quinte n'est détectée dans la main.
        """
        cls.verifier_min_cartes(cartes)
        valeurs = sorted({Carte.VALEURS().index(c.valeur) for c in cartes})
        if 12 in valeurs:  # As bas
            valeurs = [-1 if v == 12 else v for v in valeurs] + valeurs
        valeurs = sorted(set(valeurs))

        suites = []
        for i in range(len(valeurs) - 4):
            suite = valeurs[i : i + 5]
            if suite == list(range(suite[0], suite[0] + 5)):
                suites.append(suite)

        if not suites:
            raise ValueError("Aucune Quinte présente.")

        max_suite = max(suites, key=lambda s: s[-1])
        hauteur = Carte.VALEURS()[max_suite[-1] if max_suite[-1] != -1 else 12]
        return cls(hauteur=hauteur)

    def __str__(self) -> str:
        """
        Représentation lisible de la Quinte.

        Renvois
        -------
        str
            Chaîne lisible pour le joueur, par exemple : "Quinte".
        """
        return "Quinte"

    def __repr__(self) -> str:
        """
        Représentation technique de la Quinte.

        Renvois
        -------
        str
            Chaîne détaillant la hauteur de la Quinte, par exemple : "Quinte(hauteur='As')".
        """
        return f"Quinte(hauteur='{self.hauteur}')"
