from service.consulter_stats import ConsulterStats
from view.vue_abstraite import VueAbstraite
from InquirerPy import inquirer


class EquipeVue(VueAbstraite):
    """Une vue pour afficher les statistiques des équipes"""

    def __init__(self, message=""):
        self.message = message
        self.consulter_stats = ConsulterStats()

    def message_info(self):
        print("Consultation des statistiques des équipes")

    def choisir_menu(self):
        """Choix du menu suivant

        Return
        ------
        view
            Retourne la vue choisie par l'utilisateur dans le terminal
        """

        print("\n" + "-" * 50 + "\nAccueil\n" + "-" * 50 + "\n")

        reponse = input("Nom de l'équipe: ")
        self.consulter_stats.stats_equipe(reponse)

        choix = inquirer.select(
            message="",
            choices=[
                "Chercher une autre équipe",
                "Chercher un joueur",
                "Retour",
            ],
        ).execute()

        match choix:
            case "Retour":
                from view.accueil.accueil_vue import AccueilVue

                return AccueilVue()

            case "Chercher une autre équipe":

                return self

            case "Chercher un joueur":
                from view.statistique.stat_joueur_vue import JoueurVue

                return JoueurVue()
