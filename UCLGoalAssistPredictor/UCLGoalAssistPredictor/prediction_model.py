from django.conf import settings
import pandas as pd
import joblib
import os


class PredictionModel:
    _instance = None

    GOAL_PREDICTOR_PIPELINE = joblib.load(os.path.join(settings.BASE_DIR, 'UCLGoalAssistPredictor', 'static', 'models', 'xgboost_goal_model.pkl'))
    GOAL_PREDICTOR_WITH_ASSISTING_PLAYER_PIPELINE = joblib.load(os.path.join(settings.BASE_DIR, 'UCLGoalAssistPredictor', 'static', 'models', 'xgboost_goal_with_assisting_player_model.pkl'))
    ASSIST_PREDICTOR_PIPELINE = joblib.load(os.path.join(settings.BASE_DIR, 'UCLGoalAssistPredictor', 'static', 'models', 'xgboost_assists_model.pkl'))
    ASSIST_PREDICTOR_WITH_GOAL_SCORER_PIPELINE = joblib.load(os.path.join(settings.BASE_DIR, 'UCLGoalAssistPredictor', 'static', 'models', 'xgboost_assists_with_goal_scorer_model.pkl'))

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PredictionModel, cls).__new__(cls)
            cls._instance.pipeline = None
            cls._instance.input_data = None
        return cls._instance

    def set_pipeline(self, trained_pipeline):
        self.pipeline = trained_pipeline

    def set_input_data(self, data):
        self.input_data = data

    def predict(self):
        if self.pipeline is None or self.input_data is None:
            raise ValueError("Pipeline or input data is not set.")

        input_df = pd.DataFrame([self.input_data])
        predictions = self.pipeline.predict(input_df)
        rounded_prediction = round(predictions[0], 2)
        return round(rounded_prediction)