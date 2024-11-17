from service.consulter_stats import ConsulterStats
from view.vue_abstraite import VueAbstraite
from InquirerPy import inquirer


class VueConsulterStats(VueAbstraite):
    """Une vue pour afficher les statistiques des joueurs et des équipes"""

    def __init__(self, message=""):
        self.message = message
        self.consulter_stats = ConsulterStats()

    def message_info(self):
        print("Consultation des statistiques des équipes et des joueurs")

    def choisir_menu(self):
        """Choix du menu suivant

        Return
        ------
        view
            Retourne la vue choisie par l'utilisateur dans le terminal
        """

        print("\n" + "-" * 50 + "\nAccueil\n" + "-" * 50 + "\n")

        choix = inquirer.select(
            message="Voulez-vous consulter les statistique d'un joueur ou d'une équipe?",
            choices=[
                "Joueur",
                "Equipe",
                "Retour",
            ],
        ).execute()

        match choix:
            case "Retour":
                from view.accueil.accueil_vue import AccueilVue

                return AccueilVue("Connexion à l'application")

            case "Equipe":
                from view.statistique.stat_equipe_vue import EquipeVue

                return EquipeVue("Connexion à l'application")

            case "Joueur":
                from view.statistique.stat_joueur_vue import JoueurVue

                return JoueurVue("Création de compte utilisateur")
