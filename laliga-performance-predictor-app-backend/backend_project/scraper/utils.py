import requests
from bs4 import BeautifulSoup
from scraper.models import GoalkeeperMatch, DefenderMatch, MidfielderMatch, ForwardMatch
from scraper.ratings.gk_rating import compute_gk_rating
from scraper.ratings.df_rating import compute_df_rating
from scraper.ratings.mf_rating import compute_mf_rating
from scraper.ratings.fw_rating import compute_fw_rating

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "es-ES,es;q=0.9"
}

def get_player_basic_info(player_name):
    url = f"https://www.futbolfantasy.com/jugadores/{player_name}"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        name_tag = soup.find('div', class_='info-right')
        name = None
        if name_tag:
            name = name_tag.get_text(strip=True)

        position_span = soup.find("span", class_="position-box")
        position = position_span.get_text(strip=True) if position_span else "Desconocida"

        img_tag = soup.find("img", class_="img w-100 mb-1")
        photo_url = img_tag["src"] if img_tag else ""

        team_name = None
        team_logo = None
        team_div = soup.find("div", class_="img-underphoto text-center col-12 info border-0 font-weight-bold txtc")
        if team_div:
            team_img = team_div.find("img")
            if team_img:
                team_name = team_img.get("alt")
                team_logo = team_img.get("src")
                if team_logo and team_logo.startswith("//"):
                    team_logo = "https:" + team_logo

        return {
            "slug": player_name,
            "name": name,
            "position": position,
            "photo_url": photo_url,
            "team": team_name,
            "team_logo": team_logo
        }
    except Exception as e:
        return {"error": str(e)}

def get_player_season_stats(slug, season_slug='laliga-24-25'):
    for model, pos in [
        (GoalkeeperMatch, 'goalkeeper'),
        (DefenderMatch, 'defender'),
        (MidfielderMatch, 'midfielder'),
        (ForwardMatch, 'forward'),
    ]:
        if model.objects.filter(player=slug, season=season_slug).exists():
            matches = model.objects.filter(player=slug, season=season_slug)
            break
    else:
        return {}

    stats = {}

    if isinstance(matches.first(), GoalkeeperMatch):
        stats['matches_played'] = matches.count()
        stats['starter'] = matches.filter(minutes__gte=1).count()
        stats['sub'] = matches.filter(minutes=0).count()
        stats['goals'] = 0
        stats['assists'] = 0
        stats['shots_on_goal'] = 0
        stats['dribbles'] = 0
        stats['key_passes'] = 0
        stats['recoveries'] = 0
        stats['penalties_committed'] = 0
        stats['saves'] = sum(m.saves for m in matches)
        stats['goal_errors'] = sum(m.errors_leading_to_goal for m in matches)
        stats['penalties_saved'] = sum(m.penalties_saved for m in matches)
        stats['goals_conceded'] = sum(m.goals_conceded for m in matches)
        stats['minutes'] = sum(m.minutes for m in matches)
    elif isinstance(matches.first(), DefenderMatch):
        stats['matches_played'] = matches.count()
        stats['starter'] = matches.filter(minutes__gte=1).count()
        stats['sub'] = matches.filter(minutes=0).count()
        stats['goals'] = sum(m.goals for m in matches)
        stats['assists'] = sum(m.assists for m in matches)
        stats['shots_on_goal'] = 0
        stats['dribbles'] = 0
        stats['key_passes'] = 0
        stats['recoveries'] = sum(m.recoveries for m in matches)
        stats['penalties_committed'] = 0
        stats['saves'] = 0
        stats['goal_errors'] = 0
        stats['penalties_saved'] = 0
        stats['goals_conceded'] = sum(m.goals_conceded for m in matches)
        stats['minutes'] = sum(m.minutes for m in matches)
    elif isinstance(matches.first(), MidfielderMatch):
        stats['matches_played'] = matches.count()
        stats['starter'] = matches.filter(minutes__gte=1).count()
        stats['sub'] = matches.filter(minutes=0).count()
        stats['goals'] = sum(m.goals for m in matches)
        stats['assists'] = sum(m.assists for m in matches)
        stats['shots_on_goal'] = 0
        stats['dribbles'] = 0
        stats['key_passes'] = sum(m.key_passes for m in matches)
        stats['recoveries'] = sum(m.recoveries for m in matches)
        stats['penalties_committed'] = 0
        stats['saves'] = 0
        stats['goal_errors'] = 0
        stats['penalties_saved'] = 0
        stats['goals_conceded'] = 0
        stats['minutes'] = sum(m.minutes for m in matches)
    elif isinstance(matches.first(), ForwardMatch):
        stats['matches_played'] = matches.count()
        stats['starter'] = matches.filter(minutes__gte=1).count()
        stats['sub'] = matches.filter(minutes=0).count()
        stats['goals'] = sum(m.goals for m in matches)
        stats['assists'] = sum(m.assists for m in matches)
        stats['shots_on_goal'] = sum(m.shots_on_goal for m in matches)
        stats['dribbles'] = sum(m.dribbles for m in matches)
        stats['key_passes'] = 0
        stats['recoveries'] = 0
        stats['penalties_committed'] = 0
        stats['saves'] = 0
        stats['goal_errors'] = 0
        stats['penalties_saved'] = 0
        stats['goals_conceded'] = 0
        stats['minutes'] = sum(m.minutes for m in matches)

    stats['matches_played_display'] = f"{stats['starter']} ({stats['minutes']})"

    return stats

def get_last_match_data(matches):
    last = matches.filter(matchday=38).first()
    if not last:
        return None 

    prev_matches = matches.filter(matchday__lte=38).order_by('-matchday')
    u3 = prev_matches[:3]
    u5 = prev_matches[:5]

    def avg(queryset, attr):
        vals = [getattr(m, attr, 0) for m in queryset]
        return round(sum(vals) / len(vals), 2) if vals else 0

    if isinstance(last, GoalkeeperMatch):
        data = {
            'Sav-U5': avg(u5, 'saves'),
            'Sav-U3': avg(u3, 'saves'),
            'Sav-match': last.saves,
            'GoalsConced-U5': avg(u5, 'goals_conceded'),
            'GoalsConced-U3': avg(u3, 'goals_conceded'),
            'GoalsConced-match': last.goals_conceded,
            'Minutes-U5': avg(u5, 'minutes'),
            'Minutes-U3': avg(u3, 'minutes'),
            'Minutes-match': last.minutes,
            'ErrorGoal-U5': avg(u5, 'errors_leading_to_goal'),
            'ErrorGoal-U3': avg(u3, 'errors_leading_to_goal'),
            'ErrorGoal-match': last.errors_leading_to_goal,
            'PenSav-U5': avg(u5, 'penalties_saved'),
            'PenSav-U3': avg(u3, 'penalties_saved'),
            'PenSav-match': last.penalties_saved,
        }
        data['performance_rating'] = round(compute_gk_rating(data), 3)
        return data
    elif isinstance(last, DefenderMatch):
        data = {
            'Recoveries-U5': avg(u5, 'recoveries'),
            'Recoveries-U3': avg(u3, 'recoveries'),
            'Recoveries-match': last.recoveries,
            'GoalsConceded-U5': avg(u5, 'goals_conceded'),
            'GoalsConceded-U3': avg(u3, 'goals_conceded'),
            'GoalsConceded-match': last.goals_conceded,
            'Minutes-U5': avg(u5, 'minutes'),
            'Minutes-U3': avg(u3, 'minutes'),
            'Minutes-match': last.minutes,
            'Goals-U5': avg(u5, 'goals'),
            'Goals-U3': avg(u3, 'goals'),
            'Goals-match': last.goals,
            'Assists-U5': avg(u5, 'assists'),
            'Assists-U3': avg(u3, 'assists'),
            'Assists-match': last.assists,
        }
        data['performance_rating'] = round(compute_df_rating(data), 3)
        return data
    elif isinstance(last, MidfielderMatch):
        data = {
            'Recoveries-U5': avg(u5, 'recoveries'),
            'Recoveries-U3': avg(u3, 'recoveries'),
            'Recoveries-match': last.recoveries,
            'Goals-U5': avg(u5, 'goals'),
            'Goals-U3': avg(u3, 'goals'),
            'Goals-match': last.goals,
            'Assists-U5': avg(u5, 'assists'),
            'Assists-U3': avg(u3, 'assists'),
            'Assists-match': last.assists,
            'Minutes-U5': avg(u5, 'minutes'),
            'Minutes-U3': avg(u3, 'minutes'),
            'Minutes-match': last.minutes,
            'KeyPasses-U5': avg(u5, 'key_passes'),
            'KeyPasses-U3': avg(u3, 'key_passes'),
            'KeyPasses-match': last.key_passes,
        }
        data['performance_rating'] = round(compute_mf_rating(data), 3)
        return data
    elif isinstance(last, ForwardMatch):
        data = {
            'Goals-U5': avg(u5, 'goals'),
            'Goals-U3': avg(u3, 'goals'),
            'Goals-match': last.goals,
            'Assists-U5': avg(u5, 'assists'),
            'Assists-U3': avg(u3, 'assists'),
            'Assists-match': last.assists,
            'Minutes-U5': avg(u5, 'minutes'),
            'Minutes-U3': avg(u3, 'minutes'),
            'Minutes-match': last.minutes,
            'ShotsOnGoal-U5': avg(u5, 'shots_on_goal'),
            'ShotsOnGoal-U3': avg(u3, 'shots_on_goal'),
            'ShotsOnGoal-match': last.shots_on_goal,
            'Dribbles-U5': avg(u5, 'dribbles'),
            'Dribbles-U3': avg(u3, 'dribbles'),
            'Dribbles-match': last.dribbles,
        }
        data['performance_rating'] = round(compute_fw_rating(data), 3)
        return data
    return None