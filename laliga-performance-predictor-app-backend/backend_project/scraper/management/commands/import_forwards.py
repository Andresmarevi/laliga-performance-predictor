from django.core.management.base import BaseCommand
from scraper.models import ForwardMatch
import csv
import os

class Command(BaseCommand):
    help = 'Import forward matches from CSV'

    def handle(self, *args, **kwargs):
        csv_path = os.path.join(
            'scraper', 'data', 'forwards_matches_all_seasons.csv'
        )
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0
            for row in reader:
                ForwardMatch.objects.create(
                    player=row['player'],
                    season=row['season'],
                    matchday=int(row['matchday']),
                    teams=row['teams'],
                    result=row['result'],
                    minutes=int(row['minutes']),
                    goals=int(row['goals']),
                    assists=int(row['assists']),
                    shots_on_goal=int(row['shots_on_target']),
                    dribbles=int(row['dribbles']),
                )
                count += 1
            self.stdout.write(self.style.SUCCESS(f'Imported {count} forward matches'))