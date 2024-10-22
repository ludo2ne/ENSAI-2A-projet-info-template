import logging
from utils.singleton import Singleton
from utils.log_decorator import log
from dao.db_connection import DBConnection
from business_object.joueur import Joueur


class JoueurDao(metaclass=Singleton):
    """Classe contenant les méthodes pour accéder aux Joueurs de la base de données"""

    @log
    def creer(self, joueur: Joueur) -> bool:
        """Création d'un joueur dans la base de données

        Parameters
        ----------
        joueur : Joueur
            Instance du joueur à insérer dans la base de données

        Returns
        -------
        created : bool
            True si la création est un succès, False sinon
        """
        res = None
        try:
            # Connexion à la base de données
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Requête d'insertion SQL
                    cursor.execute(
                        """
                        INSERT INTO Joueur (nom, nationalite, region, rating, match_id, shots, goals, saves, assists, score,
                                            shooting_percentage, time_offensive_third, time_defensive_third, time_neutral_third,
                                            demo_inflige, demo_recu, goal_participation)
                        VALUES (%(nom)s, %(nationalite)s, %(region)s, %(rating)s, %(match_id)s, %(shots)s, %(goals)s, %(saves)s,
                                %(assists)s, %(score)s, %(shooting_percentage)s, %(time_offensive_third)s, %(time_defensive_third)s,
                                %(time_neutral_third)s, %(demo_inflige)s, %(demo_recu)s, %(goal_participation)s,%(equipe_nom)s)
                        """,
                        {
                            "nom": joueur.nom,
                            "nationalite": joueur.nationalite,
                            "region": joueur.region,
                            "rating": joueur.rating,
                            "match_id": joueur.match_id,
                            "equipe_nom": joueur.equipe_nom,
                            "shots": joueur.shots,
                            "goals": joueur.goals,
                            "saves": joueur.saves,
                            "assists": joueur.assists,
                            "score": joueur.score,
                            "shooting_percentage": joueur.shooting_percentage,
                            "time_offensive_third": joueur.time_offensive_third,
                            "time_defensive_third": joueur.time_defensive_third,
                            "time_neutral_third": joueur.time_neutral_third,
                            "demo_inflige": joueur.demo_inflige,
                            "demo_recu": joueur.demo_recu,
                            "goal_participation": joueur.goal_participation,
                        },
                    )
                    # Récupérer l'ID du joueur créé
                    res = cursor.fetchone()
            return res is not None
        except Exception as e:
            logging.error(f"Erreur lors de la création du joueur : {e}")
            return False

    @log
    def obtenir_par_nom(self, joueur_nom: str) -> Joueur:
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
                        SELECT nom, nationalite, region, rating, match_id, shots, goals, saves, assists, score,
                               shooting_percentage, time_offensive_third, time_defensive_third, time_neutral_third,
                               demo_inflige, demo_recu, goal_participation
                        FROM Joueur
                        WHERE joueur_nom = %s
                        """,
                        (joueur_nom,),
                    )
                    row = cursor.fetchone()
                    if row:
                        # Instancier et retourner le joueur
                        return Joueur(
                            nom=row[0],
                            nationalite=row[1],
                            region=row[2],
                            rating=row[3],
                            match_id=row[4],
                            shots=row[5],
                            goals=row[6],
                            saves=row[7],
                            assists=row[8],
                            score=row[9],
                            shooting_percentage=row[10],
                            time_offensive_third=row[11],
                            time_defensive_third=row[12],
                            time_neutral_third=row[13],
                            demo_inflige=row[14],
                            demo_recu=row[15],
                            goal_participation=row[16],
                        )
        except Exception as e:
            logging.error(f"Erreur lors de la récupération du joueur avec l'ID {joueur_id} : {e}")
            return None

    @log
    def mettre_a_jour(self, joueur: Joueur) -> bool:
        """Met à jour un joueur dans la base de données

        Parameters
        ----------
        joueur : Joueur
            L'instance du joueur à mettre à jour

        Returns
        -------
        updated : bool
            True si la mise à jour est réussie, False sinon
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Requête SQL pour mettre à jour un joueur
                    cursor.execute(
                        """
                        UPDATE Joueur
                        SET nom = %(nom)s, nationalite = %(nationalite)s, region = %(region)s, rating = %(rating)s,
                            match_id = %(match_id)s, shots = %(shots)s, goals = %(goals)s, saves = %(saves)s,
                            assists = %(assists)s, score = %(score)s, shooting_percentage = %(shooting_percentage)s,
                            time_offensive_third = %(time_offensive_third)s, time_defensive_third = %(time_defensive_third)s,
                            time_neutral_third = %(time_neutral_third)s, demo_inflige = %(demo_inflige)s,
                            demo_recu = %(demo_recu)s, goal_participation = %(goal_participation)s
                        WHERE joueur_id = %(joueur_id)s
                        """,
                        {
                            "nom": joueur.nom,
                            "nationalite": joueur.nationalite,
                            "region": joueur.region,
                            "rating": joueur.rating,
                            "match_id": joueur.match_id,
                            "shots": joueur.shots,
                            "goals": joueur.goals,
                            "saves": joueur.saves,
                            "assists": joueur.assists,
                            "score": joueur.score,
                            "shooting_percentage": joueur.shooting_percentage,
                            "time_offensive_third": joueur.time_offensive_third,
                            "time_defensive_third": joueur.time_defensive_third,
                            "time_neutral_third": joueur.time_neutral_third,
                            "demo_inflige": joueur.demo_inflige,
                            "demo_recu": joueur.demo_recu,
                            "goal_participation": joueur.goal_participation,
                            "joueur_id": joueur.joueur_id,
                        },
                    )
                    return cursor.rowcount > 0
        except Exception as e:
            logging.error(f"Erreur lors de la mise à jour du joueur : {e}")
            return False

    @log
    def supprimer(self, joueur_id: int) -> bool:
        """Supprime un joueur de la base de données

        Parameters
        ----------
        joueur_id : int
            L'ID du joueur à supprimer

        Returns
        -------
        deleted : bool
            True si la suppression est réussie, False sinon
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Requête SQL pour supprimer un joueur par ID
                    cursor.execute("DELETE FROM Joueur WHERE joueur_id = %s", (joueur_id,))
                    return cursor.rowcount > 0
        except Exception as e:
            logging.error(f"Erreur lors de la suppression du joueur avec l'ID {joueur_id} : {e}")
            return False
