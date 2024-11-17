from view.session import Session
from dao.paris_dao import ParisDao
from business_object.Pari import Pari
from dao.utilisateur_dao import UtilisateurDao
from dao.equipe_dao import EquipeDao
from dao.match_dao import MatchDao
from service.equipe_service import EquipeService
from service.match_service import MatchService


class ParisService:

    def __init__(self):
        self.utilisateur_dao = UtilisateurDao()
        self.equipe_dao = EquipeDao()
        self.match_dao = MatchDao()

    def instancier_paris(self, paris_bdd):
        equipe_service = EquipeService()
        match_service = MatchService
        match = self.match_dao.trouver_par_id_match(paris_bdd["id_match"])
        equipe = self.equipe_dao.trouver_par_nom_equipe(paris_bdd["nom_equipe"])  # A coder
        equipe_service.instancier(equipe)
        match_service.instancier(match)
        pari = Pari(
            id_pari=paris_bdd["id_pari"],
            match=match,
            equipe=equipe,
            statut=paris_bdd["statut"],
            montant=paris_bdd["montant"],
        )
        return pari

    def afficher_infos_paris(self):
        "Affiche les paris d'un utilisateur"
        nom_utilisateur = Session().utilisateur.nom_utilisateur
        paris = ParisDao().afficher_infos_paris(nom_utilisateur)
        if paris == []:
            print(f"{nom_utilisateur}, vous n'avez pas fait de paris")
        else:
            liste_paris = []
            for pari in paris:
                liste_paris.append(self.instancier_paris(pari))
            print(liste_paris)
        return liste_paris

    def parier(self, match, equipe, montant):  # créer un menu dans la view
        "Enregistre le paris de l'utilisateur dans la base de données"
        if not isinstance(match, str):
            raise TypeError("Match doit être une chaîne de charactères")
        if not isinstance(montant, int):
            raise TypeError("Le montant doit être un entier")
        nom_utilisateur = Session().utilisateur.nom_utilisateur
        ParisDao().ajouter_un_pari(nom_utilisateur, match, equipe, montant)

    def terminer_paris(pari, gagnant):
        "Donne le résultat du paris quand le match a été joué"
        if not isinstance(pari, Pari):
            raise TypeError("Le pari doit être de type Pari")
        if pari.equipe == gagnant:
            pari.statut = "Remporté"
        else:
            pari.statut = "Perdu"
        ParisDao().changer_statut(pari.statut)

    def supprimer_paris(pari):
        "Supprime un pari"
        if not isinstance(pari, Pari):
            raise TypeError("Le pari doit être de type Pari")
        ParisDao().supprimer_paris(pari)
