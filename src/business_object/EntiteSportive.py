from abc import ABC, abstractmethod


class EntiteSportive(ABC):
    """
    Classe abstraite représentant une entité sportive avec des statistiques de match.

    Attributs:
    ----------
    match_id : int
        Identifiant unique du match.

    equipe_nom : str
        Nom de l'équipe.

    shots : int
        Nombre de tirs effectués par l'entité sportive.

    goals : int
        Nombre de buts marqués par l'entité sportive.

    saves : int
        Nombre d'arrêts effectués par l'entité sportive.

    assists : int
        Nombre de passes décisives réalisées par l'entité sportive.

    score : int
        Score total obtenu par l'entité sportive dans le match.

    shooting_percentage : float
        Pourcentage de réussite des tirs (nombre de buts par rapport au nombre de tirs).

    time_offensive_third : float
        Temps passé dans le tiers offensif du terrain par l'entité sportive.

    time_defensive_third : float
        Temps passé dans le tiers défensif du terrain par l'entité sportive.

    time_neutral_third : float
        Temps passé dans le tiers neutre du terrain par l'entité sportive.

    demo_inflige : int
        Nombre de démolitions infligées à l'équipe adverse.

    demo_recu : int
        Nombre de démolitions reçues par l'entité sportive.

    goal_participation : float
        Taux de participation aux buts, calculé comme la somme des buts et des
        passes décisives divisée par le nombre total de buts marqués par
        l'équipe.
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
    ):

        self.match_id = match_id
        self.equipe_nom = equipe_nom
        self.shots = shots
        self.goals = goals
        self.saves = saves
        self.assists = assists
        self.score = score
        self.shooting_percentage = shooting_percentage
        self.time_offensive_third = time_offensive_third
        self.time_defensive_third = time_defensive_third
        self.time_neutral_third = time_neutral_third
        self.demo_inflige = demo_inflige
        self.demo_recu = demo_recu
        self.goal_participation = goal_participation

    @abstractmethod
    def __str__(self):
        """
        Méthode abstraite à implémenter dans les classes dérivées.

        Cette méthode doit retourner une représentation sous forme de chaîne de
        caractères de l'entité sportive.
        """
        pass
