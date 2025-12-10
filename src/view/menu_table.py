"""Menu des tables"""

import logging
import os

import requests
from InquirerPy import inquirer

from view.session import Session
from view.vue_abstraite import VueAbstraite

host = os.environ["HOST_WEBSERVICE"]
END_POINT = "/table/"

logger = logging.getLogger(__name__)


class MenuTable(VueAbstraite):
    """Vue qui affiche les tables"""

    def choisir_menu(self):
        action_table = ["Retour au Menu Joueur", "Créer une Table"]

        print("\n" + "-" * 50 + "\nMenu Tables\n" + "-" * 50 + "\n")

        # Récupération des tables existantes
        try:
            reponse = requests.get(f"{host}{END_POINT}")
            boutons_tables = reponse.json()  # Liste de tables ["Table 1, ..."]
        except ValueError:
            boutons_tables = []

        # Ajout des tables à l'interface
        action_table += boutons_tables

        # Sélection du choix
        choix = inquirer.select(
            message="Choisissez votre action : ",
            choices=action_table,
        ).execute()

        # --- CAS FIXES ---
        if choix == "Retour au Menu Joueur":
            from view.menu_joueur_vue import MenuJoueurVue

            return MenuJoueurVue()

        if choix == "Créer une Table":
            from view.menu_creation_table import MenuCreationTable

            return MenuCreationTable()

        # --- CAS DES TABLES DYNAMIQUES ---
        if choix in boutons_tables:
            session = Session()
            id_joueur = session.id_joueur  # ID du joueur connecté

            # Extraction du numéro de table
            numero_table = int(choix.split()[1].rstrip(","))

            # Appel API pour rejoindre la table
            try:
                req = requests.put(f"{host}{END_POINT}ajouter/{numero_table}/{id_joueur}")
                if req.status_code == 200:
                    # Mise à jour locale
                    session.numero_table = numero_table
                    message = f"Vous êtes connecté sur la table {numero_table}"

                    # Redirection vers le menu infos table
                    from view.menu_info_table import InfoTableMenu

                    return InfoTableMenu(numero_table, message, temps_attente=2)

                else:
                    message = "Erreur lors de la connexion à la table"
                    from view.menu_table import MenuTable

                    return MenuTable(message, temps_attente=2)

            except requests.RequestException as e:
                logger.error(f"Erreur serveur : {e}")
                message = "Impossible de rejoindre la table"
                from view.menu_table import MenuTable

                return MenuTable(message, temps_attente=2)

        # Sécurité : retour menu joueur si choix invalide
        from view.menu_joueur_vue import MenuJoueurVue

        return MenuJoueurVue()
