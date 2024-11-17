from business_object.Pari import Pari
from business_object.Tournoi import Tournoi


class Utilisateur:
    """
    Classe représentant un Utilisateur

    Attributs
    ----------
    nom_utilisateur : str
        Pseudo de l'utilisateur

    mot_de_passe : str
        Mot de passe de l'utilisateur

    email : str
        Email de l'utilisateur

    tournois_crées: list[Tournoi]
        Liste des ids de tournois créés par l'utilisateur"

    paris: list[Pari]
        Liste des paris fait par l'utilisateur

    points: int
        Nombre de points de l'utilisateur (pour faire des paris)
    """

    def __init__(
        self, nom_utilisateur, mot_de_passe, email, tournois_crees=None, paris=None, points=0
    ):
        """Constructeur"""
        if not isinstance(nom_utilisateur, str):
            raise TypeError("nom_utilisateur doit être de type str")
        if not isinstance(mot_de_passe, str):
            raise TypeError("mot_de_passe doit être de type str")
        if not isinstance(email, str):
            raise TypeError("email doit être de type str")
        if tournois_crees:
            if not isinstance(tournois_crees, list):
                raise TypeError("tournois_crees doit être de type list")
            for tournoi in tournois_crees:
                if not isinstance(tournoi, Tournoi):
                    raise TypeError("tournoi doit être de type Tournoi")
        if paris:
            if not isinstance(paris, list):
                raise TypeError("paris doit être de type list")
            for i in paris:
                if not isinstance(i, Pari):
                    raise TypeError("chaque pari doit être de type Pari")
        if not isinstance(points, int):
            raise TypeError("points doit être de type int")

        self.nom_utilisateur = nom_utilisateur
        self.mot_de_passe = mot_de_passe
        self.email = email
        self.tournois_crees = tournois_crees
        self.paris = paris  # regarder pour prendre les logs
        self.points = points

    def __str__(self):
        """Permet d'afficher les informations du joueur"""
        if self.tournois_crees:
            tournois_str = ", ".join([tournoi.nom_tournoi for tournoi in self.tournois_crees])
        else:
            tournois_str = "Aucun"
        if self.paris:
            paris_str = ", ".join([f"{pari.id_pari}" for pari in self.paris])
        else:
            paris_str = "Aucun"
        return (
            f"identifiant:{self.nom_utilisateur}, "
            f"mdp:{self.mot_de_passe}, "
            f"email:{self.email}, "
            f"tournois:[{tournois_str}], "
            f"paris:[{paris_str}], "
            f"points:{self.points}"
        )
        return f"identifiant:{self.pseudo}, mdp:{self.mdp}, mail:{self.mail}"
        f"tournois:{self.tournois_crees}, paris:{self.paris}, points:{self.points})"
