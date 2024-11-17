from tabulate import tabulate

from utils.log_decorator import log
from utils.securite import hash_password

from business_object.Utilisateur import Utilisateur
from dao.utilisateur_dao import UtilisateurDao
from dao.match_dao import MatchDao
from dao.tournoi_dao import TournoiDao
from dao.paris_dao import ParisDao

class UtilisateurService:
    """Classe contenant les méthodes de service des utilisateurs"""


    def __init__(self):
        self.match_dao = MatchDao() # créer ou enlever pour utilisateur
        self.tournoi_dao = TournoiDao() # créer ou enlever pour utilisateur
        self.pari_dao = ParisDao() # créer ou enlever pour utilisateur

    @log
    def creer_utilisateur(
        self, nom_utilisateur, mot_de_passe, email, tournois_crees=None, points=0, paris=None
    ) -> Utilisateur:
        """Création d'un utilisateur à partir de ses attributs"""

        nouveau_utilisateur = Utilisateur(
            nom_utilisateur=nom_utilisateur,
            mot_de_passe=hash_password(mot_de_passe, nom_utilisateur),
            email=email,
            tournois_crees=tournois_crees,
            points=points,
            paris=paris,
        )

        return nouveau_utilisateur if UtilisateurDao().creer(nouveau_utilisateur) else None

    @log
    def lister_tous(self, inclure_mot_de_passe=False) -> list[Utilisateur]:
        """Lister tous les utilisateurs
        Si inclure_mot_de_passe=True, les mots de passe seront inclus
        Par défaut, tous les mot_de_passe des utilisateurs sont à None
        """
        utilisateurs = UtilisateurDao().lister_tous()
        if not inclure_mot_de_passe:
            for j in utilisateurs:
                j.mot_de_passe = None
        return utilisateurs

    @log
    def trouver_par_id(self, id_utilisateur) -> Utilisateur:
        """Trouver un utilisateur à partir de son id"""
        return UtilisateurDao().trouver_par_id(id_utilisateur)

    @log
    def modifier(self, utilisateur) -> Utilisateur:
        """Modification d'un utilisateur"""

        utilisateur.mot_de_passe = hash_password(
            utilisateur.mot_de_passe, utilisateur.nom_utilisateur
        )
        return utilisateur if UtilisateurDao().modifier(utilisateur) else None

    @log
    def supprimer(self, utilisateur) -> bool:
        """Supprimer le compte d'un utilisateur"""
        return UtilisateurDao().supprimer(utilisateur)

    @log
    def afficher_tous(self) -> str:
        """Afficher tous les utilisateurs
        Sortie : Une chaine de caractères mise sous forme de tableau
        """
        entetes = ["nom_utilisateur", "age", "email", "est fan de Pokemon"]

        utilisateurs = UtilisateurDao().lister_tous()

        for j in utilisateurs:
            if j.nom_utilisateur == "admin":
                utilisateurs.remove(j)

        utilisateurs_as_list = [j.as_list() for j in utilisateurs]

        str_utilisateurs = "-" * 100
        str_utilisateurs += "\nListe des utilisateurs \n"
        str_utilisateurs += "-" * 100
        str_utilisateurs += "\n"
        str_utilisateurs += tabulate(
            tabular_data=utilisateurs_as_list,
            headers=entetes,
            tablefmt="psql",
            floatfmt=".2f",
        )
        str_utilisateurs += "\n"

        return str_utilisateurs

    @log
    def se_connecter(self, nom_utilisateur, mot_de_passe) -> Utilisateur:
        """Se connecter à partir de nom_utilisateur et mot_de_passe"""
        return UtilisateurDao().se_connecter(
            nom_utilisateur, hash_password(mot_de_passe, nom_utilisateur)
        )

    @log
    def nom_utilisateur_deja_utilise(self, nom_utilisateur) -> bool:
        """Vérifie si le nom_utilisateur est déjà utilisé
        Retourne True si le nom_utilisateur existe déjà en BDD"""
        utilisateurs = UtilisateurDao().lister_tous()
        return nom_utilisateur in [j.nom_utilisateur for j in utilisateurs]


    def afficher_paris_utilisateur(self, utilisateur_id: int):
        try:
            paris = self.pari_dao.trouver_par_utilisateur_id(utilisateur_id)
            for pari in paris:
                print(f"Pari ID: {pari.id}, Match: {pari.match_id}, Montant: {pari.montant}, Statut: {pari.statut}")
            return paris
        except Exception as e:
            logging.error(f"Erreur lors de la récupération des paris : {e}")
            return []

    def afficher_tournois_utilisateur(self, utilisateur_id: int):
        try:
            tournois = self.tournoi_dao.trouver_par_utilisateur_id(utilisateur_id)
            for tournoi in tournois:
                print(f"Tournoi ID: {tournoi.id}, Nom: {tournoi.nom}, Date: {tournoi.date}")
            return tournois
        except Exception as e:
            logging.error(f"Erreur lors de la récupération des tournois : {e}")
            return []

    def inscrire_pari(self, utilisateur_id: int, pari):
        try:
            pari.utilisateur_id = utilisateur_id
            success = self.pari_dao.creer(pari)
            if success:
                print("Pari ajouté avec succès.")
            return success
        except Exception as e:
            logging.error(f"Erreur lors de l'ajout du pari : {e}")
            return False

    def inscrire_tournoi(self, utilisateur_id: int, tournoi):
        try:
            tournoi.utilisateur_id = utilisateur_id
            success = self.tournoi_dao.creer(tournoi)
            if success:
                print("Tournoi ajouté avec succès.")
            return success
        except Exception as e:
            logging.error(f"Erreur lors de l'ajout du tournoi : {e}")
            return False

    def supprimer_pari(self, pari_id: int):
        try:
            success = self.pari_dao.supprimer(pari_id)
            if success:
                print(f"Pari avec ID {pari_id} supprimé avec succès.")
            return success
        except Exception as e:
            logging.error(f"Erreur lors de la suppression du pari : {e}")
            return False

    def supprimer_tournoi(self, tournoi_id: int):
        try:
            success = self.tournoi_dao.supprimer(tournoi_id)
            if success:
                print(f"Tournoi avec ID {tournoi_id} supprimé avec succès.")
            return success
        except Exception as e:
            logging.error(f"Erreur lors de la suppression du tournoi : {e}")
            return False

    def afficher_matchs_tournoi(self, tournoi_id: int):
        try:
            matchs = self.match_dao.trouver_par_tournoi_id(tournoi_id)
            for match in matchs:
                print(f"Match ID: {match.id}, Équipe 1: {match.equipe_1_id}, Équipe 2: {match.equipe_2_id}, Score: {match.score}")
            return matchs
        except Exception as e:
            logging.error(f"Erreur lors de la récupération des matchs du tournoi {tournoi_id} : {e}")
            return []

    def ajouter_match_au_tournoi(self, tournoi_id: int, match):
        try:
            match.tournoi_id = tournoi_id
            success = self.match_dao.creer(match)
            if success:
                print("Match ajouté au tournoi avec succès.")
            return success
        except Exception as e:
            logging.error(f"Erreur lors de l'ajout du match au tournoi {tournoi_id} : {e}")
            return False

    def afficher_statistiques_utilisateur(self, utilisateur_id: int):
        try:
            paris = self.pari_dao.trouver_par_utilisateur_id(utilisateur_id)
            tournois = self.tournoi_dao.trouver_par_utilisateur_id(utilisateur_id)
            print(f"Statistiques de l'utilisateur {utilisateur_id} :")
            print(f"- Nombre de paris : {len(paris)}")
            print(f"- Nombre de tournois : {len(tournois)}")
            return {
                "nombre_paris": len(paris),
                "nombre_tournois": len(tournois)
            }
        except Exception as e:
            logging.error(f"Erreur lors de la récupération des statistiques de l'utilisateur {utilisateur_id} : {e}")
            return {}
