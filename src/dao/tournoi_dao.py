import logging

from utils.singleton import Singleton
from utils.log_decorator import log

from dao.db_connection import DBConnection

from business_object.Tournoi import Tournoi


class TournoiDao(metaclass=Singleton):

    @log
    def creer(self, Tournoi) -> bool:
        """Creation d'un joueur dans la base de données

        Parameters
        ----------
        equipe : Equipe

        Returns
        -------
        created : bool
            True si la création est un succès
            False sinon
        """

        res = None
        try:
            # Connexion à la base de données
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Requête d'insertion SQL avec RETURNING pour récupérer l'ID
                    cursor.execute(
                        """
                        INSERT INTO Equipe (match_id, equipe_nom, equipe_score, boost_stole,
                                        shots, goals, saves, assists, score, shooting_percentage,
                                         date, ligue, region, stage, time_offensive_third, time_defensive_third,
                                         time_neutral_third, demo_inflige, demo_recu )
                        VALUES (%(match_id)s, %(equipe_nom)s, %(equipe_score)s, %(boost_stole)s,
                                %(shots)s, %(goals)s, %(saves)s, %(assists)s, %(score)s, %(shooting_percentage)s,
                                 %(date)s, %(ligue)s, %(region)s, %(stage)s, %(time_offensive_third)s, %(time_defensive_third)s,
                                %(time_neutral_third)s, %(demo_inflige)s, %(demo_recu)s)
                        RETURNING equipe_nom;

                        """,
                        {
                            "match_id": equipe.match_id,
                            "equipe_nom": equipe.equipe_nom,
                            "equipe_score": equipe.equipe_score,
                            "boost_stole": equipe.boost_stole,
                            "shots": equipe.shots,
                            "goals": equipe.goals,
                            "saves": equipe.saves,
                            "assists": equipe.assists,
                            "score": equipe.score,
                            "shooting_percentage": equipe.shooting_percentage,
                            "date": equipe.date,
                            "ligue": equipe.ligue,
                            "region": equipe.region,
                            "stage": equipe.stage,
                            "time_offensive_third": equipe.time_offensive_third,
                            "time_defensive_third": equipe.time_defensive_third,
                            "time_neutral_third": equipe.time_neutral_third,
                            "demo_inflige": equipe.demo_inflige,
                            "demo_recu": equipe.demo_recu
                         },
                    )
                    # Récupérer l'ID du joueur créé
                    res = cursor.fetchone()
            return res is not None
        except Exception as e:
            logging.error(f"Erreur lors de la création d'equipe : {e}")
            return False
