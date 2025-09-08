import re
import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from scraper.models import DefenderMatch, MidfielderMatch, ForwardMatch

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "es-ES,es;q=0.9"
}

JORNADAS = [36, 37, 38]

def extract_minutes_played(match_row):
    try:
        data_cell = match_row.find('td', class_='data')
        if data_cell:
            data_text = data_cell.get_text(strip=True).lower()
            if "no convocado" in data_text or "convocado, no jugó" in data_text:
                return 0
        if match_row.find('span', class_='lesionado'):
            return 0
        substitution = match_row.find('span', class_='cambio')
        if not substitution:
            return 90
        minute_text = re.search(r"\d+", substitution.get_text())
        if not minute_text:
            return 90
        minute = int(minute_text.group())
        icons = substitution.find_all('img')
        for icon in icons:
            if 'title' in icon.attrs:
                if 'Entrada' in icon['title']:
                    return max(0, min(90, 90 - minute))
                elif 'Salida' in icon['title']:
                    return max(0, min(90, minute))
        return 90
    except Exception as e:
        print(f"Error processing row: {e}")
        return 90

def extract_match_statistics(soup, position):
    matches = []
    seen_matches = set()
    match_rows = soup.find_all('tr', class_=lambda x: x and 'plegado' in x and 'plegable' in x)
    for row in match_rows:
        details_row = row.find_next_sibling('tr', class_='desglose')
        if not details_row:
            continue
        matchday = row.find('td', class_='bold').get_text(strip=True) if row.find('td', class_='bold') else 'Desconocida'
        if not re.match(r'^\d+$', matchday):
            continue
        matchday = int(matchday)
        if matchday not in JORNADAS:
            continue
        teams = row.find('div', class_='link').get_text(" ", strip=True) if row.find('div', class_='link') else 'Desconocido'
        result = row.find('strong', class_=lambda x: x and ('score' in x)).get_text(strip=True) if row.find('strong', class_=lambda x: x and ('score' in x)) else 'Desconocido'
        match_id = f"{matchday}-{teams}-{result}"
        if match_id in seen_matches:
            continue
        seen_matches.add(match_id)
        match_info = {
            'matchday': matchday,
            'teams': teams,
            'result': result,
            'minutes': extract_minutes_played(row),
        }
        stats = details_row.find_all('div', class_='estadistica')
        # Default values
        if position == "defender":
            match_info.update({'goals': 0, 'assists': 0, 'goals_conceded': 0, 'recoveries': 0})
        elif position == "midfielder":
            match_info.update({'goals': 0, 'assists': 0, 'key_passes': 0, 'recoveries': 0})
        elif position == "forward":
            match_info.update({'goals': 0, 'assists': 0, 'shots_on_goal': 0, 'dribbles': 0})
        for stat in stats:
            text = stat.get_text(strip=True).lower()
            if position == "defender":
                if "goles" in text and "encajados" not in text:
                    match_info['goals'] = int(re.search(r"\d+", text).group())
                elif "asistencias" in text:
                    match_info['assists'] = int(re.search(r"\d+", text).group())
                elif "goles encajados" in text:
                    match_info['goals_conceded'] = int(re.search(r"\d+", text).group())
                elif "pases interceptados" in text or "balones robados" in text:
                    match_info['recoveries'] += int(re.search(r"\d+", text).group())
            elif position == "midfielder":
                if "goles" in text and "encajados" not in text:
                    match_info['goals'] = int(re.search(r"\d+", text).group())
                elif "asistencias" in text:
                    match_info['assists'] = int(re.search(r"\d+", text).group())
                elif "pases clave" in text:
                    match_info['key_passes'] = int(re.search(r"\d+", text).group())
                elif "pases interceptados" in text or "balones robados" in text:
                    match_info['recoveries'] += int(re.search(r"\d+", text).group())
            elif position == "forward":
                if "goles" in text and "encajados" not in text:
                    match_info['goals'] = int(re.search(r"\d+", text).group())
                elif "asistencias" in text:
                    match_info['assists'] = int(re.search(r"\d+", text).group())
                elif "tiros a puerta" in text:
                    match_info['shots_on_goal'] = int(re.search(r"\d+", text).group())
                elif "regates" in text:
                    match_info['dribbles'] = int(re.search(r"\d+", text).group())
        matches.append(match_info)
    return matches

def update_position_jornadas(slugs, model, position, season_slug='laliga-24-25'):
    for slug in slugs:
        url = f"https://www.futbolfantasy.com/jugadores/{slug}/{season_slug}"
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.text, 'html.parser')
        matches = extract_match_statistics(soup, position)
        for match in matches:
            if model.objects.filter(player=slug, season=season_slug, matchday=match['matchday']).exists():
                continue
            if position == "defender":
                model.objects.create(
                    player=slug,
                    season=season_slug,
                    matchday=match['matchday'],
                    teams=match['teams'],
                    result=match['result'],
                    minutes=match['minutes'],
                    goals=match['goals'],
                    assists=match['assists'],
                    goals_conceded=match['goals_conceded'],
                    recoveries=match['recoveries']
                )
            elif position == "midfielder":
                model.objects.create(
                    player=slug,
                    season=season_slug,
                    matchday=match['matchday'],
                    teams=match['teams'],
                    result=match['result'],
                    minutes=match['minutes'],
                    goals=match['goals'],
                    assists=match['assists'],
                    key_passes=match['key_passes'],
                    recoveries=match['recoveries']
                )
            elif position == "forward":
                model.objects.create(
                    player=slug,
                    season=season_slug,
                    matchday=match['matchday'],
                    teams=match['teams'],
                    result=match['result'],
                    minutes=match['minutes'],
                    goals=match['goals'],
                    assists=match['assists'],
                    shots_on_goal=match['shots_on_goal'],
                    dribbles=match['dribbles']
                )
            print(f"Added matchday {match['matchday']} for {slug} ({position})")

class Command(BaseCommand):
    help = "Updating players..."

    def handle(self, *args, **kwargs):
        season_slug = 'laliga-24-25'
        defender_slugs = DefenderMatch.objects.values_list('player', flat=True).distinct()
        midfielder_slugs = MidfielderMatch.objects.values_list('player', flat=True).distinct()
        forward_slugs = ForwardMatch.objects.values_list('player', flat=True).distinct()

        update_position_jornadas(defender_slugs, DefenderMatch, "defender", season_slug)
        update_position_jornadas(midfielder_slugs, MidfielderMatch, "midfielder", season_slug)
        update_position_jornadas(forward_slugs, ForwardMatch, "forward", season_slug)

        self.stdout.write(self.style.SUCCESS("Update finished"))