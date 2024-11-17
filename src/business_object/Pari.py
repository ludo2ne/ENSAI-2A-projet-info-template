from business_object.Match import Match
from business_object.Equipe import Equipe


class Pari:
    """
    Définit un pari pour un joueur
    Parameters:
    ---------------

    id_pari: int
        Identifiant du pari

    match: Match
        Match sur lequel est fait le pari

    equipe: Equipe
        Equipe sur laquelle le joueur place son pari

    statut: str
        Etat du pari: "Remporté", "En cours", "Perdu"

    montant: int
        Montant mis en jeu dans le pari
    """

    def __init__(self, id_pari, match, equipe, statut, montant):

        if not isinstance(id_pari, int):
            raise TypeError("id_pari doit être de type int")
        if not isinstance(match, Match):
            raise TypeError("match doit être de type Match")
        if not isinstance(equipe, Equipe):
            raise TypeError("equipe doit être de type Equipe")
        if not isinstance(statut, str):
            raise TypeError("statut doit être de type str")
        if not isinstance(montant, float):
            raise TypeError("montant doit être de type float")

        self.id_pari = id_pari
        self.match = match
        self.equipe = equipe
        self.statut = statut
        self.montant = montant

    def __str__(self):
        """Affiche les informations du pari"""
        return f"Vous avez parié {self.montant} pour {self.equipe.equipe_nom} dans le match {self.match.id_match}"

    def calculer_gains(self):
        """Donne les gains du pari"""
        if self.equipe.equipe_winner:
            gain = self.montant * self.match.cote_match
        else:
            gain = -self.montant
        return gain
