import os

import requests

from view.session import Session
from view.vue_abstraite import VueAbstraite
from service.joueur_service import JoueurService

host = os.environ["HOST_WEBSERVICE"]


class InfosSessionVue(VueAbstraite):
    def choisir_menu(self):
        session = Session()
        joueur = JoueurService().trouver_par_id(session.id)

        res = "\n==================== INFOS SESSION ====================\n"

        # A) Joueur connecté dans CE terminal
        if joueur is None:
            res += "Aucun joueur connecté dans ce terminal.\n"
            return InfosSessionVue(res, temps_attente=3)

        res += f"Joueur connecté : {joueur.pseudo} ({joueur.credit} crédits)\n"
        res += f"Début connexion : {getattr(joueur, 'debut_connexion', 'N/A')}\n\n"

        # A) Joueurs connectés dans CE terminal
        res += "Joueurs connectés dans ce terminal :\n"
        res += "--------------------------------------------------------\n"
        for j in Session.joueurs_connectes:
            debut = getattr(j, "debut_connexion", "Non connecté")
            res += f"- {j.pseudo} : {j.credit} crédits (connexion : {debut})\n"

        res += "\n"

        # B) Tous les joueurs de la table (depuis la base)
        if joueur.table:
            table_id = joueur.table.numero_table
            try:
                url = f"{host}/table/{table_id}/joueurs/"
                req = requests.get(url)

                if req.status_code == 200:
                    joueurs_table = req.json()

                    res += f"Joueurs de la table {table_id} (depuis la base) :\n"
                    res += "--------------------------------------------------------\n"
                    for j in joueurs_table:
                        res += f"- {j['pseudo']} : {j['credit']} crédits\n"
                else:
                    res += f"Impossible de récupérer les joueurs de la table (code {req.status_code})\n"
            except Exception as e:
                res += f"Erreur API : {e}\n"

        return InfosSessionVue(res, temps_attente=3)
