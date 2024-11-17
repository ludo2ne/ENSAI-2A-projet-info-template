from service.consulter_stats import ConsulterStats
from view.vue_abstraite import VueAbstraite
from InquirerPy import inquirer


class JoueurVue(VueAbstraite):
    """Une vue pour afficher les statistiques des joueurs"""

    def __init__(self, message=""):
        self.message = message
        self.consulter_stats = ConsulterStats()

    def message_info(self):
        print("Consultation des statistiques des joueurs")

    def choisir_menu(self):
        """Choix du menu suivant

        Return
        ------
        view
            Retourne la vue choisie par l'utilisateur dans le terminal
        """

        print("\n" + "-" * 50 + "\nConsulter Statistique - Joueur\n" + "-" * 50 + "\n")

        reponse = input("Nom du joueur: ")
        joueur_stat = self.consulter_stats.stats_joueurs(reponse)
        print(joueur_stat)

        choix = inquirer.select(
            message="Que voulez-vous faire maintenant?",
            choices=[
                "Chercher un autre joueur",
                "Chercher une équipe",
                "Retour",
            ],
        ).execute()

        match choix:
            case "Retour":
                from view.accueil.accueil_vue import AccueilVue

                return AccueilVue()

            case "Chercher un autre joueur":

                return self

            case "Chercher une équipe":
                from view.statistique.stat_equipe_vue import EquipeVue

                return EquipeVue()
