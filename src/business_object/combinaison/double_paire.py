from collections import Counter
from typing import List, Tuple

from business_object.carte import Carte

from .combinaison import AbstractCombinaison


class DoublePaire(AbstractCombinaison):
    """
    Représente une combinaison Double Paire au poker.

    Une Double Paire est constituée de deux paires de cartes de même valeur,
    plus éventuellement une carte restante servant de kicker.
    """

    def __init__(self, hauteur: Tuple[str, str], kicker: Tuple[str, ...] = ()) -> None:
        """
        Initialise une combinaison Double Paire.

        Paramètres
        ----------
        hauteur : Tuple[str, str]
            Hauteur des deux paires, la plus forte en premier.
        kicker : Tuple[str, ...], optionnel
            Carte restante servant de kicker.
        """
        hauteur = tuple(sorted(hauteur, key=lambda x: Carte.VALEURS().index(x), reverse=True))
        super().__init__(hauteur, kicker)

    @classmethod
    def FORCE(cls) -> int:
        """
        Force hiérarchique de la combinaison Double Paire.

        Returns
        -------
        int
            Valeur représentant la force de la combinaison (2).
        """
        return 2

    @classmethod
    def est_present(cls, cartes: List[Carte]) -> bool:
        """
        Vérifie la présence d'une Double Paire dans une liste de cartes.

        Paramètres
        ----------
        cartes : List[Carte]
            Liste de cartes à analyser.

        Returns
        -------
        bool
            True si au moins deux valeurs apparaissent au moins deux fois.
        """
        valeurs = [c.valeur for c in cartes]
        freq = Counter(valeurs)
        paires = [v for v, count in freq.items() if count >= 2]
        return len(paires) >= 2

    @classmethod
    def from_cartes(cls, cartes: List[Carte]) -> "DoublePaire":
        """
        Construit une Double Paire à partir d'une liste de cartes.

        Paramètres
        ----------
        cartes : List[Carte]
            Liste de cartes disponibles.

        Returns
        -------
        DoublePaire
            Instance représentant la Double Paire détectée.

        Raises
        ------
        ValueError
            Si aucune Double Paire n'est présente.
        """
        cls.verifier_min_cartes(cartes)

        valeurs = [c.valeur for c in cartes]
        compteur = Counter(valeurs)
        paires_possibles = [v for v, count in compteur.items() if count >= 2]

        if len(paires_possibles) < 2:
            raise ValueError("Aucune Double Paire présente dans les cartes")

        # Sélection des deux paires les plus fortes
        paires_hautes = tuple(
            sorted(paires_possibles, key=lambda v: Carte.VALEURS().index(v), reverse=True)[:2]
        )

        # Kicker : carte la plus haute restante
        cartes_restantes = [v for v in valeurs if v not in paires_hautes]
        kicker = ()
        if cartes_restantes:
            kicker = (max(cartes_restantes, key=lambda v: Carte.VALEURS().index(v)),)

        return cls(hauteur=paires_hautes, kicker=kicker)

    def __str__(self) -> str:
        """
        Représentation lisible par un joueur.

        Returns
        -------
        str
            Exemple : "Double Paire Roi Dame".
        """
        return f"Double Paire {self.hauteur[0]} {self.hauteur[1]}"

    def __repr__(self) -> str:
        """
        Représentation technique détaillée de la Double Paire.

        Returns
        -------
        str
            Exemple : "DoublePaire(hauteur=('Roi','Dame'), kicker=('As',))".
        """
        return f"DoublePaire(hauteur={self.hauteur}, kicker={self.kicker or ()})"
