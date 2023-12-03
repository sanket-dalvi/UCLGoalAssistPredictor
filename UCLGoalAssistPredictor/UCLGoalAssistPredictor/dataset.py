import pandas as pd
from django.conf import settings
import os

class Dataset:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Dataset, cls).__new__(cls)
            csv_file_path = os.path.join(settings.BASE_DIR, 'UCLGoalAssistPredictor', 'static', 'dataset', '501_PROJECT_DATASET.csv')
            df_raw = pd.read_csv(csv_file_path)
            # Remove rows where 'GOAL_SCORER' or 'GOAL_SCORER_TEAM_NAME' is null
            cls._instance.data = df_raw.dropna(subset=['GOAL_SCORER', 'GOAL_SCORER_TEAM_NAME'])
            cls._instance.home_teams = cls._instance.data['HOME_TEAM'].unique()
            cls._instance.away_teams = cls._instance.data['AWAY_TEAM'].unique()
            cls._instance.goal_scorers = cls._instance.data['GOAL_SCORER'].unique()
            cls._instance.assist_players = cls._instance.data['ASSIST_PLAYER'].unique()
            cls._instance.stadiums = cls._instance.data['STADIUM'].unique()
            cls._instance.goal_scorer_teams = cls._instance.data['GOAL_SCORER_TEAM_NAME'].unique()
        return cls._instance

    def get_home_teams(self):
        return self.home_teams

    def get_away_teams(self):
        return self.away_teams

    def get_goal_scorers(self):
        return self.goal_scorers

    def get_assist_players(self):
        return self.assist_players

    def get_stadiums(self):
        return self.stadiums

    def get_goal_scorer_teams(self):
        return self.goal_scorer_teams

    def get_data(self):
        return self.data
