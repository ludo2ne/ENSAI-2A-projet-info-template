from tabulate import tabulate

from utils.log_decorator import log
from utils.securite import hash_password

from src.utils.singleton import Singleton
from src.business_object.Utilisateur import Utilisateur
from src.business_object.Equipe import Equipe
from src.business_object.Tournoi import Tournoi
from src.business_object.Pari import Pari


class UtilisateurService(metaclass=Singleton):
    def creer(Utilisateur):
        pass

    def lister_tous():
        pass

    def trouver_par_id(id: int):
        pass

    def modifier(Utilisateur):
        pass

    def supprimer(Utilisateur):
        pass

    def afficher_tous():
        pass

    def se_connecter(pseudo: str, mdp: str):
        pass

    def pseudo_deja_utilise(pseudo: str):
        pass

    def participer_tournoi(id_tournoi: str, Equipe):
        pass

    def gerer_tournoi(Tournoi):
        pass

    def afficher_paris_actuels():
        pass

    def creer_tournoi(Tournoi):
        pass

    def placer_pari(Pari):
        pass

    def afficher_historique_paris():
        pass
