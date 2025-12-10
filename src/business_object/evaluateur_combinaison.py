from typing import List

from business_object.carte import Carte
from business_object.combinaison.brelan import Brelan
from business_object.combinaison.carre import Carre
from business_object.combinaison.combinaison import AbstractCombinaison
from business_object.combinaison.couleur import Couleur
from business_object.combinaison.double_paire import DoublePaire
from business_object.combinaison.full import Full
from business_object.combinaison.paire import Paire
from business_object.combinaison.quinte import Quinte
from business_object.combinaison.quinte_flush import QuinteFlush
from business_object.combinaison.simple import Simple


class EvaluateurCombinaison:
    """
    Évalue la meilleure combinaison d'une main de poker donnée.
    La classe utilise une hiérarchie de combinaisons, de la plus forte à la plus faible,
    pour déterminer la combinaison présente dans un ensemble de cartes.

    """

    COMBINAISONS = [
        QuinteFlush,
        Carre,
        Full,
        Couleur,
        Quinte,
        Brelan,
        DoublePaire,
        Paire,
        Simple,
    ]

    @staticmethod
    def eval(cartes: List[Carte]) -> AbstractCombinaison:
        """
        Détermine et retourne la meilleure combinaison d'une liste de cartes.

        Paramètres
        ----------
        cartes : list[Carte]
            Liste de cartes composant la main à évaluer. Doit contenir au moins 5 cartes.

        Renvois
        -------
        AbstractCombinaison
            Instance de la sous-classe correspondant à la combinaison détectée


        Exceptions
        ----------
        ValueError
            Levée si la liste de cartes contient moins de 5 cartes.
        """
        if not cartes or len(cartes) < 5:
            raise ValueError(f"Au moins 5 cartes sont nécessaires, actuellement {len(cartes)}")

        for C in EvaluateurCombinaison.COMBINAISONS:
            if C.est_present(cartes):
                return C.from_cartes(cartes)

        # Si aucune combinaison ne correspond
        return Simple.from_cartes(cartes)
