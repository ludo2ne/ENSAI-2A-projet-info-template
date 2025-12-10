import os

import requests
from InquirerPy import inquirer

from business_object.joueur import Joueur
from view.menu_admin import MenuAdminVue
from view.session import Session
from view.vue_abstraite import VueAbstraite

host = os.environ["HOST_WEBSERVICE"]
END_POINT = "/joueur/connexion"


class ConnexionVue(VueAbstraite):
    """Vue de Connexion (saisie de pseudo)"""

    def choisir_menu(self):
        pseudo = inquirer.text(message="Entrez votre pseudo : ").execute()
        url = f"{host}{END_POINT}/{pseudo}"

        req = requests.get(url)
        if req.status_code != 200:
            message = req.json().get("detail", "Erreur inconnue")
            from view.accueil.accueil_vue import AccueilVue

            return AccueilVue(message, temps_attente=2)

        data = req.json()
        joueur = Joueur(
            id_joueur=data["_Joueur__id_joueur"],
            pseudo=data["_Joueur__pseudo"],
            credit=data["_Joueur__credit"],
            pays=data["_Joueur__pays"],
        )

        # Connexion dans la session (avec l'ID seulement)
        Session().connexion(joueur.id_joueur)

        if joueur.pseudo == "admin":
            message = "Vous êtes connecté en tant qu'Admin"
            return MenuAdminVue(message, temps_attente=1)

        else:
            message = f"Vous êtes connecté sous le pseudo {joueur.pseudo}"
            from view.menu_joueur_vue import MenuJoueurVue

            return MenuJoueurVue(message, temps_attente=1)
