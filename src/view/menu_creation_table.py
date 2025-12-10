import os

import requests
from InquirerPy import inquirer

from view.vue_abstraite import VueAbstraite

host = os.environ["HOST_WEBSERVICE"]
END_POINT = "/table/"


class MenuCreationTable(VueAbstraite):
    """Vue de création d'une table"""

    def choisir_menu(self):
        # Demande à l'utilisateur de saisir les paramètres de la table
        joueur_max = inquirer.number(
            message="Saisissez le nombre de joueurs maximum dans la table",
            min_allowed=2,
            max_allowed=10,
            default=5,
        ).execute()
        grosse_blind = inquirer.number(
            message="Saisissez la valeur de la grosse blind", min_allowed=2, default=40
        ).execute()

        # Préparation du payload pour l'API
        table_payload = {
            "joueurs_max": int(joueur_max),
            "grosse_blind": int(grosse_blind),
            "mode_jeu": 0,
            "joueurs": [],
        }

        # Appel API pour créer la table
        req = requests.post(f"{host}{END_POINT}", json=table_payload)

        if req.status_code == 200:
            table_creee = req.json()
            numero_table = table_creee.get("numero_table", "N/A")
            message = (
                f"Votre table a été créée (n°{numero_table}). Vous pouvez maintenant la rejoindre."
            )
        else:
            message = "Erreur de création de la table : paramètres incorrects"

        from view.menu_table import MenuTable

        return MenuTable(message, temps_attente=3)


class InfosTable(VueAbstraite):
    """
    Vue permettant d'afficher les informations d'une table :
    - Numéro de la table
    - Nombre de joueurs présents / nombre max
    - Liste des joueurs présents
    """

    def afficher_infos_table(self, numero_table: int):
        """
        Affiche le statut complet de la table via l'API

        Paramètres
        ----------
        numero_table : int
            Le numéro de la table à consulter
        """
        req = requests.get(f"{host}{END_POINT}id/{numero_table}")
        if req.status_code != 200:
            print("Erreur : impossible de récupérer les informations de la table.")
            return

        table_data = req.json()

        nb_joueurs_present = len(table_data.get("joueurs", []))
        nb_max = table_data.get("joueurs_max", "N/A")
        pseudos = [j["pseudo"] for j in table_data.get("joueurs", [])]

        print(f"\nTable n°{numero_table} : {nb_joueurs_present}/{nb_max} joueurs présents")
        if pseudos:
            print("Joueurs présents : " + ", ".join(pseudos))
        else:
            print("Aucun joueur présent pour le moment.\n")
