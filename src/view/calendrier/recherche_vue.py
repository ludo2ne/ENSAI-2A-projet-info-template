from service.calendrier_evenement import CalendrierEvenement
from view.vue_abstraite import VueAbstraite
from InquirerPy import inquirer


class RechercheVue(VueAbstraite):
    """Une vue pour afficher les statistiques des matchs"""

    def __init__(self, message=""):
        self.message = message
        self.calendrier_evenement = CalendrierEvenement()

    def message_info(self):
        print("")

    def choisir_menu(self):
        """Choix du menu suivant

        Return
        ------
        view
            Retourne la vue choisie par l'utilisateur dans le terminal
        """

        print("\n" + "-" * 50 + "\nAccueil\n" + "-" * 50 + "\n")

        date = input("A quelle date le match a-t-il eu lieu? (JJ/MM/AA): ")
        self.calendrier_evenement.rechercher_match_par_date(date)

        choix = inquirer.select(
            message="",
            choices=[
                "Afficher le calendrier",
                "Retour",
            ],
        ).execute()

        match choix:
            case "Retour":
                from view.accueil.accueil_vue import AccueilVue

                return AccueilVue()

            case "Afficher le calendrier":
                from view.calendrier.calendrier_even_vue import EvenementVue

                return EvenementVue()
