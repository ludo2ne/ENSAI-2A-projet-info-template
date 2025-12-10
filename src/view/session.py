import os
from datetime import datetime

import pytz
import requests

from utils.singleton import Singleton


class Session(metaclass=Singleton):
    """
    Stocke les données liées à la session locale :
    - Un seul joueur est connecté par terminal
    - Les informations des autres joueurs et tables sont récupérées via API
    """

    def __init__(self):
        """Initialisation de la session"""
        self.id_joueur = None
        self.debut_connexion = None
        self.host = os.environ.get("HOST_WEBSERVICE")

    def connexion(self, id_joueur: int):
        """Connexion d’un joueur en session locale"""
        self.id_joueur = id_joueur
        self.debut_connexion = datetime.now(pytz.timezone("Europe/Paris")).strftime(
            "%d/%m/%Y %H:%M:%S"
        )
        print(f"Joueur {id_joueur} connecté à {self.debut_connexion}")

    def deconnexion(self):
        """Déconnexion du joueur local"""
        print(f"Joueur {self.id_joueur} déconnecté")
        self.id_joueur = None
        self.debut_connexion = None

    def get_joueur(self) -> dict | None:
        """Récupère les infos du joueur depuis l’API"""
        if self.id_joueur is None:
            return None
        try:
            resp = requests.get(f"{self.host}/joueur/connectes/id/{self.id_joueur}")
            if resp.status_code != 200:
                return None
            return resp.json()
        except Exception:
            return None

    def get_table(self) -> dict | None:
        """Récupère les infos de la table du joueur"""
        joueur = self.get_joueur()
        if not joueur:
            return None
        numero_table = joueur.get("_Joueur__numero_table")
        if numero_table is None:
            return None
        try:
            resp = requests.get(f"{self.host}/table/affichage/{numero_table}")
            if resp.status_code != 200:
                return None
            return resp.json()
        except Exception:
            return None

    def afficher(self) -> str:
        """Affiche les infos de la session et de la table"""
        res = "Actuellement en session :\n" + "-" * 30 + "\n"

        if self.id_joueur is None:
            return res + "Aucun joueur connecté.\n"

        joueur = self.get_joueur()
        if not joueur:
            return res + "Impossible de récupérer les infos du joueur.\n"

        pseudo = joueur.get("_Joueur__pseudo", "Inconnu")
        credit = joueur.get("_Joueur__credit", 0)
        res += f"Joueur connecté : {pseudo} : {credit} crédits\n"
        if self.debut_connexion:
            res += f"Début connexion : {self.debut_connexion}\n"

        # Affichage des joueurs à la table
        table = self.get_table()
        if table:
            numero_table = table.get("numero_table", "?")
            joueurs = table.get("joueurs", [])
            res += f"\nJoueurs à la table {numero_table} :\n" + "-" * 40 + "\n"
            for j in joueurs:
                pseudo_j = j.get("pseudo", "Inconnu")
                credit_j = j.get("credit", 0)
                res += f"{pseudo_j} : {credit_j} crédits\n"

        return res
