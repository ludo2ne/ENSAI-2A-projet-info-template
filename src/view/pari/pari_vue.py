from service.paris_service import ParisService
from view.vue_abstraite import VueAbstraite
from InquirerPy import inquirer


class PariVue(VueAbstraite):
    """Une vue pour afficher les paris d'un utilisateur"""

    def __init__(self, message=""):
        self.message = message
        self.paris = ParisService()

    def message_info(self):
        print("Paris de l'utilisateur")

    def choisir_menu(self):
        """Choix du menu suivant

        Return
        ------
        view
            Retourne la vue choisie par l'utilisateur dans le terminal
        """

        print("\n" + "-" * 50 + "\nAccueil\n" + "-" * 50 + "\n")

        self.paris.afficher_infos_paris()

        choix = inquirer.select(
            message="Souhaitez-vous faire un nouveau paris?",
            choices=[
                "Parier sur un nouveau match",
                "Retour",
            ],
        ).execute()

        match choix:
            case "Retour":
                from view.accueil.accueil_vue import AccueilVue

                return AccueilVue()

            case "Paris":
                from view.paris.nouveau_paris_vue import NouveauParisVue

                return NouveauParisVue()
