class Joueur:
    """
    Classe représentant un Joueur

    Attributs
    ----------
    id_joueur : int
        identifiant
    pseudo : str
        pseudo du joueur
    mdp : str
        le mot de passe du joueur
    elo : int
        classement elo du joueur
    mail : str
        mail du joueur
    fan_pokemon : bool
        indique si le joueur est un fan de Pokemon
    """

    def __init__(self, pseudo, elo, mail, mdp=None, fan_pokemon=False, id_joueur=None):
        """Constructeur"""
        self.id_joueur = id_joueur
        self.pseudo = pseudo
        self.mdp = mdp
        self.elo = elo
        self.mail = mail
        self.fan_pokemon = fan_pokemon

    def __str__(self):
        """Permet d'afficher les informations du joueur"""
        return f"Joueur({self.pseudo}, elo: {self.elo})"

    def as_list(self) -> list[str]:
        """Retourne les attributs du joueur dans une liste"""
        return [self.pseudo, self.elo, self.mail, self.fan_pokemon]
