from django.core.management.base import BaseCommand
import time
import pandas as pd
from core.utils import scraper

class Command(BaseCommand):
    help = "Scrape goalkeeper data from futbolfantasy.com and save results."

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting goalkeeper scraping...")

        players_file = "ruta/absoluta/o/relativa/a/goalkeepers_la_liga.csv"
        player_list = pd.read_csv(players_file)['nombre_jugador'].tolist()

        df_matches = scraper.process_goalkeeper_list(player_list)

        if not df_matches.empty:
            output_file = "ruta/absoluta/o/relativa/a/goalkeepers_matches_all_seasons.csv"
            df_matches.to_csv(output_file, index=False, encoding='utf-8')
            self.stdout.write(self.style.SUCCESS(f"Data saved to {output_file}"))
        else:
            self.stdout.write("No goalkeeper data found.")
