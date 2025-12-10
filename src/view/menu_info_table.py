import logging
import os

import requests
from InquirerPy import inquirer

from business_object.joueur import Joueur
from view.session import Session
from view.vue_abstraite import VueAbstraite

logger = logging.getLogger(__name__)
host = os.environ.get("HOST_WEBSERVICE")
END_POINT = "/table/"


class InfoTableMenu(VueAbstraite):
    """Menu de gestion d'une table ."""

    def __init__(self, numero_table: int, message="", temps_attente=0, input_attente=False):
        self.numero_table = numero_table
        super().__init__(message, temps_attente, input_attente)

    def choisir_menu(self):
        """Boucle principale du menu de la table."""
        print("\n" + "-" * 50 + f"\nTable {self.numero_table}\n" + "-" * 50 + "\n")
        choix = inquirer.select(
            message="Faites votre choix :",
            choices=["Voir joueurs", "Lancer manche", "Quitter table"],
        ).execute()

        if choix == "Voir joueurs":
            texte = self.afficher_infos_table(self.numero_table)
            return InfoTableMenu(self.numero_table, texte, input_attente=True)

        elif choix == "Lancer manche":
            menu_manche = self.lancer_manche(self.numero_table)
            return menu_manche

        elif choix == "Quitter table":
            id_joueur = Session().id_joueur
            return self.quitter_table(id_joueur)

    def afficher_infos_table(self, numero_table: int) -> str:
        joueurs_ids = self.get_joueurs_table(numero_table)

        texte = f"\nTable n°{numero_table} ({len(joueurs_ids)} joueurs présents)\n"
        i = 0
        for jid in joueurs_ids:
            i += 1

            req = requests.get(f"{host}/joueur/connectes/id/{jid}")

            data = req.json()
            joueur = Joueur(
                id_joueur=data["_Joueur__id_joueur"],
                pseudo=data["_Joueur__pseudo"],
                credit=data["_Joueur__credit"],
                pays=data["_Joueur__pays"],
            )

            texte += f" - Joueur {i} : {joueur.pseudo}\n"

        return texte

    def get_joueurs_table(self, numero_table: int):
        try:
            resp = requests.get(f"{host}{END_POINT}joueurs/{numero_table}")
            if resp.status_code == 200:
                return resp.json()
            else:
                print("Impossible de récupérer les joueurs de la table")
                return []
        except requests.RequestException as e:
            logger.error(f"Erreur serveur lors de la récupération des joueurs : {e}")
            print("Erreur serveur lors de la récupération des joueurs de la table")
            return []

    def lancer_manche(self, numero_table: int):
        joueurs_ids = self.get_joueurs_table(numero_table)
        if not joueurs_ids:
            message = "Impossible de lancer la manche : aucun joueur présent"
            return InfoTableMenu(self.numero_table, message, temps_attente=2)

        try:
            req = requests.put(f"{host}/manche/lancer/{numero_table}")
            if req.status_code == 200:
                message = "Manche lancée !"

                reqj = requests.get(f"{host}/joueur/connectes/id/{Session().id_joueur}")

                data = reqj.json()
                joueur = Joueur(
                    id_joueur=data["_Joueur__id_joueur"],
                    pseudo=data["_Joueur__pseudo"],
                    credit=data["_Joueur__credit"],
                    pays=data["_Joueur__pays"],
                )

                from view.menu_manche import MenuManche

                return MenuManche(
                    self.numero_table, pseudo=joueur.pseudo, message=message, temps_attente=1
                )
            else:
                message = (
                    f"Erreur lors du lancement : {req.json().get('detail', 'Erreur inconnue')}"
                )
                return InfoTableMenu(self.numero_table, message, temps_attente=2)

        except requests.RequestException as e:
            message = f"Erreur serveur : {e}"
            return InfoTableMenu(self.numero_table, message, temps_attente=2)

    def quitter_table(self, id_joueur: int):
        try:
            req = requests.put(f"{host}/table/retirer/{id_joueur}")
            if req.status_code == 200:
                message = req.text
            else:
                message = req.text
        except requests.RequestException as e:
            logger.error(f"Erreur serveur lors de la déconnexion de la table : {e}")
            message = "Erreur serveur lors de la déconnexion de la table"

        from view.menu_joueur_vue import MenuJoueurVue

        return MenuJoueurVue(message, temps_attente=2)
