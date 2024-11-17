from InquirerPy import inquirer
from utils.reset_database import ResetDatabase
from view.vue_abstraite import VueAbstraite
from view.session import Session


class AccueilVue(VueAbstraite):
    """Vue d'accueil de l'application"""

    def message_info(self):
        with open("src/graphical_asset/nom.txt", "r", encoding="utf-8") as asset:
            print(asset.read())

    def choisir_menu(self):
        """Choix du menu suivant

        Return
        ------
        view
            Retourne la vue choisie par l'utilisateur dans le terminal
        """

        print("\n" + "-" * 50 + "\nAccueil\n" + "-" * 50 + "\n")
        if Session().utilisateur:
            choix = inquirer.select(
                message="Faites votre choix : ",
                choices=[
                    "Consulter les statistiques de match",
                    "Consulter les statistiques de joueur/équipe",
                    "Consulter le calendrier",
                    "Parier",
                    "Gestion des tournois",
                    "Infos de session",
                    "Se déconnecter",
                    "Quitter",
                ],
            ).execute()
        else:
            choix = inquirer.select(
                message="Faites votre choix : ",
                choices=[
                    "Se connecter",
                    "Créer un compte",
                    "Consulter les statistiques de match",
                    "Consulter les statistiques de joueur/équipe",
                    "Consulter le calendrier",
                    "Infos de session",
                    "Quitter",
                ],
            ).execute()

        match choix:
            case "Quitter":
                exit()

            case "Se connecter":
                from view.accueil.connexion_vue import ConnexionVue

                return ConnexionVue("Connexion à l'application")

            case "Créer un compte":
                from view.accueil.inscription_vue import InscriptionVue

                return InscriptionVue("Création de compte utilisateur")

            case "Consulter les statistiques de joueur/équipe":
                from view.statistique.stat_vue import VueConsulterStats

                return VueConsulterStats("Consulter les statistiques de joueur/équipe")

            case "Consulter les statistiques de match":
                from view.statistique.match_vue import MatchVue

                return MatchVue("Consultation des statistiques de match")

            case "Consulter le calendrier":
                from view.statistique.calendrier_vue import CalendrierVue

                return CalendrierVue("")

            case "Gestion des tournois":
                from view.tournoi.tournoi_vue import TournoiVue

                return TournoiVue("")

            case "Parier":
                from view.pari.pari_vue import PariVue

                return PariVue("")

            case "Infos de session":
                return AccueilVue(Session().afficher())

                return AccueilVue(message)
