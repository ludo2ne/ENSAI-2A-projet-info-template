import os

import requests
from InquirerPy import inquirer

from service.joueur_service import JoueurService
from view.vue_abstraite import VueAbstraite

host = os.environ["HOST_WEBSERVICE"]
END_POINT = "/joueur/"


class InscriptionVue(VueAbstraite):
    def choisir_menu(self):
        # Demande à l'utilisateur de saisir pseudo, mot de passe...
        pseudo = inquirer.text(message="Entrez votre pseudo : ").execute()

        if JoueurService().pseudo_deja_utilise(pseudo):
            from view.accueil.accueil_vue import AccueilVue

            return AccueilVue(f"Le pseudo {pseudo} est déjà utilisé.")

        pays = inquirer.text(message="Entrez votre pays : ").execute()

        # Appel de l'app pour créer le joueur
        joueur = {"id_joueur": 8, "pseudo": pseudo, "pays": pays, "credit": 0}
        
        req = requests.post(f"{host}{END_POINT}", json=joueur)

        if req.status_code == 200:
            message = f"Votre compte {joueur['pseudo']} a été créé. Vous pouvez maintenant vous connecter."
        else:
            message = f"{req.status_code} {req.text} Erreur de connexion (pseudo ou pays invalide)"

        from view.accueil.accueil_vue import AccueilVue

        return AccueilVue(message)

