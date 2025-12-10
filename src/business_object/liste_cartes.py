"""Implémentation de la classe AbstractListeCartes"""

from abc import ABC
from copy import deepcopy
from random import shuffle

from business_object.carte import Carte


class AbstractListeCartes(ABC):
    """
    Représente une liste de cartes issues d'un jeu de cartes.

    Cette classe permet de gérer un ensemble de cartes, d'ajouter ou retirer des cartes,
    et de mélanger la liste. Elle peut également représenter un jeu complet.
    """

    def __init__(self, cartes: list[Carte], complet: bool):
        """
        Initialise une liste de cartes

        Paramètres
        ----------
        cartes : list[Carte] | None
            Liste initiale de cartes. Peut être vide ou None.
        complet : bool
            Indique si la liste doit être initialisée avec un jeu complet
            (toutes les valeurs et couleurs possibles).

        Renvois
        -------
        AbstractListeCartes
            Instance de la classe représentant la liste de cartes.

        Exceptions
        ----------
        TypeError
            si cartes n'est pas de type list ou si un élément de cette liste n'est pas de type Carte
        """

        if not isinstance(cartes, list) and cartes is not None:
            raise TypeError(f"cartes n'est pas list ou None : {type(cartes)}")

        # Vérifie que toutes les cartes de la liste sont de type 'Carte'
        if cartes is not None:
            for carte in cartes:
                if not isinstance(carte, Carte):
                    raise TypeError(
                        f"cartes ne doit contenir que des objet de type Carte : {type(carte)}"
                    )

        if cartes is None:
            self.__cartes = []

        if cartes is not None:
            self.__cartes = cartes

        # Créer un jeu de cartes complet
        if complet:
            self.__cartes = [
                Carte(valeur, couleur) for valeur in Carte.VALEURS() for couleur in Carte.COULEURS()
            ]

    @property
    def cartes(self) -> list[Carte]:
        """
        Retourne une copie profonde des cartes présentes dans la liste.

        Renvois
        -------
        list[Carte]
            Copie des cartes contenues dans la liste.
        """
        return deepcopy(self.__cartes)

    def __str__(self) -> str:
        """
        Représentation lisible de la liste de cartes

        Renvois
        -------
        str
            Chaîne affichant toutes les cartes dans la liste.
        """
        if len(self.__cartes) == 0:
            return "[]"

        texte = "["
        for carte in self.__cartes:
            texte += f"{carte}, "

        return texte[:-2] + "]"

    def __len__(self) -> int:
        """
        Nombre de cartes présentes dans la liste.

        Renvois
        -------
        int
            Nombre de cartes.
        """
        return len(self.__cartes)

    def __eq__(self, other) -> bool:
        """
        Compare l'égalité entre deux listes de cartes

        Paramètres
        ----------
        other : any
            Objet à comparer.

        Renvois
        -------
        bool
            True si les listes sont du même type, ont la même taille
            et contiennent exactement les mêmes cartes dans le même ordre.
        """

        if type(self) is not type(other):
            return False

        if len(self) != len(other):
            return False

        for carte in range(len(self)):
            if self.cartes[carte] != other.cartes[carte]:
                return False

        return True

    def ajouter_carte(self, carte: Carte) -> None:
        """
        Ajoute une carte à la liste

        Paramètres
        ----------
        carte : Carte
            Carte à ajouter.
        """

        if not isinstance(carte, Carte):
            raise TypeError(f"l'objet à ajouter n'est pas de type Carte : {type(carte)}")

        self.__cartes.append(carte)

    def retirer_carte(self, indice: int = 0) -> Carte:
        """
        Retire une carte de la liste selon son indice

        Paramètres
        ----------
        indice : int, optionnel
            Position de la carte à retirer (par défaut le premier élément).

        Renvois
        -------
        Carte
            Carte retirée de la liste.

        Exceptions
        ----------
        Exception
            Si la liste est vide.
        ValueError
            Si l'indice est invalide.
        """

        if len(self) == 0:
            raise Exception("La liste de cartes est vide, aucune carte ne peut être retirée.")

        if not isinstance(indice, int):
            raise TypeError(f"L'indice renseigné n'est pas de type int : {type(indice)}")

        if not (0 <= indice < len(self)):
            raise ValueError(f"L'indice renseigné est trop grand : {indice}")

        return self.__cartes.pop(indice)

    def melanger(self):
        """Mélange aléatoirement les cartes de la liste"""
        shuffle(self.__cartes)
