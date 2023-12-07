from django.shortcuts import render, redirect
from django.contrib import messages
from .prediction_model import PredictionModel
from .dataset import Dataset



def home(request):
    return render(request, 'home.html')  


def make_prediction(request):
    # Create an instance of Dataset
    ds = Dataset()
    # Create an instance of PredictionModel
    prediction_model = PredictionModel()
    prediction_pipeline = None
    input_data = {}


    home_teams = ds.get_home_teams()
    away_teams = ds.get_away_teams()
    goal_scorers = ds.get_goal_scorers()
    assist_players = ds.get_assist_players()
    goal_scorer_teams = ds.get_goal_scorer_teams()
    stadiums = ds.get_stadiums()

    context = {
        'home_teams' : home_teams,
        'away_teams' : away_teams,
        'goal_scorers' : goal_scorers,
        'assist_players' : assist_players,
        'goal_scorer_teams' : goal_scorer_teams,
        'stadiums' : stadiums
    }


    if request.method == 'POST':

        # collect data from form
        home_team = request.POST.get('home_team')
        away_team = request.POST.get('away_team')
        stadium = request.POST.get('stadium')
        goal_scorer_name = request.POST.get('goal_scorer')
        player_team = request.POST.get('player_team')
        assist_player = request.POST.get('assist_player')

        input_data = {
                'HOME_TEAM': home_team,
                'AWAY_TEAM': away_team,
                'STADIUM': stadium,
                'GOAL_SCORER_TEAM_NAME': player_team
            }

        if assist_player and goal_scorer_name:
            input_data['GOAL_SCORER'] = goal_scorer_name
            input_data['ASSIST_PLAYER'] = assist_player
            prediction_pipeline = prediction_model.GOAL_PREDICTOR_WITH_ASSISTING_PLAYER_PIPELINE

            prediction_model.set_pipeline(prediction_pipeline)
            prediction_model.set_input_data(input_data)
            predicted_goals = prediction_model.predict()
            result = f"Goals : {goal_scorer_name} - {predicted_goals}\n"

            prediction_pipeline = prediction_model.ASSIST_PREDICTOR_WITH_GOAL_SCORER_PIPELINE
            prediction_model.set_pipeline(prediction_pipeline)
            predicted_assists = prediction_model.predict()
            result += f"Assists : {assist_player} - {predicted_assists}"
            return render(request, 'show_prediction.html', {'predicted_score' : result})


        elif goal_scorer_name:

            input_data['GOAL_SCORER'] = goal_scorer_name
            prediction_pipeline = prediction_model.GOAL_PREDICTOR_PIPELINE
            prediction_model.set_pipeline(prediction_pipeline)
            prediction_model.set_input_data(input_data)
            predicted_goals = prediction_model.predict()
            result = f"Goals : {goal_scorer_name} - {predicted_goals}\n"

            return render(request, 'show_prediction.html', {'predicted_score' : result})

        elif assist_player:
        
            input_data['ASSIST_PLAYER'] = assist_player
            prediction_pipeline = prediction_model.ASSIST_PREDICTOR_PIPELINE
            prediction_model.set_pipeline(prediction_pipeline)
            prediction_model.set_input_data(input_data)
            predicted_assists = prediction_model.predict()
            result = f"Assists : {goal_scorer_name} - {predicted_goals}\n"
            return render(request, 'show_prediction.html', {'predicted_score' : result})

        else:
            messages.error(request, "Received Invalid Goal Scorer and Assist Player Name")
         
        return render(request, 'show_prediction.html', {'predicted_goals' : predicted_goals})
        
    return render(request, 'make_prediction.html', context)


def show_prediction(request):
    return render(request, 'show_prediction.html')