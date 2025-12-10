from collections import Counter

from business_object.carte import Carte
from business_object.combinaison.combinaison import AbstractCombinaison


class Brelan(AbstractCombinaison):
    """
    Représente un Brelan, c'est-à-dire trois cartes de même valeur.

    Un Brelan peut avoir jusqu'à deux cartes supplémentaires ("kickers")
    pour départager les égalités entre plusieurs Brelans.
    """

    def __init__(self, hauteur: str, kicker: tuple[str, ...] = ()) -> None:
        """
        Initialise un Brelan avec sa valeur principale et ses kickers.

        Paramètres
        ----------
        hauteur : str
            La valeur principale du Brelan (par exemple "Roi").
        kicker : tuple[str, ...], optionnel
            Les valeurs des cartes restantes servant à départager les égalités.
            Seuls les deux kickers les plus forts sont conservés.

        Renvois
        -------
        None
        """
        super().__init__(hauteur, kicker)

    @classmethod
    def FORCE(cls) -> int:
        """
        Renvoie la force relative de la combinaison.

        Renvois
        -------
        int
            Valeur numérique représentant la force d’un Brelan.
            Plus la valeur est élevée, plus la combinaison est forte.
            Ici, un Brelan a une force de 4.
        """
        return 4

    @classmethod
    def est_present(cls, cartes: list[Carte]) -> bool:
        """
        Vérifie la présence d'un Brelan dans une liste de cartes.

        Paramètres
        ----------
        cartes : list[Carte]
            Liste des cartes à analyser.

        Renvois
        -------
        bool
            True si au moins trois cartes de même valeur sont présentes, False sinon.
        """
        valeurs = [c.valeur for c in cartes]
        freq = Counter(valeurs).values()
        return 3 in freq

    @classmethod
    def from_cartes(cls, cartes: list[Carte]) -> "Brelan":
        """
        Construit un objet Brelan à partir d'une liste de cartes.

        Paramètres
        ----------
        cartes : list[Carte]
            Liste des cartes disponibles pour former le Brelan.

        Renvois
        -------
        Brelan
            Instance représentant le Brelan détecté, avec ses kickers.

        Exceptions
        ----------
        ValueError
            Levée si aucune combinaison de trois cartes de même valeur n’est trouvée.
        """
        cls.verifier_min_cartes(cartes)
        valeurs = [c.valeur for c in cartes]
        compteur = Counter(valeurs)

        brelans = [v for v, count in compteur.items() if count == 3]
        if not brelans:
            details = ", ".join(f"{val}:{nb}" for val, nb in compteur.items())
            raise ValueError(f"Aucun brelan présent dans les cartes {details}")

        hauteur = max(brelans, key=lambda v: Carte.VALEURS().index(v))
        autres = sorted(
            (c for c in cartes if c.valeur != hauteur),
            key=lambda c: Carte.VALEURS().index(c.valeur),
            reverse=True,
        )
        kicker = tuple(c.valeur for c in autres[:2])
        return cls(hauteur, kicker)

    def __str__(self) -> str:
        """
        Renvoie une description lisible du Brelan pour un joueur.

        Renvois
        -------
        str
            Exemple : "Brelan de Roi" ou "Brelan d'As".
        """
        if self.hauteur == "As":
            return "Brelan d'As"
        return f"Brelan de {self.hauteur}"

    def __repr__(self) -> str:
        """
        Renvoie une représentation technique détaillée du Brelan.

        Renvois
        -------
        str
            Exemple : "Brelan(hauteur=Roi, kickers=(As, Dame))".
        """
        if self.kicker is None:
            return f"Brelan(hauteur={self.hauteur})"

        kicker_tuple = self.kicker if isinstance(self.kicker, tuple) else (self.kicker,)
        return f"Brelan(hauteur={self.hauteur}, kickers={kicker_tuple})"
