import json
import os

import requests
from InquirerPy import inquirer

from view.session import Session
from view.vue_abstraite import VueAbstraite

host = os.environ.get("HOST_WEBSERVICE")


class MenuAdminVue(VueAbstraite):
    """Menu de l'administrateur"""

    def __init__(self, message="", temps_attente=0, input_attente=False):
        super().__init__(message, temps_attente, input_attente)
        self.session = Session()

    def choisir_menu(self):
        print("\n" + "-" * 50 + "\nMenu Admin\n" + "-" * 50 + "\n")

        choix = inquirer.select(
            message="Faites votre choix : ",
            choices=[
                "Créditer un joueur",
                "Débiter un joueur",
                "Afficher les joueurs de la base de données",
                "Se déconnecter",
            ],
        ).execute()

        if not self.session.id_joueur:
            print("Aucun joueur connecté")
            from view.accueil.accueil_vue import AccueilVue

            return AccueilVue()

        match choix:
            case "Se déconnecter":
                requests.get(f"{host}/joueur/deconnexion/{self.session.id_joueur}")
                self.session.deconnexion()
                from view.accueil.accueil_vue import AccueilVue

                return AccueilVue()

            case "Créditer un joueur":
                message = self.crediter()

                from view.accueil.accueil_vue import AccueilVue

                return MenuAdminVue(message, temps_attente=2)

            case "Débiter un joueur":
                message = self.debiter()

                from view.accueil.accueil_vue import AccueilVue

                return MenuAdminVue(message, temps_attente=2)

            case "Afficher les joueurs de la base de données":
                try:
                    req = requests.get(f"{host}/joueur/")
                    if req.status_code == 200:
                        reponse = req.json()
                        message = json.dumps(reponse, indent=4, ensure_ascii=False)
                    else:
                        message = "Impossible de récupérer la liste des joueurs"
                except Exception:
                    print("Erreur lors de la récupération des joueurs")
                return MenuAdminVue(message, temps_attente=3)

    def crediter(self) -> str:
        """Permet à un administrateur d’ajouter du crédit à un joueur"""
        pseudo = inquirer.text(message="Entrez le pseudo du joueur à créditer : ").execute()
        credit = int(inquirer.number(message="Entrez le montant à créditer : ").execute())

        try:
            req = requests.put(f"{host}/admin/crediter/{pseudo}/{credit}")
            if req.status_code == 200:
                message = req.text
            else:
                message = "Erreur lors de l'ajout de crédit"

        except Exception as e:
            message = f"Montant invalide : {e}"

        return message

    def debiter(self) -> str:
        """Permet à un administrateur d’ajouter du crédit à un joueur"""
        pseudo = inquirer.text(message="Entrez le pseudo du joueur à débiter : ").execute()
        credit = int(inquirer.number(message="Entrez le montant à débiter : ").execute())

        try:
            req = requests.put(f"{host}/admin/debiter/{pseudo}/{credit}")
            if req.status_code == 200:
                message = req.text
            else:
                message = "Erreur lors du retrait des crédits"

        except Exception as e:
            message = f"Montant invalide : {e}"

        return message
