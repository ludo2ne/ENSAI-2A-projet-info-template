"""Implémentation de la classe Joueur"""

import logging

from utils.log_decorator import log

logger = logging.getLogger(__name__)


class Joueur:
    """Représente un joueur de poker avec ses informations personnelles"""

    def __init__(
        self,
        id_joueur: int,
        pseudo: str,
        credit: int,
        pays: str,
        numero_table: int = None,
        est_admin: True = False,
    ) -> "Joueur":
        """
        Crée un nouveau joueur avec ses informations de base.

        Paramètres
        ----------
        id_joueur : int
            Identifiant unique du joueur.
        pseudo : str
            Nom ou pseudo du joueur.
        credit : int
            Montant de crédits possédés par le joueur.
        pays : str
            Pays du joueur.
        table : Table
            Table à laquelle le joueur est associé (None si aucune).

        Renvois
        -------
        Joueur
            Instance du joueur créée.

        Exceptions
        ----------
        TypeError
            si un paramètre n'a pas le bon type indique dans le typage
        ValueError
            si l'id du joueur est négatif
            si le crédit est strictement négatif
        """

        if not isinstance(id_joueur, int):
            raise TypeError(f"L'identifiant du joueur doit être un int : {type(id_joueur)}")
        if id_joueur < 1:
            raise ValueError(
                f"L'identifiant du joueur doit être un entier strictement positif : {id_joueur}"
            )

        if not isinstance(pseudo, str):
            raise TypeError(f"Le pseudo du joueur doit être un str : {type(pseudo)}")

        if not isinstance(credit, int):
            raise TypeError(f"Le crédit du joueur doit être un int : {type(credit)}")
        if credit < 0:
            raise ValueError(f"Le crédit du joueur doit être un entier positif : {credit}")

        if not isinstance(pays, str):
            raise TypeError(f"Le pays du joueur doit être un str : {type(pays)}")

        self.__id_joueur = id_joueur
        self.__pseudo = pseudo
        self.__credit = credit
        self.__pays = pays
        self.__numero_table = numero_table
        self.__est_admin = est_admin

    @property
    def id_joueur(self) -> int:
        """Retourne l'identifiant du joueur"""
        return self.__id_joueur

    @property
    def pseudo(self) -> str:
        """Retourne le pseudo du joueur"""
        return self.__pseudo

    @property
    def credit(self) -> int:
        """Retourne les crédits du joueur"""
        return self.__credit

    @property
    def pays(self) -> str:
        """Retourne le pays du joueur"""
        return self.__pays

    @property
    def numero_table(self):
        """Retourne la table où se trouve le joueur"""
        return self.__numero_table

    @numero_table.setter
    def numero_table(self, numero_table: int):
        self.__numero_table = numero_table

    @property
    def est_admin(self) -> bool:
        """Renvoie si le joueur est un admin ou non"""
        return self.__est_admin

    @est_admin.setter
    def est_admin(self, valeur: bool):
        self.__est_admin = valeur

    def __str__(self) -> str:
        """Permet d'afficher le pseudo et les crédits du joueur"""
        return f"{self.__pseudo} : {self.__credit} crédits"

    def __repr__(self) -> str:
        """Représentation formelle d'un joueur selon ses informations"""
        return f"Joueur({self.__id_joueur}, {self.__pseudo}, {self.__pays})"

    def __eq__(self, other) -> bool:
        """
        Compare deux joueurs selon leur identifiant.

        Paramètres
        ----------
        other : any
            Objet à comparer.

        Renvois
        -------
        bool
            True si les identifiants des deux joueurs sont identiques, False sinon.
        """

        if not isinstance(other, Joueur):
            return False

        return self.__id_joueur == other.id_joueur

    def __hash__(self) -> int:
        """Code de hachage déterminé selon la représentation officielle du joueur"""
        return hash(self.__repr__())

    @log
    def ajouter_credits(self, credits: int) -> int:
        """
        Ajoute des crédits au joueur.

        Paramètres
        ----------
        credits : int
            Nombre de crédits à ajouter.

        Renvois
        -------
        int
            Total des crédits après l'ajout.
        """

        if not isinstance(credits, int):
            raise TypeError(f"Les crédits doivent être de type int : {type(credits)}")

        if credits < 0:
            raise ValueError(f"Le nombre de crédits à ajouter doit être positif : {credits}")

        self.__credit += credits
        logger.info(f"{self.pseudo} reçoit {credits} crédits")

        return self.credit

    @log
    def retirer_credits(self, credits: int) -> int:
        """
        Retire des crédits au joueur.

        Paramètres
        ----------
        credits : int
            Nombre de crédits à retirer.

        Renvois
        -------
        int
            Crédit restant du joueur après le retrait.

        Exceptions
        ----------
        ValueError
            Si le joueur ne possède pas suffisamment de crédits.
        """

        if not isinstance(credits, int):
            raise TypeError(f"Les crédits doivent être de type int : {type(credits)}")

        if credits < 0:
            raise ValueError(f"Le nombre de crédits à retirer doit être positif : {credits}")

        if credits > self.credit:
            logger.warning(
                f"Le joueur {self.pseudo} ne peut pas être débiter de {credits} (credit restant : {self.credit})"
            )
            raise ValueError(
                f"Le joueur {self.pseudo} a trop peu de crédits pour retirer {credits}: {self.credit}"
            )

        self.__credit -= credits
        logger.info(f"Le joueur {self.pseudo} a été débité de {credits}")

        return self.credit

    @log
    def rejoindre_table(self, numero_table: int) -> None:
        """
        Associe le joueur à une table de poker.

        Paramètres
        ----------
        table : Table
            Table que le joueur souhaite rejoindre.

        Exceptions
        ----------
        Exception
            Si le joueur est déjà à une table.
        """

        if self.numero_table is not None:
            raise Exception(f"Le joueur {self.pseudo} est déjà à une table")

        if not isinstance(numero_table, int):
            raise TypeError(f"le paramètre numero_table doit être un int : {type(numero_table)}")

        self.__numero_table = numero_table

        logger.info(f"Le joueur {self.pseudo} a rejoint une table")

    @log
    def quitter_table(self) -> None:
        """
        Retire le joueur de sa table actuelle.

        Exceptions
        ----------
        Exception
            Si le joueur n'est associé à aucune table.
        """

        if self.numero_table is None:
            raise Exception(f"Le joueur {self.pseudo} n'est actuellement à aucune table")

        numero_table = self.__numero_table

        self.__numero_table = None
        logger.info(f"Le joueur {self.pseudo} a quitté sa table {numero_table}")

    @log
    def changer_pseudo(self, pseudo: str) -> None:
        """
        Change le pseudo du joueur.

        Paramètres
        ----------
        pseudo : str
            Nouveau pseudo.

        Renvois
        -------
        None
        """

        if not isinstance(pseudo, str):
            raise TypeError(f"Le pseudo doit être de type str : {type(pseudo)}")

        logger.info(f"{self.pseudo} à changé de pseudo")
        self.__pseudo = pseudo

        return

    @log
    def changer_pays(self, pays: str) -> None:
        """
        Change le pays du joueur.

        Paramètres
        ----------
        pays : str
            Nouveau pays.

        Renvois
        -------
        None
        """

        if not isinstance(pays, str):
            raise TypeError(f"Le pays doit être de type str : {type(pays)}")

        self.__pays = pays
        logger.info(f"{self.pseudo} à changé de pays")
        return
