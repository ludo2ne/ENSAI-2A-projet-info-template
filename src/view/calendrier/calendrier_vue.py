from InquirerPy import inquirer
from view.vue_abstraite import VueAbstraite
from calendrier_evenement import CalendrierEvenement


class CalendrierVue(VueAbstraite):
    """Vue du calendrier (plus recherche de match par date)"""

    def __init__(self, message=""):
        self.message = message
        self.calendrier_evenement = CalendrierEvenement()

    def message_info(self):
        print("Calendrier des futurs matchs")

    def choisir_menu(self):
        """Choix du menu suivant

        Return
        ------
        view
            Retourne la vue choisie par l'utilisateur dans le terminal
        """

        print("\n" + "-" * 50 + "\nAccueil\n" + "-" * 50 + "\n")

        choix = inquirer.select(
            message="",
            choices=[
                "Afficher le calendrier des matchs futurs",
                "Rechercher un match dans le calendrier",
                "Retour",
            ],
        ).execute()

        match choix:
            case "Afficher le calendrier des matchs futurs":
                from view.calendrier.calendrier_even_vue import EvenementVue

                return EvenementVue()

            case "Rechercher un match dans le calendrier":
                from view.calendrier.recherche_vue import RechercheVue

                return RechercheVue()

            case "Retour":
                from view.accueil.accueil_vue import AcceuilVue

                return AcceuilVue()
