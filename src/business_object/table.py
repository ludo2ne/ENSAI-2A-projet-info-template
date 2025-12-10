"""Implémentation de la classe Table"""

import logging

from business_object.info_manche import InfoManche
from business_object.joueur import Joueur
from business_object.manche import Manche
from utils.log_decorator import log

logger = logging.getLogger(__name__)


class Table:
    """
    Modélisation d'une table de jeu de poker.

    Une table gère les joueurs, la grosse blind, le dealer, le mode de jeu
    et éventuellement la manche en cours.
    """

    def __init__(
        self,
        joueurs_max: int,
        grosse_blind: int,
        numero_table: int = 0,
        mode_jeu: int = 1,
        id_joueurs: list[int] = None,
        manche: Manche = None,
    ):
        """
        Instanciation de la table de jeu

        Paramètres
        ----------
        joueurs_max : int
            nombre de joueurs maximum sur la table
        grosse_blind : int
            valeur de la grosse blind
        mode_jeu : int
            code du mode de jeu de la tabl
            1 : Texas Hold'em (cash game)
        id_joueurs : list[int]
            liste des joueurs present sur la table
        manche : Manche
            Manche en cours sur la table

        Renvois
        -------
        Table
            Instance de 'Table'

        """
        self.__joueurs_max = joueurs_max
        self.__grosse_blind = grosse_blind
        self.__numero_table = numero_table
        self.__mode_jeu = mode_jeu
        self.__manche = manche
        self.joueurs: list[Joueur] = []

        if id_joueurs is None:
            self.__id_joueurs = []
        else:
            self.__id_joueurs = id_joueurs

    @property
    def joueurs_max(self):
        """Retourne l'attribut 'joueurs_max'"""
        return self.__joueurs_max

    @property
    def grosse_blind(self):
        """Retourne l'attribut 'grosse_blind'"""
        return self.__grosse_blind

    @property
    def numero_table(self):
        """Retourne l'attribut 'numero_table'"""
        return self.__numero_table

    @property
    def mode_jeu(self):
        """Retourne l'attribut 'mode_jeu'"""
        return self.__mode_jeu

    @property
    def id_joueurs(self):
        """Retourne l'attribut 'id_joueurs'"""
        return self.__id_joueurs

    @property
    def manche(self):
        """retourne l'attribut 'manche'"""
        return self.__manche

    def __str__(self):
        """Représentation d'une table"""
        return f"Table {self.numero_table}, grosse blind : {self.grosse_blind} ({len(self)}/{self.joueurs_max})"

    def __len__(self) -> int:
        """Retourne le nombre de joueurs à la table"""
        return len(self.id_joueurs)

    @log
    def ajouter_joueur(self, id_joueur: int) -> None:
        """
        Ajoute un joueur à la table

        Paramètres
        ----------
        joueur : Joueur
            joueur à ajouter à la table

        Renvois
        -------
        None
        """

        if not isinstance(id_joueur, int):
            raise TypeError(f"L'id_joueur n'est pas un entier : {type(id_joueur)}")

        if len(self.__id_joueurs) >= self.__joueurs_max:
            logger.warning(f"Table pleine : impossible d'ajouter le joueur {id_joueur}")
            raise ValueError("Nombre maximum de joueurs atteint")

        logger.info(
            f"Le joueur {id_joueur} rejoint la table {self.numero_table} ({len(self.id_joueurs)}/{self.joueurs_max})"
        )
        self.__id_joueurs.append(id_joueur)

    @log
    def retirer_joueur(self, indice: int) -> Joueur:
        """
        Retire un joueur de la liste des joueurs selon son indice

        Paramètres
        ----------
        indice : int
            Indice du joueur à retirer dans la liste des joueurs

        Renvois
        -------
        Joueur
            Retourne le joueru retirée de la liste des joueurs
        """

        if not isinstance(indice, int):
            raise TypeError("L'indice doit être un entier")

        if indice >= len(self.__id_joueurs):
            raise IndexError(
                f"Indice plus grand que le nombre de joueurs : {len(self.__id_joueurs)}"
            )

        if indice < 0:
            raise IndexError("Indice négatif impossible")

        logger.info(f"Le joueur {self.id_joueurs[indice]} est retiré de la table")
        return self.__id_joueurs.pop(indice)

    @log
    def mettre_grosse_blind(self, montant: int) -> None:
        """
        Change la valeur de la grosse blind de la table.

        Paramètres
        ----------
        montant : int
            Nouvelle valeur de la grosse blind.

        Renvois
        -------
        None
        """
        if not isinstance(montant, int):
            raise TypeError("Le crédit doit être un int")

        self.__grosse_blind = montant
        logger.info(f"La grosse blind de la table passe à {montant}")

    @log
    def rotation_dealer(self) -> None:
        """
        Change la valeur de la grosse blind de la table.

        Paramètres
        ----------
        montant : int
            Nouvelle valeur de la grosse blind.

        Renvois
        -------
        None
        """
        dealer = self.retirer_joueur(0)
        self.ajouter_joueur(dealer)

        logger.info(f"Le joueur {dealer} devient dealer")

    @log
    def nouvelle_manche(self, pseudos: list[str] = None) -> None:
        """
        Lance une nouvelle manche sur la table.

        Paramètres
        ----------
        Aucun

        Renvois
        -------
        None

        Exceptions
        ----------
        Exception
            Si le nombre de joueurs restants est inférieur à 2
        """

        if len(self.__id_joueurs) < 2:
            raise Exception(
                f"Trop peu de joueurs sur la table pour lancer une manche : {len(self.__id_joueurs)}"
            )

        self.__manche = Manche(
            info=InfoManche(self.__id_joueurs, pseudos), grosse_blind=self.__grosse_blind
        )
