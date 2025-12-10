from typing import List

from business_object.carte import Carte

from .combinaison import AbstractCombinaison


class QuinteFlush(AbstractCombinaison):
    """
    Représente une Quinte Flush au poker (suite de 5 cartes de même couleur).

    La combinaison est caractérisée par la valeur la plus haute de la suite.
    Le kicker n'est pas utilisé pour cette combinaison.
    """

    def __init__(self, hauteur: str, kicker=None) -> None:
        """
        Initialise une Quinte Flush.

        Paramètres
        ----------
        hauteur : str
            Carte la plus haute de la suite.
        kicker : None
            Non utilisé pour Quinte Flush.
        """
        super().__init__(hauteur, ())

    @classmethod
    def FORCE(cls) -> int:
        """
        Force hiérarchique de la Quinte Flush.

        Returns
        -------
        int
            Valeur représentant la force de la combinaison (8).
        """
        return 8

    @classmethod
    def est_present(cls, cartes: List[Carte]) -> bool:
        """
        Vérifie si une Quinte Flush est présente.

        Paramètres
        ----------
        cartes : List[Carte]
            Main de cartes à analyser.

        Returns
        -------
        bool
            True si une suite de 5 cartes de même couleur existe.
        """
        couleurs = [c.couleur for c in cartes]
        for couleur_max in set(couleurs):
            cartes_couleur = [c for c in cartes if c.couleur == couleur_max]
            if len(cartes_couleur) < 5:
                continue

            valeurs = sorted({Carte.VALEURS().index(c.valeur) for c in cartes_couleur})
            # Gérer l'As bas pour A-2-3-4-5
            if 12 in valeurs:  # As
                valeurs = [-1 if v == 12 else v for v in valeurs] + valeurs
            valeurs = sorted(set(valeurs))

            for i in range(len(valeurs) - 4):
                if valeurs[i : i + 5] == list(range(valeurs[i], valeurs[i] + 5)):
                    return True
        return False

    @classmethod
    def from_cartes(cls, cartes: List[Carte]) -> "QuinteFlush":
        """
        Construit une Quinte Flush à partir d'une main de cartes.

        Paramètres
        ----------
        cartes : List[Carte]
            Liste de cartes disponibles.

        Returns
        -------
        QuinteFlush
            Instance représentant la Quinte Flush détectée.

        Raises
        ------
        ValueError
            Si aucune Quinte Flush n'est trouvée.
        """
        cls.verifier_min_cartes(cartes)
        couleurs = [c.couleur for c in cartes]

        for couleur_max in set(couleurs):
            cartes_couleur = [c for c in cartes if c.couleur == couleur_max]
            if len(cartes_couleur) < 5:
                continue

            valeurs = sorted({Carte.VALEURS().index(c.valeur) for c in cartes_couleur})
            if 12 in valeurs:
                valeurs = [-1 if v == 12 else v for v in valeurs] + valeurs
            valeurs = sorted(set(valeurs))

            suites = [
                valeurs[i : i + 5]
                for i in range(len(valeurs) - 4)
                if valeurs[i : i + 5] == list(range(valeurs[i], valeurs[i] + 5))
            ]

            if suites:
                max_suite = max(suites, key=lambda s: s[-1])
                hauteur = Carte.VALEURS()[max_suite[-1] if max_suite[-1] != -1 else 12]
                return cls(hauteur=hauteur)

        raise ValueError("Aucune Quinte Flush présente.")

    def __str__(self) -> str:
        """
        Représentation lisible de la Quinte Flush.

        Returns
        -------
        str
            Exemple : "Quinte Flush" ou "Quinte Flush Royale" si As.
        """
        return "Quinte Flush Royale" if self.hauteur == "As" else "Quinte Flush"

    def __repr__(self) -> str:
        """
        Représentation technique pour le débogage.

        Returns
        -------
        str
            Exemple : "Quinte Flush(hauteur='Roi')"
        """
        return f"Quinte Flush(hauteur='{self.hauteur}')"
