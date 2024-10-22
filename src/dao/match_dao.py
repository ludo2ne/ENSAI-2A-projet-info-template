import logging

from utils.singleton import Singleton
from utils.log_decorator import log

from dao.db_connection import DBConnection

from business_object.Utilisateur import Utilisateur


class UtilisateurDao(metaclass=Singleton):
    """Classe contenant les méthodes pour accéder aux utilisateurs de la base de données"""

    @log
    def creer(self, utilisateur) -> bool:

        res = None

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO match(id_match, equipe1, equipe2, score1, score2, date, region, ligue, perso) VALUES        "
                        "(%(id_match)s, %(equipe1)s, %(equipe2)s, %(score1)s, %(score2)s, %(date)s, %(region)s, %(ligue)s, %(perso)s)             "
                        "  RETURNING id_utilisateur;                                                ",
                        {
                            "id_match": match.id_match,
                            "equipe1": match.equipe1,
                            "equipe2": match.equipe2,
                            "score1": match.score1,
                            "score2": match.score2,
                            "date": match.date,
                            "region": match.region,
                            "ligue": match.ligue,
                            "perso": match.perso

                        },
"
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)

        created = False
        if res:
            utilisateur.id_utilisateur = res["id_utilisateur"]
            created = True

        return created

    @log
    def trouver_par_id(self, id_utilisateur) -> Utilisateur:
        """trouver un utilisateur grace à son id

        Parameters
        ----------
        id_utilisateur : int
            numéro id du utilisateur que l'on souhaite trouver

        Returns
        -------
        utilisateur : Utilisateur
            renvoie le utilisateur que l'on cherche par id
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                           "
                        "  FROM utilisateur                      "
                        " WHERE id_utilisateur = %(id_utilisateur)s;  ",
                        {"id_utilisateur": id_utilisateur},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)
            raise

        utilisateur = None
        if res:
            utilisateur = Utilisateur(
                pseudo=res["pseudo"],
                age=res["age"],
                mail=res["mail"],
                fan_pokemon=res["fan_pokemon"],
                id_utilisateur=res["id_utilisateur"],
            )

        return utilisateur
