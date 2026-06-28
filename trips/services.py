import requests

ARTIC_BASE_URL = "https://api.artic.edu/api/v1"


def get_artwork(external_id):
    try:
        response = requests.get(f"{ARTIC_BASE_URL}/artworks/{external_id}")
        if response.status_code == 200:
            data = response.json()
            return data.get("data")
        return None
    except requests.RequestException:
        return None


def validate_artwork_exists(external_id):
    artwork = get_artwork(external_id)
    return artwork is not None


def search_artworks(query, limit=10):
    try:
        response = requests.get(
            f"{ARTIC_BASE_URL}/artworks/search",
            params={"q": query, "limit": limit}
        )
        if response.status_code == 200:
            return response.json()
        return None
    except requests.RequestException:
        return None