from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from scraper.models import GoalkeeperMatch, DefenderMatch, MidfielderMatch, ForwardMatch
from django.http import JsonResponse
from .utils import get_player_basic_info, get_player_season_stats, get_last_match_data
from .predict_utils import predict_performance_for_player
from .performance_utils import get_player_performance_evolution

def player_info(request):
    player_name = request.GET.get("player")
    if not player_name:
        return JsonResponse({"error": "Missing player parameter"}, status=400)

    data = get_player_basic_info(player_name)
    return JsonResponse(data)

def player_season_stats(request):
    slug = request.GET.get('player')
    if not slug:
        return JsonResponse({'error': 'No player slug provided'}, status=400)
    stats = get_player_season_stats(slug)
    return JsonResponse(stats)

def player_last_match_stats(request):
    slug = request.GET.get("player")
    season_slug = request.GET.get("season", "laliga-24-25")

    for model in [GoalkeeperMatch, DefenderMatch, MidfielderMatch, ForwardMatch]:
        if model.objects.filter(player=slug, season=season_slug).exists():
            matches = model.objects.filter(player=slug, season=season_slug)
            break
    else:
        return JsonResponse({"error": "No matches found"}, status=404)

    stats = get_last_match_data(matches)
    return JsonResponse(stats)

def predict_performance(request):
    slug = request.GET.get('player')
    season = request.GET.get('season', 'laliga-24-25')

    for model, pos in [
        (GoalkeeperMatch, 'goalkeeper'),
        (DefenderMatch, 'defender'),
        (MidfielderMatch, 'midfielder'),
        (ForwardMatch, 'forward'),
    ]:
        if model.objects.filter(player=slug, season=season).exists():
            matches = model.objects.filter(player=slug, season=season)
            break
    else:
        return JsonResponse({'error': 'Player not found'}, status=404)

    result = predict_performance_for_player(matches, pos)
    return JsonResponse(result)


@require_GET
def player_performance_evolution(request):
    slug = request.GET.get('player')
    season = request.GET.get('season', 'laliga-24-25')
    if not slug:
        return JsonResponse({'error': 'No player slug provided'}, status=400)
    data = get_player_performance_evolution(slug, season)
    return JsonResponse(data, safe=False)