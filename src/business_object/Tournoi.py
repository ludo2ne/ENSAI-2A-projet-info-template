class Tournoi:
    """
    Classe représentant un Utilisateur

    Attributs
    ----------
    id_tournoi : str
        région
    nom_tournoi : str
        liste d'équipe
    equipes :  List[Equipe]


    """

    def __init__(self, id_tournoi, nom_tournoi, equipes):
        """Constructeur"""
        self.id_tournoi = id_tournoi
        self.nom_tournoi = nom_tournoi
        self.equipes = equipes

    def inscrire_equipe(self, equipe):

        self.equipes.append(equipe)
        return self.equipes

    def suivre_resultats(self,Match_preso)
