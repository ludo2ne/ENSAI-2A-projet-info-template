
import requests,json # truc à importer
import pandas as pd
import os
import dotenv
from dao.joueur_dao import JoueurDao





# Charger les variables d'environnement
dotenv.load_dotenv()
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
        self.filtered_matches = []
        self.filtered_players = []
        self.joueur_dao = JoueurDao()
        #self.matchdao = JoueurDao()
        #self.joueur_dao = JoueurDao()



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


            # Process teams and players for each match
            for couleur in ['blue', 'orange']:
                self.process_team(match_data, couleur)
                self.process_players(match_data, couleur)

    def process_team(self, match_data,couleur):
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
            "shooting_percentage": stats_core['shootingPercentage'],
            "time_defensive_third": match_data[couleur]['team']['stats']['positioning']['timeDefensiveThird'],
            "time_neutral_third": match_data[couleur]['team']['stats']['positioning']['timeNeutralThird'],
            "time_offensive_third": match_data[couleur]['team']['stats']['positioning']['timeOffensiveThird']
        }
        self.filtered_matches.append(equipe_stats)


        ligue = match_data['event']['name']
        region = match_data['event']['region']
        stage = match_data['stage']['name']
        date = match_data['date']


    def process_players(self, match_data, couleur):
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
                "joueur_nom": joueur_nom,
                "nationalite": joueur_nationalite,
                "shots": joueur_core['shots'],
                "goals": joueur_core['goals'],
                "saves": joueur_core['saves'],
                "assists": joueur_core['assists'],
                "score": joueur_core['score'],
                "shooting_percentage": joueur_core['shootingPercentage'],
                "demo_infligées": joueur_stats['stats']['demo']['inflicted'],
                "demo_reçues": joueur_stats['stats']['demo']['taken'],
                "goal_participation": joueur_stats['advanced']['goalParticipation'],
                "rating": joueur_stats['advanced']['rating'],
                "time_defensive_third": joueur_stats['stats']['positioning']['timeDefensiveThird'],
                "time_neutral_third": joueur_stats['stats']['positioning']['timeNeutralThird'],
                "time_offensive_third": joueur_stats['stats']['positioning']['timeOffensiveThird']
            }
            self.filtered_players.append(joueur_data)
            result = self.joueur_dao.creer(joueur_data)



    def create_dataframes(self):
        """Create Pandas DataFrames from the filtered match and player data."""
        df_filtered_matches = pd.DataFrame(self.filtered_matches)
        df_filtered_players = pd.DataFrame(self.filtered_players)
        return df_filtered_matches, df_filtered_players







# Example usage
api = API(base_url="https://api.rlcstatistics.net")
match_processor = MatchProcessor(api)

# Step 1: Get the matches
t= match_processor.recup_matches(page=226, page_size=2)
print(t)
u=match_processor.recup_match_data()
print(u)
# Step 3: Process the match and player data
match_processor.process_matches()

# Step 4: Create DataFrames
df_matches, df_players = match_processor.create_dataframes()

print(df_matches,df_players)

