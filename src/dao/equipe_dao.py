import logging

from utils.singleton import Singleton
from utils.log_decorator import log

from dao.db_connection import DBConnection

from business_object.Equipe import Equipe


class EquipeDao(metaclass=Singleton):
    """Classe contenant les méthodes pour accéder aux Joueurs de la base de données"""

    @log
    def creer(self, Equipe) -> bool:
        """Creation d'un joueur dans la base de données

        Parameters
        ----------
        Equipe : Equipe

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
                        INSERT INTO Equipe (match_id, equipe_nom, equipe_image, equipe_score, equipe_winner,
                                        shots, goals, saves, assists, score, shooting_percentage, date, ligue, region, stage)
                        VALUES (%(match_id)s, %(equipe_nom)s, %(equipe_image)s, %(equipe_score)s, %(equipe_winner)s,
                                %(shots)s, %(goals)s, %(saves)s, %(assists)s, %(score)s, %(shooting_percentage)s, %(date)s,
                                %(ligue)s, %(region)s, %(stage)s)
                        
                        """,
                        {
                            "match_id": equipe.match_id,
                            "equipe_nom": equipe.equipe_nom,
                            "equipe_image": equipe.equipe_image,
                            "equipe_score": equipe.equipe_score,
                            "equipe_winner": equipe.equipe_winner,
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
                        },
                    )
                    
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)

        created = False
        if res:
            equipe.match_id = res["match_id"]  # Si un ID est retourné, on le met à jour
            created = True

        return created

    @log
    def lister_tous(self) -> list[Joueur]:
        """lister tous les joueurs

        Parameters
        ----------
        None

        Returns
        -------
        liste_joueurs : list[Joueur]
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
                    mdp=row["mdp"],
                    age=row["age"],
                    mail=row["mail"],
                    fan_pokemon=row["fan_pokemon"],
                )

                liste_joueurs.append(joueur)

        return liste_joueurs

    @log
