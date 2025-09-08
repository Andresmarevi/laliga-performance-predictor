import pandas as pd

df = pd.read_csv("players_la_liga.csv")

def slug_to_name(slug: str) -> str:
    parts = slug.split("-")
    parts = [p.capitalize() for p in parts]
    return " ".join(parts)

df["display_name"] = df["name_player"].apply(slug_to_name)
df.to_csv("players_slugs_display.csv", index=False, encoding="utf-8")

print("File 'players_slugs_display.csv' created")
