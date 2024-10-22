class MatchPerso:
    """
    Classe représentant un Utilisateur

    Attributs
    ----------
    id_match : str
        id_match
    id_tounoi : str
        creer quand tu créer un tounoi
    equipe1 :

    equipe2 :

    score1:int

    score2:int

    date: Date

    lieu: str

    etat : str
    en cours ou pas


    """

    def __init__(self, id_match, id_tounoi, equipe1,equipe2,score1,score2,date,lieu,etat):
        """Constructeur"""
        self.id_match = id_match
        self.id_tounoi = id_tounoi
        self.equipe1 = equipe1
        self.equipe2 = equipe2
        self.score1 = score1
        self.score2 = score2
        self.date = date
        self.lieu = lieu
        self.etat = etat

    def afficher_détails(self):
        """Permet d'afficher les informations de l'equipe"""

        return f"Match : {self.equipe1} VS {self.equipe2}, Score: {self.score1}-{self.score2},
         Date: {self.date}, Lieu: {self.lieu}, État: {self.etat}"

    def mettre_a_jour_score(self,score1,score2):
        # Bizarre psoer des question sur si on met dans matchdao forme speciale ou meme forme que match et l'utilisateur doit ajouter 
