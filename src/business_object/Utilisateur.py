from Pari import Pari


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
        Liste des tournois créés par l'utilisateur"

    paris: list[Pari]
        Liste des paris fait par l'utilisateur

    points: int
        Nombre de points de l'utilisateur (pour faire des paris)
    """

    def __init__(self, nom_utilisateur, mot_de_passe, email, tournois_crees, paris, points):
        """Constructeur"""
        if not isinstance(nom_utilisateur, str):
            raise TypeError("nom_utilisateur doit être de type str")
        if not isinstance(mot_de_passe, str):
            raise TypeError("mot_de_passe doit être de type str")
        if not isinstance(email, str):
            raise TypeError("email doit être de type str")
        if not isinstance(tournois_crees, list):
            raise TypeError("tournois_crees doit être de type list")
        if not isinstance(paris, Pari):
            raise TypeError("paris doit être de type Pari")
        if not isinstance(points, int):
            raise TypeError("points doit être de type int")

        self.nom_utilisateur = nom_utilisateur
        self.mot_de_passe = mot_de_passe
        self.email = email
        self.tournois_crees = tournois_crees
        self.paris = paris # regarder pour prendre les logs
        self.points = points

    def __str__(self):
        """Permet d'afficher les informations du joueur"""
        return f"Joueur({self.nom_utilisateur}"
