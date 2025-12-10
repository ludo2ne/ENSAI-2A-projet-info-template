from collections import Counter
from typing import List

from business_object.carte import Carte

from .combinaison import AbstractCombinaison


class Couleur(AbstractCombinaison):
    """
    Représente une combinaison de type Couleur  au poker.

    Une Couleur est constituée d'au moins cinq cartes de la même couleur.
    La force de la combinaison est déterminée par la carte la plus haute.
    """

    def __init__(self, hauteur: List[str], kicker=None) -> None:
        """
        Initialise une combinaison Couleur.

        Paramètres
        ----------
        hauteur : List[str]
            Liste des valeurs des cinq cartes les plus hautes de la couleur.
        kicker : None
            Non utilisé pour la Couleur.
        """
        super().__init__(hauteur, kicker or ())

    @classmethod
    def FORCE(cls) -> int:
        """
        Renvoie la force hiérarchique de la combinaison Couleur.

        Returns
        -------
        int
            Valeur représentant la force de la combinaison (5).
        """
        return 5

    @classmethod
    def est_present(cls, cartes: List[Carte]) -> bool:
        """
        Vérifie la présence d'une Couleur dans une liste de cartes.

        Paramètres
        ----------
        cartes : List[Carte]
            Main de cartes à analyser.

        Returns
        -------
        bool
            True si au moins cinq cartes ont la même couleur, False sinon.
        """
        couleurs = [c.couleur for c in cartes]
        freq = Counter(couleurs)
        return any(count >= 5 for count in freq.values())

    @classmethod
    def from_cartes(cls, cartes: List[Carte]) -> "Couleur":
        """
        Construit une combinaison Couleur à partir d'une liste de cartes.

        Paramètres
        ----------
        cartes : List[Carte]
            Liste de cartes disponibles.

        Returns
        -------
        Couleur
            Instance représentant la couleur détectée.

        Raises
        ------
        ValueError
            Si aucune couleur n'est présente.
        """
        cls.verifier_min_cartes(cartes)

        couleurs = [c.couleur for c in cartes]
        couleur_max = next((c for c in set(couleurs) if couleurs.count(c) >= 5), None)
        if couleur_max is None:
            raise ValueError("Aucune Couleur présente dans les cartes")

        cartes_couleur = [c for c in cartes if c.couleur == couleur_max]
        cartes_couleur.sort(key=lambda c: Carte.VALEURS().index(c.valeur), reverse=True)

        hauteur = [c.valeur for c in cartes_couleur[:5]]
        return cls(hauteur=hauteur, kicker=None)

    def __str__(self) -> str:
        """
        Représentation lisible par un joueur.

        Returns
        -------
        str
            Exemple : "Couleur".
        """
        return "Couleur"

    def __repr__(self) -> str:
        """
        Représentation technique détaillée de la combinaison.

        Returns
        -------
        str
            Exemple : "Couleur(hauteur=['As', 'Roi', 'Dame', 'Valet', '10'])".
        """
        return f"Couleur(hauteur={self.hauteur})"
