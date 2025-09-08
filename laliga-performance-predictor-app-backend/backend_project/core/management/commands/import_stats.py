import csv
from django.core.management.base import BaseCommand
from scraper.models import PlayerMatchStat

class Command(BaseCommand):
    help = 'Import player match stats from CSV'

    def add_arguments(self, parser):
        parser.add_argument('csv_path', type=str)

    def handle(self, *args, **options):
        with open(options['csv_path'], newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                PlayerMatchStat.objects.update_or_create(
                    player_slug=row['player_slug'],
                    season=row['season'],
                    matchday=row['matchday'],
                    defaults={
                        'opponent': row['opponent'],
                        'is_home': row['is_home'] == 'True',
                        'starter': row['starter'] == 'True',
                        'minutes': int(row['minutes']),
                        'goals': int(row['goals']),
                        'assists': int(row['assists']),
                        'shots_on_goal': int(row.get('shots_on_goal', 0) or 0),
                        'dribbles': int(row.get('dribbles', 0) or 0),
                        'key_passes': int(row.get('key_passes', 0) or 0),
                        'recoveries': int(row.get('recoveries', 0) or 0),
                        'penalties_committed': int(row.get('penalties_committed', 0) or 0),
                        'saves': int(row.get('saves', 0) or 0),
                        'goal_errors': int(row.get('goal_errors', 0) or 0),
                        'penalties_saved': int(row.get('penalties_saved', 0) or 0),
                    }
                )
        self.stdout.write(self.style.SUCCESS('Import completed!'))