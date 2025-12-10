"""Implémentation de la classe JoueurDAO"""

import logging

from business_object.joueur import Joueur
from dao.db_connection import DBConnection
from utils.log_decorator import log
from utils.singleton import Singleton


class JoueurDao(metaclass=Singleton):
    """Classe contenant les méthodes pour intéragir avec la table des Joueurs de la base de données"""

    @log
    def creer(self, pseudo: str, pays: str) -> bool:
        """
        Création d'un joueur dans la base de données

        Paramètres
        ----------
        pseudo : str
            Le pseudo du joueur
        pays : str
            Le pays du joueur

        Renvois
        -------
        bool
            True si la création est un succès, False sinon
        """

        res = None

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO joueur(pseudo, credit, pays) VALUES        "
                        "(%(pseudo)s, 2000, %(pays)s)                         "
                        "RETURNING id_joueur;                                                ",
                        {
                            "pseudo": pseudo,
                            "pays": pays,
                        },
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)

        created = False
        if res:
            created = True

        return created

    def trouver_par_id(self, id_joueur: int) -> Joueur:
        """
        Trouver un joueur grace à son id

        Paramètres
        ----------
        id_joueur : int
            id du joueur que l'on souhaite trouver

        Renvois
        -------
        Joueur
            renvoie le joueur correspondant si il existe
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                           "
                        "  FROM joueur                      "
                        " WHERE id_joueur = %(id_joueur)s;  ",
                        {"id_joueur": id_joueur},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)
            raise

        joueur = None
        if res:
            joueur = Joueur(
                id_joueur=id_joueur, pseudo=res["pseudo"], credit=res["credit"], pays=res["pays"]
            )
        return joueur

    def trouver_par_pseudo(self, pseudo: str) -> Joueur:
        """
        Trouver un joueur grace à son pseudo

        Paramètres
        ----------
        pseudo : str
            pseudo du joueur que l'on souhaite trouver

        Renvois
        -------
        Joueur
            renvoie le joueur correspondant si il existe
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                           "
                        "  FROM joueur                      "
                        " WHERE pseudo = %(pseudo)s;  ",
                        {"pseudo": pseudo},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)
            raise

        joueur = None
        if res:
            joueur = Joueur(
                id_joueur=res["id_joueur"], pseudo=pseudo, credit=res["credit"], pays=res["pays"]
            )
        return joueur

    def lister_tous(self) -> list[Joueur]:
        """
        Lister tous les joueurs

        Paramètres
        ----------
        None

        Renvois
        -------
        list[Joueur]
            renvoie la liste de tous les joueurs dans la base de données
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                              "
                        "  FROM joueur;                        "
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logging.info(e)
            raise

        liste_joueurs = []

        if res:
            for row in res:
                joueur = Joueur(
                    id_joueur=row["id_joueur"],
                    pseudo=row["pseudo"],
                    credit=row["credit"],
                    pays=row["pays"],
                )

                liste_joueurs.append(joueur)
                texte = "["
            for joueur in liste_joueurs:
                texte += f"{joueur}, "
            texte[:-2] + "]"

        return texte[:-2] + "]"

    @log
    def modifier(self, joueur: Joueur) -> bool:
        """
        Modification d'un joueur dans la base de données

        Paramètres
        ----------
        joueur : Joueur
            Le joueur dont on souhaite mettre à jour les informations

        Renvois
        -------
        bool
            True si la modification est un succès, False sinon
        """

        res = None

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE joueur                                      "
                        "   SET pseudo      = %(pseudo)s,                   "
                        "       credit      = %(credit)s,                   "
                        "       pays        = %(pays)s                      "
                        " WHERE id_joueur = %(id_joueur)s;                  ",
                        {
                            "pseudo": joueur.pseudo,
                            "credit": joueur.credit,
                            "pays": joueur.pays,
                            "id_joueur": joueur.id_joueur,
                        },
                    )
                    res = cursor.rowcount
        except Exception as e:
            logging.info(e)

        return res == 1

    @log
    def supprimer(self, joueur: Joueur) -> bool:
        """
        Suppression d'un joueur dans la base de données

        Paramètres
        ----------
        joueur : Joueur
            joueur à supprimer de la base de données

        Renvois
        -------
        bool
            True si le joueur a bien été supprimé, False sinon
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Supprimer le compte d'un joueur
                    cursor.execute(
                        "DELETE FROM joueur                   WHERE id_joueur=%(id_joueur)s      ",
                        {"id_joueur": joueur.id_joueur},
                    )
                    res = cursor.rowcount
        except Exception as e:
            logging.info(e)
            raise

        return res > 0

    @log
    def se_connecter(self, pseudo: str) -> Joueur:
        """
        Se connecter grâce à son pseudo

        Paramètres
        ----------
        pseudo : str
            pseudo du joueur que l'on souhaite trouver

        Renvois
        -------
        Joueur
            renvoie le joueur que l'on cherche
        """

        res = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                           "
                        "  FROM joueur                      "
                        " WHERE pseudo = %(pseudo)s         ",
                        {"pseudo": pseudo},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)

        joueur = None

        if res:
            joueur = Joueur(
                id_joueur=res["id_joueur"],
                pseudo=res["pseudo"],
                credit=res["credit"],
                pays=res["pays"],
            )

        return joueur
