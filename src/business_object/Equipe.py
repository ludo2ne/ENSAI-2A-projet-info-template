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
        equipe_score,
        boost_stole,
        date,
        region,
        ligue,
        stage,
        # Paramètres avec valeurs par défaut pour les statistiques par match
        shots_par_match=1,  # valeur par défaut 1
        goals_par_match=1,  # valeur par défaut 1
        saves_par_match=1,  # valeur par défaut 1
        assists_par_match=1,  # valeur par défaut 1
        score_par_match=1,  # valeur par défaut 1
        demo_inflige_par_match=1,  # valeur par défaut 1
        indice_de_pression=1,
        indice_performance=1
    ):
        # Initialisation des attributs principaux (super() appelé si nécessaire)
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
            date,
            region,
            ligue,
            stage,
        )

        # Initialisation des attributs spécifiques à Equipe
        self.equipe_score = equipe_score
        self.boost_stole = boost_stole

        # Initialisation des statistiques par match
        self.shots_par_match = shots_par_match
        self.goals_par_match = goals_par_match
        self.saves_par_match = saves_par_match
        self.assists_par_match = assists_par_match
        self.score_par_match = score_par_match
        self.demo_inflige_par_match = demo_inflige_par_match

    def __str__(self):
        """
        Retourne une représentation sous forme de chaîne de caractères des informations de l'équipe.
        """
        return (f"Equipe({self.equipe_nom}, "
                f"Match ID: {self.match_id}, "
                f"Shots: {self.shots}, "
                f"Goals: {self.goals}, "
                f"Saves: {self.saves}, "
                f"Assists: {self.assists}, "
                f"Score: {self.score}, "
                f"Shooting Percentage: {self.shooting_percentage}, "
                f"Time Offensive Third: {self.time_offensive_third}, "
                f"Time Defensive Third: {self.time_defensive_third}, "
                f"Time Neutral Third: {self.time_neutral_third}, "
                f"Demo Infligé: {self.demo_inflige}, "
                f"Demo Reçu: {self.demo_recu}, "
                f"Equipe Score: {self.equipe_score}, "
                f"Boost Stolen: {self.boost_stole}, "
                f"Date: {self.date}, "
                f"Region: {self.region}, "
                f"Ligue: {self.ligue}, "
                f"Stage: {self.stage}, "
                f"Shots per Match: {self.shots_par_match}, "
                f"Goals per Match: {self.goals_par_match}, "
                f"Saves per Match: {self.saves_par_match}, "
                f"Assists per Match: {self.assists_par_match}, "
                f"Score per Match: {self.score_par_match}, "
                f"Demo Infligé per Match: {self.demo_inflige_par_match})")


# Supposons que la classe EntiteSportive et Equipe aient été définies comme ci-dessus.
