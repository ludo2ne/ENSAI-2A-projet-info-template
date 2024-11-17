from service.tournoi_service import TournoiService
from view.vue_abstraite import VueAbstraite
from InquirerPy import inquirer


class PariVue(VueAbstraite):
    """Une vue pour afficher les paris d'un utilisateur"""

    def __init__(self, message=""):
        self.message = message
        self.tournoi = TournoiService()

    def message_info(self):
        print("Tournois de l'utilisateur")

    def choisir_menu(self):
        """Choix du menu suivant

        Return
        ------
        view
            Retourne la vue choisie par l'utilisateur dans le terminal
        """

        print("\n" + "-" * 50 + "\nAccueil\n" + "-" * 50 + "\n")

        self.tournois.afficher_infos_tournoi()

        choix = inquirer.select(
            message="Souhaitez-vous lancer un nouveau tournoi?",
            choices=[
                "Créer un tournoi",
                "Retour",
            ],
        ).execute()

        match choix:
            case "Retour":
                from view.accueil.accueil_vue import AccueilVue

                return AccueilVue()

            case "Paris":
                from view.tournoi.nouveau_tournoi_vue import NouveauTournoiVue

                return NouveauTournoiVue()
