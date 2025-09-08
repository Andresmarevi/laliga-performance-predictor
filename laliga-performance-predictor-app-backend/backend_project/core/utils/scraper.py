import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "es-ES,es;q=0.9"
}


def scrape_player_basic_info(player_slug):
    url = f"https://www.futbolfantasy.com/jugadores/{player_slug}"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        name_tag = soup.find('div', class_='info-right')
        name = None
        if name_tag:
            name = name_tag.get_text(strip=True)

        position_tag = soup.find('span', class_='position-box')
        position = position_tag.get_text(strip=True) if position_tag else None

        img_tag = soup.find('img', class_='img w-100 mb-1')
        photo_url = img_tag['src'] if img_tag and 'src' in img_tag.attrs else None

        return {
            "name": name,
            "position": position,
            "photo_url": photo_url
        }
    except Exception as e:
        print(f"Error scraping player {player_slug}: {e}")
        return None


if __name__ == "__main__":
    player_slug = "pedri-gonzalez"
    data = scrape_player_basic_info(player_slug)
    print(data)