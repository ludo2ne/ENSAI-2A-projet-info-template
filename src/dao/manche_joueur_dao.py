"""Implémentation de la classe MancheJoueurDAO"""

import logging

from business_object.info_manche import InfoManche
from dao.db_connection import DBConnection
from utils.log_decorator import log
from utils.singleton import Singleton

logger = logging.getLogger(__name__)


class MancheJoueurDAO(metaclass=Singleton):
    """Classe contenant les méthodes pour accéder à la table manche_joueur"""

    # ---------------------------------------------------------------------
    @log
    def creer_manche_joueur(self, id_manche: int, info_manche: InfoManche, gains : dict = {}) -> bool:
        """
        Création des entrées de la table manche_joueur pour une manche donnée.

        Paramètres
        ----------
        id_manche : int
            Identifiant de la manche concernée
        info_manche : InfoManche
            Object contenant les informations des joueurs de la partie

        Renvois
        -------
        bool
            True si la création est un succès, False sinon
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    for i, joueur in enumerate(info_manche.joueurs):
                        # Cartes du joueur si elles existent
                        carte1 = None
                        carte2 = None
                        gain = 0 
                        if joueur in gains :
                            gain = gains[joueur]
                        # if hasattr(info_manche, "cartes_mains"):
                        try:
                            carte1 = info_manche.mains[i].cartes[0]
                            carte2 = info_manche.mains[i].cartes[1]
                        except (IndexError, TypeError):
                            pass  # reste None si non défini

                        # Insertion SQL
                        cursor.execute(
                            """
                            INSERT INTO manche_joueur(
                                id_joueur,
                                id_manche,
                                carte_main_1,
                                carte_main_2,
                                mise,
                                gain,
                                tour_couche
                            )
                            VALUES (
                                %(id_joueur)s,
                                %(id_manche)s,
                                %(carte_main_1)s,
                                %(carte_main_2)s,
                                %(mise)s,
                                %(gain)s,
                                %(tour_couche)s
                            );
                            """,
                            {
                                "id_manche": id_manche,
                                "id_joueur": joueur,
                                "carte_main_1": str(carte1),
                                "carte_main_2": str(carte2),
                                "gain": gain,
                                "mise": info_manche.mises[i],
                                "tour_couche": info_manche.tour_couche[i],
                            },
                        )
            return True

        except Exception as e:
            logging.error(f"[ERREUR DAO] Création manche_joueur : {e}")
            return False

    def trouver_par_ids(self, id_manche: int, id_joueur: int) -> list[dict]:
        """
        Récupère toutes les lignes de la table manche_joueur associées à une manche donnée.

        Paramètres
        ----------
        id_manche : int
            Identifiant de la manche concernée
        id_joueur : int
            Identifiant du joueur concernée

        Renvois
        -------
        list[dict]
            Liste des participations des joueurs dans cette manche
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT *
                          FROM manche_joueur
                         WHERE id_manche = %(id_manche)s and id_joueur = %(id_joueur)s;
                        """,
                        {"id_manche": id_manche, "id_joueur": id_joueur},
                    )
                    res = cursor.fetchall()

        except Exception as e:
            logging.error(f"[ERREUR DAO] Lecture manche_joueur : {e}")
            raise

        participations = []
        if res:
            for row in res:
                participations.append(
                    {
                        "id_manche": row["id_manche"],
                        "id_joueur": row["id_joueur"],
                        "carte_main_1": row["carte_main_1"],
                        "carte_main_2": row["carte_main_2"],
                        "gain": row["gain"],
                        "mise": row["mise"],
                        "tour_couche": row["tour_couche"],
                    }
                )
        return participations

    # ---------------------------------------------------------------------
    @log
    def supprimer_par_id_manche(self, id_manche: int) -> bool:
        """
        Supprime toutes les participations liées à une manche.

        Paramètres
        ----------
        id_joueur : int
            Identifiant du joueur concernée

        Renvois
        -------
        bool
            True si la suppression est un succès, False sinon
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        DELETE FROM manche_joueur
                         WHERE id_manche = %(id_manche)s;
                        """,
                        {"id_manche": id_manche},
                    )
                    res = cursor.rowcount
        except Exception as e:
            logging.error(f"[ERREUR DAO] Suppression manche_joueur : {e}")
            raise

        return res > 0

    # ---------------------------------------------------------------------
    @log
    def supprimer_participation(self, id_manche: int, id_joueur: int) -> bool:
        """
        Supprime la participation d’un joueur spécifique à une manche.

        Paramètres
        ----------
        id_manche : int
            Identifiant de la manche concernée
        id_joueur : int
            Identifiant du joueur concernée

        Renvois
        -------
        bool
            True si la suppression est un succès, False sinon
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        DELETE FROM manche_joueur
                         WHERE id_manche = %(id_manche)s
                           AND id_joueur = %(id_joueur)s;
                        """,
                        {"id_manche": id_manche, "id_joueur": id_joueur},
                    )
                    res = cursor.rowcount
        except Exception as e:
            logging.error(f"[ERREUR DAO] Suppression participation : {e}")
            raise

        return res == 1
