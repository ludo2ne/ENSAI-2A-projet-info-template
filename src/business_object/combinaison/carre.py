from collections import Counter
from typing import List

from business_object.carte import Carte

from .combinaison import AbstractCombinaison


class Carre(AbstractCombinaison):
    """
    Représente un Carré, c'est-à-dire quatre cartes de même valeur.

    Le Carré peut avoir un kicker (la carte la plus haute restante)
    pour départager les égalités entre plusieurs Carrés.
    """

    def __init__(self, hauteur: str, kicker: tuple[str, ...]) -> None:
        """
        Initialise un Carré avec sa hauteur et son kicker.

        Paramètres
        ----------
        hauteur : str
            Valeur des cartes formant le Carré.
        kicker : tuple[str, ...]
            Carte restante servant à départager les égalités.

        Renvois
        -------
        None

        Exceptions
        ----------
        ValueError
            Levée si le nombre de cartes n’est pas suffisant ou si elles ne forment pas un Carré.
        """
        super().__init__(hauteur, kicker)

    @classmethod
    def FORCE(cls) -> int:
        """
        Renvoie la force relative d’un Carré.

        Renvois
        -------
        int
            Valeur numérique représentant la force du Carré (7).
            Plus la valeur est élevée, plus la combinaison est forte.
        """
        return 7

    @classmethod
    def est_present(cls, cartes: List[Carte]) -> bool:
        """
        Vérifie la présence d'un Carré dans une liste de cartes.

        Paramètres
        ----------
        cartes : List[Carte]
            Liste des cartes à analyser.

        Renvois
        -------
        bool
            True si au moins quatre cartes de même valeur sont présentes, False sinon.
        """
        valeurs = [c.valeur for c in cartes]
        compteur = Counter(valeurs)
        return any(count >= 4 for count in compteur.values())

    @classmethod
    def from_cartes(cls, cartes: List[Carte]) -> "Carre":
        """
        Construit un Carré à partir d’une liste de cartes.

        Paramètres
        ----------
        cartes : List[Carte]
            Liste des cartes disponibles.

        Renvois
        -------
        Carre
            Instance représentant le Carré détecté, avec son kicker.

        Exceptions
        ----------
        ValueError
            Levée si aucun Carré n’est trouvé dans les cartes.
        """
        cls.verifier_min_cartes(cartes)
        valeurs = [c.valeur for c in cartes]
        compteur = Counter(valeurs)

        carres_possibles = [v for v, count in compteur.items() if count >= 4]
        if not carres_possibles:
            raise ValueError(f"Aucun Carré présent dans les cartes : {dict(compteur)}")

        # Hauteur = Carré le plus fort
        hauteur = max(carres_possibles, key=lambda v: Carte.VALEURS().index(v))

        # Kicker = carte la plus haute hors Carré
        autres = [c for c in cartes if c.valeur != hauteur]
        kicker_valeur = max(autres, key=lambda c: Carte.VALEURS().index(c.valeur)).valeur

        return cls(hauteur, (kicker_valeur,))

    def __str__(self) -> str:
        """
        Renvoie une représentation lisible du Carré pour un joueur.

        Renvois
        -------
        str
            Exemple : "Carre de Roi" ou "Carre d'As".
        """
        if self.hauteur == "As":
            return "Carre d'As"
        return f"Carre de {self.hauteur}"

    def __repr__(self) -> str:
        """
        Renvoie une représentation technique du Carré.

        Renvois
        -------
        str
            Exemple : "Carre(hauteur=Roi, kicker=('As',))"
        """
        return f"Carre(hauteur={self.hauteur}, kicker={self.kicker})"
