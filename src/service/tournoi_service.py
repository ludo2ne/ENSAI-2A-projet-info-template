from view.session import Session
from dao.tournoi_dao import TournoiDao
from business_object.Tournoi import Tournoi
from dao.utilisateur_dao import UtilisateurDao
from dao.equipe_dao import EquipeDao
from dao.match_dao import MatchDao
from service.equipe_service import EquipeService
from service.match_service import MatchService


class TournoiService:

    def __init__(self):
        self.utilisateur_dao = UtilisateurDao()
        self.equipe_dao = EquipeDao()
        self.match_dao = MatchDao()

    def instancier_tournoi(self, tournois_bdd):
        equipe_service = EquipeService()
        match_service = MatchService()
        match = self.match_dao.trouver_par_id_match(paris_bdd["id_match"])
        equipe = self.equipe_dao.trouver_par_nom_equipe(paris_bdd["nom_equipe"])  # A coder
        equipe_service.instancier(equipe)
        match_service.instancier(match)
        tournoi = Tournoi(
            id_tournoi=tournois_bdd["id_tournoi"],
            officiel=tournois_bdd["officiel"]
        )
        return tournoi

    def afficher_infos_tournois(self):
        "Affiche les tournois d'un utilisateur"
        nom_utilisateur = Session().utilisateur.nom_utilisateur
        tournois = tournoisDao().afficher_infos_tournois(nom_utilisateur)
        if tournois == []:
            print(f"{nom_utilisateur}, vous n'avez pas fait de tournois")
        else:
            liste_tournois = []
            for tournoi in tournois:
                liste_tournois.append(self.instancier_tournois(tournoi))
            print(liste_tournois)
        return liste_tournois

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
