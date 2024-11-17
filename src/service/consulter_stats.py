from utils.singleton import Singleton
from dao.equipe_dao import EquipeDao
from dao.joueur_dao import JoueurDao
from dao.match_dao import MatchDao
from business_object.joueur import Joueur
from business_object.Equipe import Equipe


class ConsulterStats(metaclass=Singleton):
    """Une classe service qui affiche les statistiques par joueur, équipe et match"""

    @staticmethod
    def stats_par_match(total, n):
        """Calculer la moyenne par match tout en évitant la division par zéro"""
        return total / n if n > 0 else 0

    def stats_joueurs(self, nom_joueur):
        """Une fonction qui permet d'afficher les statistiques par joueur"""
        if not isinstance(nom_joueur, str):
            raise TypeError("nom_joueur doit être une instance de str")

        joueurdao = JoueurDao()
        joueur_data = joueurdao.obtenir_par_nom(nom_joueur)

        # Si aucun joueur n'est trouvé
        if not joueur_data:
            raise ValueError(f"Aucun joueur nommé {nom_joueur} n'a été trouvé.")

        n = joueurdao.nombre_match(nom_joueur)

        if n == 0:
            raise ValueError(f"Aucun match trouvé pour le joueur {nom_joueur}.")

        # Dictionnaire pour simplifier l'indice régional
        regional_indices = {
            "EU": 1,
            "NA": 1,
            "SAM": 0.9,
            "MENA": 0.9,
            "OCE": 0.5,
            "APAC": 0.5,
            "SSA": 0.3,
        }

        collonne = [
            "goals",
            "assists",
            "score",
            "shots",
            "shooting_percentage",
            "demo_inflige",
            "demo_recu",
            "goal_participation",
            "saves",
            "indice_offensif",
            "indice_performance",
            "time_offensive_third",
            "time_defensive_third",
            "time_neutral_third",
        ]
        stat_affiché = joueurdao.moyennes_statistiques(nom_joueur, collonne)

        print(
            f"Statistiques de {joueur_data.nom}, depuis le début de la saison :\n"
            f"Nombre moyen de buts marqués par match : {stat_affiché['goals']}\n"
            f"Nombre moyen de passes décisives par match : {stat_affiché['assists']}\n"
            f"Score moyen par match : {stat_affiché['score']}\n"
            f"Nombre moyen de tirs par match : {stat_affiché['shots']}\n"
            f"Pourcentage moyen des tirs effectués convertis en buts : {stat_affiché['shooting_percentage']}\n"
            f"Nombre moyen d'arrêts par match : {stat_affiché['saves']}\n"
            f"Performance moyenne : {stat_affiché['indice_performance']}\n"
            f"Participation aux buts au cours de la saison : {stat_affiché['goal_participation']}\n"
            f"Moyennes de démolitions infligées : {stat_affiché['demo_inflige']}\n"
            f"Moyennes de démolitions reçues par match : {stat_affiché['demo_recu']}\n"
            f"Apport offensif moyen : {stat_affiché['indice_offensif']}\n"
            f"Temps moyen passé en attaque : {stat_affiché['time_offensive_third']} secondes\n"
            f"Temps moyen passé en défense : {stat_affiché['time_defensive_third']} secondes"
        )

    # Note pour les vues : Les stats à afficher dans la vue sont : goals, goals par match, assists, assists par match,
    # saves, saves par match, shots, shots par match, score, score par match, demo infligées, demo infligées par match,
    # indice de performance, indice offensif, pourcentage de tirs

    def stats_equipe(self, nom_equipe):
        """Une fonction qui permet d'afficher les statistiques par équipe"""

        equipedao = EquipeDao()
        equipe_data = equipedao.obtenir_par_nom(nom_equipe)
        n = equipedao.nombre_match(nom_equipe)
        if n == 0:
            raise ValueError(f"Aucun match n'a été trouvé pour l'équipe {nom_equipe}.")

        # indice de pression TODO -> besoin du nombre de boosts volés, du temps passé dans la partie de terrain adverse, et des démolitions

        collonne = [
            "goals",
            "assists",
            "score",
            "shots",
            "shooting_percentage",
            "demo_inflige",
            "demo_recu",
            "saves",
            "boost_stole",
            "time_offensive_third",
            "time_defensive_third",
            "time_neutral_third",
            "indice_de_pression",
            "indice_performance",
        ]

        stat_affiché = equipedao.moyennes_statistiques(nom_equipe, collonne)

        print(
            f"Statistiques de {nom_equipe}, depuis le début de la saison :\n"
            f"Nombre moyen de buts marqués par match : {stat_affiché['goals']}\n"
            f"Nombre moyen de passes décisives par match : {stat_affiché['assists']}\n"
            f"Score moyen par match : {stat_affiché['score']}\n"
            f"Nombre moyen de tirs par match : {stat_affiché['shots']}\n"
            f"Pourcentage moyen des tirs effectués convertis en buts : {stat_affiché['shooting_percentage']}\n"
            f"Nombre moyen d'arrêts par match : {stat_affiché['saves']}\n"
            f"Performance moyenne : {stat_affiché['indice_performance']}\n"
            f"Moyennes de démolitions infligées : {stat_affiché['demo_inflige']}\n"
            f"Moyennes de démolitions reçues par match : {stat_affiché['demo_recu']}\n"
            f"Temps moyen passé en attaque : {stat_affiché['time_offensive_third']} secondes\n"
            f"Temps moyen passé en défense : {stat_affiché['time_defensive_third']} secondes\n"
            f"Temps moyen passé en zone neutre : {stat_affiché['time_neutral_third']} secondes\n"
            f"Indice de pression moyen : {stat_affiché['indice_de_pression']}\n"
        )

    def stats_matchs_joueurs(self, nom_joueur):
        """Renvoie toutes les données par match pour un joueur spécifié, ainsi que celles des autres joueurs"""
        if not isinstance(nom_joueur, str):
            raise TypeError("Le nom du joueur doit être une chaîne de caractères.")

        joueurdao = JoueurDao()
        matchdao = MatchDao()

        # Vérifier si le joueur existe
        joueur_data = joueurdao.obtenir_par_nom(nom_joueur)
        if not joueur_data:
            raise ValueError(f"Aucun joueur nommé {nom_joueur} trouvé.")

        # Obtenir les IDs de tous les matchs joués par le joueur
        id_matchs = matchdao.trouver_match_id_par_joueur(nom_joueur)
        if not id_matchs:
            raise ValueError(f"Aucun match trouvé pour le joueur {nom_joueur}.")

        # Obtenir les statistiques par match pour le joueur et pour tous les autres joueurs
        stats_details = []
        for match_id in id_matchs:
            match_stats = matchdao.obtenir_stats_match_joueur(nom_joueur, match_id)

            # Il faut encore créer la fonction obtenir_stats_match_joueur
            # Exemple de structure de données attendue de la fonction DAO pour un match donné :
            # match_stats = {"goals": 2, "assists": 1, "shots": 5, "saves": 3, "score": 500, "demo_inflige": 1}

            match_detail = {
                "match_id": match_id,
                "goals": match_stats.get("goals", 0),
                "assists": match_stats.get("assists", 0),
                "shots": match_stats.get("shots", 0),
                "saves": match_stats.get("saves", 0),
                "score": match_stats.get("score", 0),
                "demo_inflige": match_stats.get("demo_inflige", 0),
                "pourcentage_tirs": self.stats_par_match(
                    match_stats.get("goals", 0), match_stats.get("shots", 0)
                ),
            }

            # Récupérer aussi les stats des autres joueurs participant à ce match
            joueurs_match = matchdao.trouver_joueurs_par_match(
                match_id
            )  # Cette fonction retourne la liste des noms des joueurs du match
            for joueur_nom in joueurs_match:
                if joueur_nom != nom_joueur:  # Ignorer le joueur demandé
                    other_player_stats = matchdao.obtenir_stats_match_joueur(joueur_nom, match_id)
                    match_detail[f"{joueur_nom}_goals"] = other_player_stats.get("goals", 0)
                    match_detail[f"{joueur_nom}_assists"] = other_player_stats.get("assists", 0)
                    match_detail[f"{joueur_nom}_shots"] = other_player_stats.get("shots", 0)
                    match_detail[f"{joueur_nom}_saves"] = other_player_stats.get("saves", 0)
                    match_detail[f"{joueur_nom}_score"] = other_player_stats.get("score", 0)
                    match_detail[f"{joueur_nom}_demo_inflige"] = other_player_stats.get(
                        "demo_inflige", 0
                    )

            stats_details.append(match_detail)

        return stats_details

    def stats_matchs_equipe(self, nom_equipe):
        """Renvoie toutes les données par match pour une équipe spécifiée, ainsi que celles des autres équipes"""
        if not isinstance(nom_equipe, str):
            raise TypeError("Le nom de l'équipe doit être une chaîne de caractères.")

        equipedao = EquipeDao()
        matchdao = MatchDao()

        # Vérifier si l'équipe existe
        equipe_data = equipedao.obtenir_par_nom(nom_equipe)
        if not equipe_data:
            raise ValueError(f"Aucune équipe nommée {nom_equipe} trouvée.")

        # Obtenir les IDs de tous les matchs joués par l'équipe
        id_matchs = matchdao.trouver_match_id_par_equipe(nom_equipe)
        if not id_matchs:
            raise ValueError(f"Aucun match trouvé pour l'équipe {nom_equipe}.")

        # Obtenir les statistiques par match pour l'équipe et pour toutes les autres équipes
        stats_details = []
        for match_id in id_matchs:
            match_stats = matchdao.obtenir_stats_match_equipe(nom_equipe, match_id)

            # Exemple de structure de données attendue de la fonction DAO pour un match donné :
            # match_stats = {"goals": 4, "assists": 2, "shots": 10, "saves": 5, "score": 1500, "demo_inflige": 2}

            match_detail = {
                "match_id": match_id,
                "goals": match_stats.get("goals", 0),
                "assists": match_stats.get("assists", 0),
                "shots": match_stats.get("shots", 0),
                "saves": match_stats.get("saves", 0),
                "score": match_stats.get("score", 0),
                "demo_inflige": match_stats.get("demo_inflige", 0),
                "pourcentage_tirs": self.stats_par_match(
                    match_stats.get("goals", 0), match_stats.get("shots", 0)
                ),
            }

            # Récupérer aussi les stats des autres équipes participant à ce match
            equipes_match = matchdao.trouver_equipes_par_match(
                match_id
            )  # Cette fonction retourne la liste des équipes du match
            for equipe_nom in equipes_match:
                if equipe_nom != nom_equipe:  # Ignorer l'équipe demandée
                    other_team_stats = matchdao.obtenir_stats_match_equipe(equipe_nom, match_id)
                    match_detail[f"{equipe_nom}_goals"] = other_team_stats.get("goals", 0)
                    match_detail[f"{equipe_nom}_assists"] = other_team_stats.get("assists", 0)
                    match_detail[f"{equipe_nom}_shots"] = other_team_stats.get("shots", 0)
                    match_detail[f"{equipe_nom}_saves"] = other_team_stats.get("saves", 0)
                    match_detail[f"{equipe_nom}_score"] = other_team_stats.get("score", 0)
                    match_detail[f"{equipe_nom}_demo_inflige"] = other_team_stats.get(
                        "demo_inflige", 0
                    )

            stats_details.append(match_detail)

        return stats_details

    def stats_matchs(self, nom_equipe="Non renseigné", nom_joueur="Non renseigné"):
        """Renvoie les statistiques par match pour un joueur et/ou une équipe et inclut les autres joueurs et équipes"""
        if not isinstance(nom_equipe, str) or not isinstance(nom_joueur, str):
            raise TypeError(
                "Les noms d'équipe et de joueur doivent être des chaînes de caractères."
            )
        if nom_equipe == "Non renseigné" and nom_joueur == "Non renseigné":
            raise ValueError("Il faut renseigner au moins un nom d'équipe ou de joueur.")

        stats_joueur = []
        stats_equipe = []

        # Obtenir les statistiques par joueur
        if nom_joueur != "Non renseigné":
            stats_joueur = self.stats_matchs_joueurs(nom_joueur)

        # Obtenir les statistiques par équipe
        if nom_equipe != "Non renseigné":
            stats_equipe = self.stats_matchs_equipe(nom_equipe)

        # Fusionner les résultats
        stats_combined = stats_joueur + stats_equipe

        return stats_combined
