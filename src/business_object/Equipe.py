from business_object.EntiteSportive import EntiteSportive


class Equipe(EntiteSportive):
    """
    Classe représentant une équipe dans un match, héritant des statistiques d'une entité sportive.

    Attributs hérités de EntiteSportive:
    ------------------------------------
    match_id : int
        Identifiant unique du match.

    equipe_nom : str
        Nom de l'équipe ou de l'entité sportive.

    shots : int
        Nombre de tirs effectués par l'équipe.

    goals : int
        Nombre de buts marqués par l'équipe.

    saves : int
        Nombre d'arrêts effectués par l'équipe.

    assists : int
        Nombre de passes décisives réalisées par l'équipe.

    score : int
        Score total obtenu par l'équipe dans le match.

    shooting_percentage : float
        Pourcentage de réussite des tirs (nombre de buts par rapport au nombre de tirs).

    time_offensive_third : float
        Temps passé dans le tiers offensif du terrain par l'équipe.

    time_defensive_third : float
        Temps passé dans le tiers défensif du terrain par l'équipe.

    time_neutral_third : float
        Temps passé dans le tiers neutre du terrain par l'équipe.

    demo_inflige : int
        Nombre de démolitions infligées à l'équipe adverse par l'équipe.

    demo_recu : int
        Nombre de démolitions reçues par l'équipe.

    goal_participation : float
        Taux de participation aux buts, calculé comme la somme des buts et des
        passes décisives divisée par le nombre total de buts marqués par
        l'équipe.

    Nouveaux attributs propres à Equipe:
    ------------------------------------
    equipe_score : int
        Score total obtenu par l'équipe dans le match.

    equipe_winner : bool
        Indicateur si l'équipe a gagné le match (True pour gagnante, False pour perdante).

    region : str
        Région géographique à laquelle l'équipe appartient.

    ligue : str
        Ligue ou division dans laquelle l'équipe évolue.

    stage : str
        Étape du tournoi ou de la compétition où se situe l'équipe
        (ex : poule, quart de finale, etc.).
    """

    def __init__(
        self,
        match_id,
        equipe_nom,
        shots,
        goals,
        saves,
        assists,
        score,
        shooting_percentage,
        time_offensive_third,
        time_defensive_third,
        time_neutral_third,
        demo_inflige,
        demo_recu,
        goal_participation,
        equipe_score,
        equipe_winner,
        region,
        ligue,
        stage,
    ):

        # Appel du constructeur parent (EntiteSportive)
        super().__init__(
            match_id,
            equipe_nom,
            shots,
            goals,
            saves,
            assists,
            score,
            shooting_percentage,
            time_offensive_third,
            time_defensive_third,
            time_neutral_third,
            demo_inflige,
            demo_recu,
            goal_participation,
        )

        # Initialisation des nouveaux attributs spécifiques à la classe Equipe
        self.equipe_score = equipe_score
        self.equipe_winner = equipe_winner
        self.region = region # autant créer une classe match non?
        self.ligue = ligue
        self.stage = stage

    def __str__(self):
        """
        Retourne une représentation sous forme de chaîne de caractères des informations de l'équipe.

        Retour:
        -------
        str :
            Représentation de l'équipe avec son nom, son score et sa région.
        """
        return f"Equipe({self.equipe_nom}, Score: {self.equipe_score}, Région: {self.region}, Vainqueur: {'Oui' if self.equipe_winner else 'Non'})"
