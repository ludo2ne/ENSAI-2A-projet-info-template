from collections import Counter
from typing import List, Optional

from business_object.carte import Carte

from .combinaison import AbstractCombinaison


class Full(AbstractCombinaison):
    """
    Représente une combinaison Full au poker (Brelan + Paire).

    Le Full est caractérisé par :
    - la valeur du Brelan (trois cartes identiques),
    - la valeur de la Paire (deux cartes identiques différentes du Brelan).
    """

    def __init__(self, hauteur: List[str], kicker: Optional[str] = None) -> None:
        """
        Initialise une combinaison Full.

        Paramètres
        ----------
        hauteur : List[str]
            Liste de deux valeurs [brelan, paire], la plus forte en premier.
        kicker : str, optionnel
            Non utilisé pour le Full.
        """
        super().__init__(hauteur, kicker)

    @classmethod
    def FORCE(cls) -> int:
        """
        Force hiérarchique du Full.

        Returns
        -------
        int
            Valeur représentant la force de la combinaison (6).
        """
        return 6

    @classmethod
    def est_present(cls, cartes: List[Carte]) -> bool:
        """
        Vérifie la présence d'un Full dans une liste de cartes.

        Paramètres
        ----------
        cartes : List[Carte]
            Main de cartes à analyser.

        Returns
        -------
        bool
            True si un Brelan et une Paire distincte sont présents.
        """
        valeurs = [c.valeur for c in cartes]
        compteur = Counter(valeurs)
        has_brelan = any(count >= 3 for count in compteur.values())
        has_paire = any(count >= 2 for v, count in compteur.items() if count < 3)
        return has_brelan and has_paire

    @classmethod
    def from_cartes(cls, cartes: List[Carte]) -> "Full":
        """
        Construit un Full à partir d'une liste de cartes.

        Paramètres
        ----------
        cartes : List[Carte]
            Liste de cartes disponibles.

        Returns
        -------
        Full
            Instance représentant le Full détecté.

        Raises
        ------
        ValueError
            Si aucun Brelan ou Paire n'est trouvé.
        """
        cls.verifier_min_cartes(cartes)
        valeurs = [c.valeur for c in cartes]
        compteur = Counter(valeurs)

        # Brelan le plus fort
        brelans = [v for v, count in compteur.items() if count >= 3]
        if not brelans:
            raise ValueError("Aucun brelan pour former un Full")
        brelan = max(brelans, key=lambda v: Carte.VALEURS().index(v))

        # Paire la plus forte différente du brelan
        paires = [v for v, count in compteur.items() if count >= 2 and v != brelan]
        if not paires:
            raise ValueError("Aucune paire pour former un Full")
        paire = max(paires, key=lambda v: Carte.VALEURS().index(v))

        return cls(hauteur=[brelan, paire])

    def _valeur_comparaison(self):
        # Brelan puis paire
        brelan_val = Carte.VALEURS().index(self._hauteur[0])
        paire_val = Carte.VALEURS().index(self._hauteur[1])
        return (self.FORCE(), (brelan_val, paire_val), ())

    def __str__(self) -> str:
        """
        Représentation lisible du Full.

        Returns
        -------
        str
            Exemple : "Full Dame Roi".
        """
        return f"Full {self.hauteur[0]} {self.hauteur[1]}"

    def __repr__(self) -> str:
        """
        Représentation technique détaillée du Full.

        Returns
        -------
        str
            Exemple : "Full(hauteur=['Dame','Roi'], kicker=None)".
        """
        return f"Full(hauteur={self.hauteur}, kicker={self.kicker})"
