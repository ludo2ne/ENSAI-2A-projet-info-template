import logging
import os

import requests
from InquirerPy import inquirer

from view.session import Session
from view.vue_abstraite import VueAbstraite

logger = logging.getLogger(__name__)
host = os.environ.get("HOST_WEBSERVICE")
END_POINT = "/action/"


class MenuManche(VueAbstraite):
    """Menu du joueur pendant une manche"""

    def __init__(
        self,
        numero_table: int,
        pseudo: str = "?",
        message="",
        temps_attente=0,
        input_attente=False,
    ):
        self.numero_table = numero_table
        self.pseudo = pseudo
        super().__init__(message, temps_attente, input_attente)

    def choisir_menu(self):
        print("\n" + "-" * 50)
        print(f"Menu Manche - Table {self.numero_table} - Joueur {self.pseudo}")
        print("-" * 50 + "\n")

        choix = inquirer.select(
            message="Faites votre choix :",
            choices=[
                "Voir infos manche",
                "Voir main",
                "Checker",
                "Suivre",
                "All in",
                "Se coucher",
                "Terminer manche",
            ],
        ).execute()

        if choix == "Voir infos manche":
            message = self.voir_infos_manche(self.numero_table)
            return MenuManche(self.numero_table, self.pseudo, message=message, input_attente=True)

        elif choix == "Voir main":
            message = self.voir_main(self.numero_table, Session().id_joueur)
            return MenuManche(self.numero_table, self.pseudo, message=message, input_attente=True)

        elif choix in ["Checker", "Suivre", "All in", "Se coucher"]:
            mapping = {
                "Checker": "checker",
                "Suivre": "suivre",
                "All in": "all_in",
                "Se coucher": "se_coucher",
            }

            message = self.effectuer_action(mapping[choix], Session().id_joueur)
            return MenuManche(self.numero_table, self.pseudo, message, temps_attente=2)

        elif choix == "Terminer manche":
            menu = self.terminer_manche(self.numero_table)

            return menu

    # -------------------------
    # Actions et affichages
    # -------------------------
    def voir_infos_manche(self, numero_table: int):
        try:
            req = requests.get(f"{host}/manche/affichage/{numero_table}")
            if req.status_code == 200:
                return "Infos :\n\n" + str(req.text).replace("\\n", "\n")
            else:
                return "Impossible de récupérer les infos de la manche"

        except requests.RequestException as e:
            logger.error(f"Erreur serveur lors de l'affichage de la manche : {e}")
            return "Erreur serveur lors de l'affichage de la manche"

    def voir_main(self, numero_table: int, id_joueur: int):
        try:
            resp = requests.get(f"{host}/manche/main/{numero_table}/{id_joueur}")
            if resp.status_code == 200:
                return resp.text
            else:
                return "Impossible de récupérer votre main"
        except requests.RequestException as e:
            logger.error(f"Erreur serveur lors de l'affichage de la main : {e}")
            return "Erreur serveur lors de l'affichage de la main"

    def effectuer_action(self, action: str, id_joueur: int):
        try:
            if action == "suivre":
                relance = inquirer.number(
                    "Valeur de la relance (0 si pas de relance) : ", min_allowed=0
                ).execute()
                montant = f"/{relance}"
            else:
                montant = ""

            resp = requests.put(f"{host}{END_POINT}{action}/{id_joueur}{montant}")
            if resp.status_code == 200:
                return f"Action '{action}' effectuée !"
            else:
                # Tenter de récupérer le message d'erreur depuis le JSON
                try:
                    data = resp.json()
                    return f"Erreur : {data.get('message', 'Impossible de faire cette action')}"
                except Exception:
                    return f"Impossible de faire '{action}'"
        except requests.RequestException as e:
            logger.error(f"Erreur serveur lors de l'action '{action}' : {e}")
            return f"Erreur serveur lors de l'action '{action}'"

    def terminer_manche(self, numero_table: int):
        try:
            resp = requests.put(f"{host}/manche/terminer/{numero_table}")
            resp.raise_for_status()
            message = str(resp.text).replace("\\n", "\n")

            from view.menu_info_table import InfoTableMenu

            return InfoTableMenu(numero_table, message, input_attente=True)
        except requests.HTTPError:
            try:
                message = f"Erreur serveur : {resp.json().get('detail', resp.text)}"
                return MenuManche(self.numero_table, self.pseudo, message=message, temps_attente=2)
            except Exception:
                message = f"Erreur serveur : {resp.text}"
                return MenuManche(self.numero_table, self.pseudo, message=message, temps_attente=2)
        except requests.RequestException as e:
            logger.error(f"Erreur serveur lors de la fermeture de la manche : {e}")
            message = f"Erreur serveur lors de la fermeture de la manche : {e}"
            return MenuManche(self.numero_table, self.pseudo, message=message, temps_attente=2)
