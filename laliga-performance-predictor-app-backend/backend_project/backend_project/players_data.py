import csv
import os
from django.conf import settings

PLAYERS = []

def load_players():
    global PLAYERS
    csv_path = os.path.join(settings.BASE_DIR, 'core/utils/players_slugs_display.csv')
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        PLAYERS = []
        for row in reader:
            slug = row.get('name_player')
            name = row.get('display_name')
            if slug and name:
                PLAYERS.append({'slug': slug, 'name': name})


load_players()


