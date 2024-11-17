import regex
from InquirerPy import prompt
from prompt_toolkit.validation import ValidationError
from view.vue_abstraite import VueAbstraite
from service.utilisateur_service import UtilisateurService
from business_object.Utilisateur import Utilisateur


class InscriptionVue(VueAbstraite):
    def __init__(self, message=""):
        self.message = message
        self.__questions = [
            {
                "type": "input",
                "name": "pseudo",
                "message": "Choisissez un pseudo: ",
            },
            {
                "type": "password",  # permet de cacher le mdp
                "name": "mot_de_passe",
                "message": "Choisissez un mot de passe: ",
            },
            {
                "type": "password",
                "name": "confirmation_mot_de_passe",
                "message": "Confirmez votre mot de passe: ",
            },
            {"type": "input", "name": "email", "message": "Entrez votre email"},
        ]

    def message_info(self):
        print("Bonjour,choisissez votre pseudo et votre mot de passe s'il vous plait")

    def choisir_menu(self):
        reponse = prompt(self.__questions)

        if reponse["mot_de_passe"] != reponse["confirmation_mot_de_passe"]:
            print("Les mots de passe ne correspondent pas. Veuillez réessayer.")
            return self  # ramène au mot de passe
        self.validate(reponse["email"])
        pseudo = reponse["pseudo"]
        mot_de_passe = reponse["mot_de_passe"]
        email = reponse["email"]
        compte = UtilisateurService()

        result = compte.creer_utilisateur(
            pseudo,
            mot_de_passe,
            email,
        )
        if isinstance(result, Utilisateur):
            print("Compte créé avec succès ! ")
        else:
            print("Il y a eu une erreur avec la création du compte")

        """
        except Exception as e:
            print(f"Erreur lors de la création du compte : {e}")
            return self
        """

        from view.accueil.connexion_vue import ConnexionVue

        return ConnexionVue()

    def validate(self, document) -> None:
        ok = regex.match(r"^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$", document)
        if not ok:
            raise ValidationError(
                message="Please enter a valid mail", cursor_position=len(document)
            )
            return self
