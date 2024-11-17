class Match:
    def __init__(
        self,
        match_id,
        equipe1,
        equipe2,
        score1,
        score2,
        date,
        ligue,
        region,
        stage,
        perso=False,  # Valeur par défaut pour `perso`
        cote_equipe1=2,
        cote_equipe2=2
    ):
        self.match_id = match_id
        self.equipe1 = equipe1
        self.equipe2 = equipe2
        self.score1 = score1
        self.score2 = score2
        self.date = date
        self.stage = stage
        self.region = region
        self.ligue = ligue
        self.perso = perso
        self.cote_equipe1 = cote_equipe1
        self.cote_equipe2 = cote_equipe2

        def __str__(self):
            """
            Retourne une représentation sous forme de chaîne de caractères des informations du joueur.

            Retour:
            -------
            str :
                Représentation du joueur avec toutes ses informations personnelles et statistiques.
            """
            return (f"Match({self.match_id}, ")
