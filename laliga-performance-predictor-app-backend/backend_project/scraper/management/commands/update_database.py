import re
import requests
from bs4 import BeautifulSoup
from scraper.models import GoalkeeperMatch

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "es-ES,es;q=0.9"
}

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

def extract_match_statistics(soup):
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
        teams = row.find('div', class_='link').get_text(" ", strip=True) if row.find('div', class_='link') else 'Desconocido'
        result = row.find('strong', class_=lambda x: x and ('score' in x)).get_text(strip=True) if row.find('strong', class_=lambda x: x and ('score' in x)) else 'Desconocido'
        match_id = f"{matchday}-{teams}-{result}"
        if match_id in seen_matches:
            continue
        seen_matches.add(match_id)
        match_info = {
            'matchday': int(matchday),
            'teams': teams,
            'result': result,
            'minutes': extract_minutes_played(row),
            'saves': 0,
            'goals_conceded': 0,
            'errors_leading_to_goal': 0,
            'penalties_saved': 0
        }
        stats = details_row.find_all('div', class_='estadistica')
        for stat in stats:
            text = stat.get_text(strip=True).lower()
            if "paradas" in text:
                match_info['saves'] = int(re.search(r"\d+", text).group())
            elif "goles encajados" in text:
                match_info['goals_conceded'] = int(re.search(r"\d+", text).group())
            elif "errores en gol en contra" in text:
                match_info['errors_leading_to_goal'] = int(re.search(r"\d+", text).group())
            elif "penaltis parados" in text:
                match_info['penalties_saved'] = int(re.search(r"\d+", text).group())
        matches.append(match_info)
    return matches

def update_goalkeeper_jornadas(slug, season_slug='laliga-24-25'):
    url = f"https://www.futbolfantasy.com/jugadores/{slug}/{season_slug}"
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    matches = extract_match_statistics(soup)
    for match in matches:
        if match['matchday'] not in [36, 37, 38]:
            continue
        if GoalkeeperMatch.objects.filter(player=slug, season=season_slug, matchday=match['matchday']).exists():
            continue
        GoalkeeperMatch.objects.create(
            player=slug,
            season=season_slug,
            matchday=match['matchday'],
            teams=match['teams'],
            result=match['result'],
            minutes=match['minutes'],
            saves=match['saves'],
            goals_conceded=match['goals_conceded'],
            errors_leading_to_goal=match['errors_leading_to_goal'],
            penalties_saved=match['penalties_saved']
        )
        print(f"Added matchday {match['matchday']} for {slug}")

from scraper.models import GoalkeeperMatch

def update_all_goalkeepers(season_slug='laliga-24-25'):
    slugs = GoalkeeperMatch.objects.values_list('player', flat=True).distinct()
    for slug in slugs:
        update_goalkeeper_jornadas(slug, season_slug)

update_all_goalkeepers('laliga-24-25')