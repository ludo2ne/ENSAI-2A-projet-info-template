from service.consulter_stats import ConsulterStats
from view.vue_abstraite import VueAbstraite
from InquirerPy import inquirer


class MatchVue(VueAbstraite):
    """Une vue pour afficher les statistiques des matchs"""

    def __init__(self, message=""):
        self.message = message
        self.consulter_stats = ConsulterStats()

    def message_info(self):
        print("Consultation des statistiques des matchs")

    def choisir_menu(self):
        """Choix du menu suivant

        Return
        ------
        view
            Retourne la vue choisie par l'utilisateur dans le terminal
        """

        print("\n" + "-" * 50 + "\nAccueil\n" + "-" * 50 + "\n")

        reponse = input("Renseigner ou l'équipe ou la date du match: ")
        self.consulter_stats.stats_matchs(reponse)

        choix = inquirer.select(
            message="",
            choices=[
                "Chercher un autre match",
                "Chercher une équipe ou un joueur",
                "Retour",
            ],
        ).execute()

        match choix:
            case "Retour":
                from view.accueil.accueil_vue import AccueilVue

                return AccueilVue()

            case "Chercher un autre match":

                return self

            case "Chercher une équipe ou un joueur":
                from view.statistique.stat_vue import StatVue

                return StatVue()
