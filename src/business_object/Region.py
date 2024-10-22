class Region:
    """
    Classe représentant un Utilisateur

    Attributs
    ----------
    nom_region : int
        région
    equipe : list[Equipe]
        liste d'équipe
    tournois_régionaux :  # pas compris


    """

    def __init__(self, nom_region, equipe, tournois_régionaux):
        """Constructeur"""
        self.nom_region = nom_region
        self.equipe = equipe
        self.tournois_régionaux = tournois_régionaux
