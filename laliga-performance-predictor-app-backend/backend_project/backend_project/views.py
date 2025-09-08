import csv
import os
from django.http import JsonResponse
from django.conf import settings
from .players_data import PLAYERS

def search_players(request):
    query = request.GET.get('q', '').strip().lower()
    if not query or len(query) < 2:
        return JsonResponse({'results': []})

    results = []
    for player in PLAYERS:
        if query in player['name'].lower():
            results.append(player)
        if len(results) >= 20:
            break

    return JsonResponse({'results': results})
