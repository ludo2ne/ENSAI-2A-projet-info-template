from InquirerPy import inquirer

from view.vue_abstraite import VueAbstraite
from view.session import Session

from service.utilisateur_service import UtilisateurService


class ConnexionVue(VueAbstraite):
    """Vue de Connexion (saisie de pseudo et mdp)"""

    def choisir_menu(self):
        # Demande à l'utilisateur de saisir pseudo et mot de passe
        pseudo = inquirer.text(message="Entrez votre pseudo : ").execute()
        mdp = inquirer.secret(message="Entrez votre mot de passe :").execute()

        # Appel du service pour trouver le utilisateur
        utilisateur = UtilisateurService().se_connecter(pseudo, mdp)

        # Si le utilisateur a été trouvé à partir des ses identifiants de connexion
        if utilisateur:
            message = f"Vous êtes connecté sous le pseudo {utilisateur.pseudo}"
            Session().connexion(utilisateur)

            from view.menu_utilisateur_vue import MenuJoueurVue

            return MenuJoueurVue(message)

        message = "Erreur de connexion (pseudo ou mot de passe invalide)"
        from view.accueil.accueil_vue import AccueilVue

        return AccueilVue(message)
