from django.shortcuts import render, redirect
from django.contrib import messages


def home(request):
    return render(request, 'home.html')


def make_prediction(request):
    if request.method == 'POST':
        home_team = request.POST.get('home_team')
        away_team = request.POST.get('away_team')
        stadium = request.POST.get('stadium')
        player_name = request.POST.get('player_name')
        player_team = request.POST.get('player_team')


        input_data = {
            'HOME_TEAM': home_team,
            'AWAY_TEAM': away_team,
            'STADIUM': stadium,
            'GOAL_SCORER': player_name,
            'GOAL_SCORER_TEAM_NAME': player_team
        }
    return render(request, 'make_prediction.html')


def show_prediction(request):
    return render(request, 'show_prediction.html')