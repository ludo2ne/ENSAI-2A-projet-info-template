import requests,json # truc à importer  #la docu en roue libre donc...
import pandas as pd
import os
import dotenv
from dao.joueur_dao import JoueurDao
from business_object.joueur import Joueur
from dao.equipe_dao import EquipeDao
from business_object.Equipe import Equipe
from business_object.Match import Match

from dao.match_dao import MatchDao
# Charger les variables d'environnement
dotenv.load_dotenv()

regional_indices = {
            "EU": 1, "NA": 1, "SAM": 0.9, "MENA": 0.9,
            "OCE": 0.5, "APAC": 0.5, "SSA": 0.3, "INT":1
        }

class API:
    def __init__(self, base_url):
        self.base_url = base_url

    def recup_page(self, endpoint, params=None):
        """Retrieve data from a given API endpoint."""
        url = self.base_url + endpoint
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: Unable to fetch data from {url}")
            return None


class MatchProcessor:
    def __init__(self, api):
        self.api = api
        self.match_list = []
        self.match_data_list = []
        self.joueur_dao = JoueurDao()
        self.equipe_dao = EquipeDao()
        self.match_dao = MatchDao()



    def recup_matches(self, page, page_size):
        """Retrieve all match IDs from the API and store them in a list."""
        endpoint = f"/matches?page={page}&page_size={page_size}"
        data = self.api.recup_page(endpoint)
        if data and 'matches' in data:
            self.match_list = [match['id_match'] for match in data['matches']]
            return self.match_list  # Return the match_list
        else:
            print("Error: Unable to retrieve matches.")
            return None  # Return None in case of an error

    def recup_match_data(self):
        """Retrieve detailed match data for each match in the match_list."""
        for match_id in self.match_list:
            endpoint = f"/match/{match_id}"
            match_data = self.api.recup_page(endpoint)
            if match_data:
                self.match_data_list.append(match_data)
        return self.match_data_list


    def process_matches(self):
        """Process match and player data from match_data_list."""
        for match_data in self.match_data_list:
            if match_data == {'detail': 'Match Unknown'}:
                print("Erreur : Match Unknown. Aucun traitement effectué.")
                continue

            team_data_blue = match_data.get('blue', {})
            equipe_score_blue = team_data_blue.get('score', 0)  # Défaut : 0 si absent
            equipe1_nom = match_data['blue']['team']['team']['name']

            team_data_orange = match_data.get('orange', {})
            equipe_score_orange = team_data_orange.get('score', 0)  # Défaut : 0 si absent
            equipe2_nom = match_data['orange']['team']['team']['name']

            ligue = match_data['event']['name']
            region = match_data['event']['region']
            stage = match_data['stage']['name']
            date = match_data['date']
            perso = False

            match1 = {
                "date": date,
                "stage": stage,
                "ligue": ligue,
                "region": region,
                "score1": equipe_score_blue,
                "score2": equipe_score_orange,
                "equipe1": equipe1_nom,  # Nom de l'équipe
                "equipe2": equipe2_nom,  # Nom de l'équipe
                "perso": perso,
                "match_id": match_data["_id"]
            }

            # Créer l'objet Match et l'enregistrer
            match2 = Match(**match1)

            result_match = self.match_dao.creer(match2)


            # Process teams and players for each match
            for couleur in ['blue', 'orange']:
                self.process_team(match_data, couleur,ligue,region,stage,date)
                self.process_players(match_data, couleur,ligue,region,stage,date)

    def process_team(self,match_data,couleur,ligue,region,stage,date):
        """Process team data for a given match and team color."""
        team_data = match_data.get(couleur, {})

        # Vérification de l'existence du score
        equipe_score = team_data.get('score')
        equipe_nom = match_data[couleur]['team']['team']['name']

        stats_core = match_data[couleur]['team']['stats']['core']


        equipe_stats = {
            "match_id": match_data["_id"],
            "equipe_nom": equipe_nom,
            "equipe_score": equipe_score,
            "shots": stats_core['shots'],
            "goals": stats_core['goals'],
            "saves": stats_core['saves'],
            "assists": stats_core['assists'],
            "score": stats_core['score'],
            "demo_inflige": match_data[couleur]['team']['stats']['demo']['inflicted'],
            "demo_recu": match_data[couleur]['team']['stats']['demo']['taken'],
            "boost_stole":match_data[couleur]['team']['stats']['boost']["countStolenBig"],
            "shooting_percentage": stats_core['shootingPercentage'],
            "time_defensive_third": match_data[couleur]['team']['stats']['positioning']['timeDefensiveThird'],
            "time_neutral_third": match_data[couleur]['team']['stats']['positioning']['timeNeutralThird'],
            "time_offensive_third": match_data[couleur]['team']['stats']['positioning']['timeOffensiveThird'],
            "date": date,
            "region": region,
            "stage": stage,
            "ligue": ligue
        }

        equipe = Equipe(**equipe_stats)
        equipe.indice_performance = round(
            (
                equipe.goals * 1 +
                equipe.assists * 0.75 +
                equipe.saves * 0.6 +
                equipe.shots * 0.4 +
                (equipe.goals / equipe.shots) * 0.5 if equipe.shots > 0 else 0
            )  * regional_indices[equipe.region], 2
        )
        equipe.indice_de_pression = round(
            (   equipe.boost_stole/10 +
                equipe.goals / 1.05 +
                equipe.shots / 3.29 +
                equipe.demo_inflige / 0.56 +
                equipe.time_offensive_third / 201.1
            ) , 2)
        result_equipe = self.equipe_dao.creer(equipe)





    def process_players(self, match_data, couleur,ligue,region,stage,date):
        """Process player data for a given team."""
        equipe_nom = match_data[couleur]['team']['team']['name']

        for j in range(3):  # Assume 3 players per team
            joueur_stats = match_data[couleur]['players'][j]
            joueur_nom = joueur_stats['player']['tag']
            joueur_nationalite = joueur_stats['player']['country']
            joueur_core = joueur_stats['stats']['core']

            joueur_data = {
            "match_id": match_data["_id"],
            "equipe_nom": equipe_nom,
            "nom": joueur_nom,
            "nationalite": joueur_nationalite,
            "shots": joueur_core['shots'],
            "goals": joueur_core['goals'],
            "saves": joueur_core['saves'],
            "assists": joueur_core['assists'],
            "score": joueur_core['score'],
            "shooting_percentage": round(joueur_core['shootingPercentage'],2),
            "demo_inflige": joueur_stats['stats']['demo']['inflicted'],
            "demo_recu": joueur_stats['stats']['demo']['taken'],
            "goal_participation": round(joueur_stats['advanced']['goalParticipation'],2),
            "rating": round(joueur_stats['advanced']['rating'],2),
            "time_defensive_third": joueur_stats['stats']['positioning']['timeDefensiveThird'],
            "time_neutral_third": joueur_stats['stats']['positioning']['timeNeutralThird'],
            "time_offensive_third": joueur_stats['stats']['positioning']['timeOffensiveThird'],
            "date":date,
            "region":region,
            "stage":stage,
            "ligue":ligue
        }


            joueur = Joueur(**joueur_data)
            joueur.indice_offensif = round(
            (
                joueur.goals / 1.05 +
                joueur.assists / 0.5 +
                joueur.shots / 3.29 +
                joueur.demo_inflige / 0.56 +
                joueur.time_offensive_third / 201.1
            ) , 2)
            joueur.indice_performance = round(
            (
                joueur.goals * 1 +
                joueur.assists * 0.75 +
                joueur.saves * 0.6 +
                joueur.shots * 0.4 +
                (joueur.goals / joueur.shots) * 0.5 if joueur.shots > 0 else 0
            )  * regional_indices[joueur.region], 2
        )
            result = self.joueur_dao.creer(joueur)
