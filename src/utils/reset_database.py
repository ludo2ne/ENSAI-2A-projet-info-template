import os
import logging


from unittest import mock

from utils.log_decorator import log
from utils.singleton import Singleton
from dao.db_connection import DBConnection
from service.utilisateur_service import UtilisateurService
import dotenv

dotenv.load_dotenv()  # Charger .env avant d'utiliser DBConnection ou ResetDatabase

from business_object.crea_data import*

class ResetDatabase(metaclass=Singleton):
    """
    Classe pour gérer la réinitialisation de la base de données.
    """

    def lancer_joueur(self):
        """
        Création de la table Joueur dans la base de données.
        """
        try:
            # Connexion à la base de données
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Commande SQL pour supprimer et recréer la table Joueur
                    cursor.execute(
                        """
                        DROP TABLE IF EXISTS Joueur;
                        CREATE TABLE Joueur (
                            nom VARCHAR(100) NOT NULL,
                            nationalite VARCHAR(50),
                            rating FLOAT,
                            match_id VARCHAR(50) NOT NULL,
                            equipe_nom VARCHAR(100),
                            shots INTEGER,
                            goals INTEGER,
                            saves INTEGER,
                            assists INTEGER,
                            score INTEGER,
                            shooting_percentage FLOAT,
                            time_offensive_third FLOAT,
                            time_defensive_third FLOAT,
                            time_neutral_third FLOAT,
                            demo_inflige INTEGER,
                            demo_recu INTEGER,
                            goal_participation FLOAT,
                            date TIMESTAMP WITH TIME ZONE,                 -- Date du match
                            region VARCHAR(50),        -- Région du match
                            ligue VARCHAR(100),        -- Ligue à laquelle appartient le match
                            stage VARCHAR(100),        -- Étape ou phase du tournoi ou du match
                            indice_offensif FLOAT,
                            indice_performance FLOAT,
                            PRIMARY KEY (match_id, equipe_nom,nom)
                        );
                        """
                    )
                    connection.commit()  # Confirmer les modifications
                    logging.info("Table Joueur créée avec succès.")
        except Exception as e:
            logging.error(f"Erreur lors de la création de la table Joueur: {e}")

    def lancer_equipe(self):
        """
        Création de la table Equipe dans la base de données.
        """
        try:
            # Connexion à la base de données
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Commande SQL pour supprimer et recréer la table Equipe
                    cursor.execute(
                        """
                        DROP TABLE IF EXISTS Equipe;
                        CREATE TABLE  Equipe (
                            match_id VARCHAR(255),                 -- Identifiant unique du match
                            equipe_nom VARCHAR(255),               -- Nom de l'équipe
                            equipe_score INT,                      -- Score de l'équipe
                            shots INT,                             -- Nombre de tirs
                            goals INT,                             -- Nombre de buts
                            saves INT,                             -- Nombre d'arrêts
                            assists INT,                           -- Nombre de passes décisives
                            score INT,                             -- Score total de l'équipe
                            demo_inflige INT,                      -- Démolitions infligées par l'équipe
                            demo_recu INT,                         -- Démolitions reçues par l'équipe
                            boost_stole INT,                       -- Nombre de boosts volés
                            shooting_percentage FLOAT,             -- Pourcentage de tirs réussis
                            time_defensive_third FLOAT,            -- Temps passé dans le tiers défensif (en secondes)
                            time_neutral_third FLOAT,              -- Temps passé dans le tiers neutre (en secondes)
                            time_offensive_third FLOAT,            -- Temps passé dans le tiers offensif (en secondes)
                            date TIMESTAMP WITH TIME ZONE,                             -- Date du match
                            region VARCHAR(50),                    -- Région du match
                            stage VARCHAR(100),                    -- Étape ou phase du tournoi ou du match
                            ligue VARCHAR(100),                    -- Ligue ou division du match
                            indice_performance FLOAT,
                            indice_de_pression FLOAT,
                            PRIMARY KEY (match_id, equipe_nom)     -- Clé primaire composée de match_id et equipe_nom
                        );
                        """
                    )
                    connection.commit()  # Confirmer les modifications
                    logging.info("Table Equipe créée avec succès.")
        except Exception as e:
            logging.error(f"Erreur lors de la création de la table Equipe: {e}")



    def lancer_match(self):
        """
        Création de la table Equipe dans la base de données.
        """
        try:
            # Connexion à la base de données
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Commande SQL pour supprimer et recréer la table Equipe
                    cursor.execute(
                        """
                        DROP TABLE IF EXISTS Match;
                        CREATE TABLE  Match (
                            match_id VARCHAR(255) PRIMARY KEY,
                            equipe1 VARCHAR(255),
                            equipe2 VARCHAR(255),
                            score1 INT,
                            score2 INT,
                            date DATE,  -- Utilisation d'un type DATE pour les dates
                            region VARCHAR(50),
                            stage VARCHAR(255),
                            ligue VARCHAR(255),
                            perso BOOL,
                            cote_equipe1 FLOAT,
                            cote_equipe2 FLOAT
                        );
                        """
                    )
                    connection.commit()  # Confirmer les modifications
                    logging.info("Table Match créée avec succès.")
        except Exception as e:
            logging.error(f"Erreur lors de la création de la table Match: {e}")


    def lancer(self):

        self.lancer_joueur()
        self.lancer_equipe()
        self.lancer_match()
            # Step 1: Initialiser l'API et le processeur de match
        api = API(base_url="https://api.rlcstatistics.net")
        match_processor = MatchProcessor(api)

            # Step 2: Récupérer les matchs
        match_processor.recup_matches(page=265, page_size=4)

            # Step 3: Récupérer les données des matchs
        match_processor.recup_match_data()

            # Step 4: Traiter les matchs et les joueurs
        match_processor.process_matches()
