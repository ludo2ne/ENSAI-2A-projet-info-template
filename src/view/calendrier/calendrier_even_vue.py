from service.calendrier_evenement import CalendrierEvenement
from view.vue_abstraite import VueAbstraite
from InquirerPy import inquirer


class EvenementVue(VueAbstraite):
    """Une vue pour afficher les statistiques des matchs"""

    def __init__(self, message=""):
        self.message = message
        self.calendrier_evenement = CalendrierEvenement()

    def message_info(self):
        print("Calendrier des matchs futurs")

    def choisir_menu(self):
        """Choix du menu suivant

        Return
        ------
        view
            Retourne la vue choisie par l'utilisateur dans le terminal
        """

        print("\n" + "-" * 50 + "\nAccueil\n" + "-" * 50 + "\n")

        self.calendrier_evenement.afficher_calendrier_annee()

        choix = inquirer.select(
            message="",
            choices=[
                "Chercher un match spécifique",
                "Retour",
            ],
        ).execute()

        match choix:
            case "Retour":
                from view.accueil.accueil_vue import AccueilVue

                return AccueilVue()

            case "Chercher une équipe ou un joueur":
                from view.calendrier.recherche_vue import RechercheVue

                return RechercheVue()
