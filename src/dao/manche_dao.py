"""Implémentation de la classe MancheDAO"""

import logging

from dao.db_connection import DBConnection
from utils.log_decorator import log
from utils.singleton import Singleton


class MancheDao(metaclass=Singleton):
    """Classe contenant les méthodes pour accéder à la table Manche de la base de données"""

    @log
    def sauvegarder(self, manche) -> int:
        """
        Creation d'une manche dans la base de données

        Paramètres
        ----------
        manche : Manche
            la manche dont on souhaite stocker les informations

        Renvois
        -------
        int
            l'identifiant de la manche nouvellement créée
        """

        res = None

        try:
            logging.info(f"Valeurs envoyées : {manche.board.cartes}")
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO manche(carte1, carte2, carte3, carte4, carte5) "
                        " VALUES (%(carte1)s, %(carte2)s, %(carte3)s, %(carte4)s, %(carte5)s)"
                        " RETURNING id_manche;                                                ",
                        {
                            "carte1": str(manche.board.cartes[0]),
                            "carte2": str(manche.board.cartes[1]),
                            "carte3": str(manche.board.cartes[2]),
                            "carte4": str(manche.board.cartes[3]),
                            "carte5": str(manche.board.cartes[4]),
                        },
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)

        if res:
            return res["id_manche"]

        return None

    @log
    def supprimer(self, manche) -> bool:
        """
        Suppression d'une manche dans la base de données

        Paramètres
        ----------
        manche : Manche
            manche à supprimer de la base de données

        Renvois
        -------
        bool
            True si la manche a bien été supprimée
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Supprimer la manche de la bbd
                    cursor.execute(
                        "DELETE FROM manche        "
                        "WHERE carte1=%(carte1)s and carte2=%(carte2)s and carte3=%(carte3)s and "
                        "carte4=%(carte4)s and carte5=%(carte5)s   ",
                        {
                            "carte1": str(manche.board.cartes[0]),
                            "carte2": str(manche.board.cartes[1]),
                            "carte3": str(manche.board.cartes[2]),
                            "carte4": str(manche.board.cartes[3]),
                            "carte5": str(manche.board.cartes[4]),
                        },
                    )
                    res = cursor.rowcount
        except Exception as e:
            logging.info(e)
            raise

        return res > 0
