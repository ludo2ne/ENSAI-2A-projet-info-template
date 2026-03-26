from InquirerPy import inquirer

from service.joueur_service import JoueurService
from view.session import Session
from view.vue_abstraite import VueAbstraite


class ConnexionVue(VueAbstraite):
    """Vue de Connexion (saisie de pseudo et mdp)"""

    def choisir_menu(self):
        # Demande à l'utilisateur de saisir pseudo et mot de passe
        pseudo = inquirer.text(message="Entrez votre pseudo : ").execute()
        mdp = inquirer.secret(message="Entrez votre mot de passe :").execute()

        # Appel du service pour trouver le joueur
        joueur = JoueurService().se_connecter(pseudo, mdp)

        # Si le joueur a été trouvé à partir des ses identifiants de connexion
        if joueur:
            message = f"Vous êtes connecté sous le pseudo {joueur.pseudo}"
            Session().connexion(joueur)

            from view.menu_joueur_vue import MenuJoueurVue

            return MenuJoueurVue(message)

        message = "Erreur de connexion (pseudo ou mot de passe invalide)"
        from view.accueil.accueil_vue import AccueilVue

        return AccueilVue(message)
