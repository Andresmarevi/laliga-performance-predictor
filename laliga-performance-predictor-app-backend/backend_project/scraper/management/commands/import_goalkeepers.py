from django.core.management.base import BaseCommand
from scraper.models import GoalkeeperMatch
import csv
import os


class Command(BaseCommand):
    help = 'Import goalkeeper matches from CSV'

    def handle(self, *args, **kwargs):
        csv_path = os.path.join(
            'scraper', 'data', 'goalkeepers_matches_all_seasons.csv'
        )
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0
            for row in reader:
                GoalkeeperMatch.objects.create(
                    player=row['player'],
                    season=row['season'],
                    matchday=int(row['matchday']),
                    teams=row['teams'],
                    result=row['result'],
                    minutes=int(row['minutes']),
                    saves=int(row['saves']),
                    goals_conceded=int(row['goals_conceded']),
                    errors_leading_to_goal=int(row['errors_leading_to_goal']),
                    penalties_saved=int(row['penalties_saved']),
                )
                count += 1
            self.stdout.write(self.style.SUCCESS(f'Imported {count} goalkeeper matches'))