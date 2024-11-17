import logging

from utils.singleton import Singleton
from utils.log_decorator import log

from dao.db_connection import DBConnection

from business_object.Equipe import Equipe
from business_object.joueur import Joueur


class EquipeDao(metaclass=Singleton):
    """Classe contenant les méthodes pour accéder aux Joueurs de la base de données"""

    @log
    def creer(self, equipe) -> bool:
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
                                         time_neutral_third, demo_inflige, demo_recu,indice_performance,
                                         indice_de_pression  )
                        VALUES (%(match_id)s, %(equipe_nom)s, %(equipe_score)s, %(boost_stole)s,
                                %(shots)s, %(goals)s, %(saves)s, %(assists)s, %(score)s, %(shooting_percentage)s,
                                 %(date)s, %(ligue)s, %(region)s, %(stage)s, %(time_offensive_third)s, %(time_defensive_third)s,
                                %(time_neutral_third)s, %(demo_inflige)s, %(demo_recu)s, %(indice_performance)s, %(indice_de_pression)s)
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
                            "demo_recu": equipe.demo_recu,
                            "indice_performance": equipe.indice_performance,
                            "indice_de_pression": equipe.indice_de_pression
                         },
                    )
                    # Récupérer l'ID du joueur créé
                    res = cursor.fetchone()
            return res is not None
        except Exception as e:
            logging.error(f"Erreur lors de la création d'equipe : {e}")
            return

    @log
    def obtenir_par_nom(self, equipe_nom: str) -> Equipe:
        """Récupère un joueur de la base de données par son nom

        Parameters
        ----------
        joueur_id : int
            L'ID du joueur à récupérer

        Returns
        -------
        joueur : Joueur
            Une instance du joueur récupéré
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Requête SQL pour obtenir un joueur par ID
                    cursor.execute(
                        """
                        SELECT*
                        FROM Equipe
                        WHERE equipe_nom = %s

                        """,
                        (equipe_nom,),
                    )
                    row = cursor.fetchone()
                    if row:
                        # Instancier et retourner le joueur
                        return Equipe(
                                            match_id=row["match_id"],
                                            equipe_nom=row["equipe_nom"],
                                            equipe_score=row["equipe_score"],
                                            boost_stole=row["boost_stole"],
                                            shots=row["shots"],
                                            goals=row["goals"],
                                            saves=row["saves"],
                                            assists=row["assists"],
                                            score=row["score"],
                                            shooting_percentage=row["shooting_percentage"],
                                            time_offensive_third=row["time_offensive_third"],
                                            time_defensive_third=row["time_defensive_third"],
                                            time_neutral_third=row["time_neutral_third"],
                                            demo_inflige=row["demo_inflige"],
                                            demo_recu=row["demo_recu"],
                                            date=row["date"],
                                            region=row["region"],
                                            ligue=row["ligue"],
                                            stage=row["stage"],
                                            indice_performance=row["indice_performance"],
                                            indice_de_pression=row["indice_de_pression"]
                                        )
        except Exception as e:
            logging.error(f"Erreur lors de la récupération du joueur avec l'ID {equipe_nom} : {e}")
            return None


    def nombre_match(self, equipe_nom: str) -> int:
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT COUNT(match_id) AS count
                        FROM Equipe
                        WHERE TRIM(LOWER(equipe_nom)) = TRIM(LOWER(%s));
                        """,
                        (equipe_nom,)
                    )

                    row = cursor.fetchone()

                    if row and 'count' in row and row['count'] is not None:
                        count = int(row['count'])  # Accéder à 'count' comme une clé de dictionnaire
                        logging.info(f"Nombre de matchs pour le joueur '{equipe_nom}': {count}")
                        return count
                    else:
                        logging.warning(f"Aucun match trouvé pour le joueur '{equipe_nom}'.")
                        return 0
        except Exception as e:
            logging.error(f"Erreur lors de la récupération des matchs pour le joueur '{equipe_nom}': {e}")
            return 0

    def moyennes_statistiques(self, equipe_nom: str, colonnes: list) -> dict:
        """
        Récupère les moyennes de plusieurs statistiques pour un joueur donné.

        Parameters
        ----------
        joueur_nom : str
            Le nom du joueur pour lequel récupérer les moyennes.
        colonnes : list
            Une liste des colonnes dont on veut calculer la moyenne (ex : ['score', 'rating', 'goals']).

        Returns
        -------
        dict
            Un dictionnaire contenant les moyennes des statistiques demandées.
            Exemple : {'score': 500.0, 'rating': 4.5, 'goals': 1.2}
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Construire la partie SELECT de la requête avec les colonnes
                    colonnes_sql = ", ".join([f"AVG({colonne}) AS {colonne}" for colonne in colonnes])

                    # Requête SQL pour calculer les moyennes
                    cursor.execute(
                        f"""
                        SELECT {colonnes_sql}
                        FROM Equipe
                        WHERE TRIM(LOWER(equipe_nom)) = TRIM(LOWER(%s));
                        """,
                        (equipe_nom,)
                    )

                    row = cursor.fetchone()

                    if row:
                        # Convertir les résultats en dictionnaire
                        moyennes = {colonne: float(row[colonne]) if row[colonne] is not None else 0.0 for colonne in colonnes}
                        logging.info(f"Moyennes pour le joueur '{equipe_nom}': {moyennes}")
                        return moyennes
                    else:
                        logging.warning(f"Aucune donnée trouvée pour le joueur '{equipe_nom}'.")
                        return {colonne: 0.0 for colonne in colonnes}
        except Exception as e:
            logging.error(f"Erreur lors de la récupération des moyennes pour le joueur '{equipe_nom}': {e}")
            return {colonne: 0.0 for colonne in colonnes}

