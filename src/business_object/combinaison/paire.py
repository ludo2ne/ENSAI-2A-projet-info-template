from collections import Counter
from typing import List, Tuple

from business_object.carte import Carte

from .combinaison import AbstractCombinaison


class Paire(AbstractCombinaison):
    """
    Représente une combinaison Paire au poker (deux cartes de même valeur).

    Une Paire est caractérisée par sa valeur principale et éventuellement
    des kickers pour départager les égalités.
    """

    def __init__(self, hauteur: str, kicker: Tuple[str, ...] = ()) -> None:
        """
        Initialise une combinaison Paire.

        Paramètres
        ----------
        hauteur : str
            Valeur de la Paire.
        kicker : Tuple[str, ...], optionnel
            Cartes restantes servant de kickers pour départager.
        """
        super().__init__(hauteur, kicker)

    @classmethod
    def FORCE(cls) -> int:
        """
        Force hiérarchique de la Paire.

        Returns
        -------
        int
            Valeur représentant la force de la combinaison (1).
        """
        return 1

    @classmethod
    def est_present(cls, cartes: List[Carte]) -> bool:
        """
        Vérifie si une Paire est présente dans une liste de cartes.

        Paramètres
        ----------
        cartes : List[Carte]
            Main de cartes à analyser.

        Returns
        -------
        bool
            True si au moins une Paire est présente.
        """
        valeurs = [c.valeur for c in cartes]
        compteur = Counter(valeurs)
        return any(count >= 2 for count in compteur.values())

    @classmethod
    def from_cartes(cls, cartes: List[Carte]) -> "Paire":
        """
        Construit une Paire à partir d'une liste de cartes.

        Paramètres
        ----------
        cartes : List[Carte]
            Liste de cartes disponibles.

        Returns
        -------
        Paire
            Instance représentant la Paire détectée avec ses kickers.

        Raises
        ------
        ValueError
            Si aucune Paire n'est présente.
        """
        cls.verifier_min_cartes(cartes)
        valeurs = [c.valeur for c in cartes]
        compteur = Counter(valeurs)

        paires = [v for v, count in compteur.items() if count >= 2]
        if not paires:
            raise ValueError("Aucune Paire présente")

        meilleure_paire = max(paires, key=lambda v: Carte.VALEURS().index(v))
        cartes_restantes = [v for v in valeurs if v != meilleure_paire]
        kickers = tuple(
            sorted(cartes_restantes, key=lambda v: Carte.VALEURS().index(v), reverse=True)
        )

        return cls(hauteur=meilleure_paire, kicker=kickers)

    def __str__(self) -> str:
        """
        Représentation lisible de la Paire.

        Returns
        -------
        str
            Exemple : "Paire As" ou "Paire Roi" selon la hauteur.
        """
        if self.hauteur == "As":
            return "Paire d'As"
        return f"Paire {self.hauteur}"

    def __repr__(self) -> str:
        """
        Représentation technique de la Paire.

        Returns
        -------
        str
            Exemple : "Paire(hauteur='Roi', kicker=('As','Dame','Valet'))"
        """
        return f"Paire(hauteur={self.hauteur}, kicker={self.kicker})"
