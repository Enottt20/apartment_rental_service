import requests


# Функция для геокодирования города через Nominatim
def geocode_city(city_name):
    base_url = "https://nominatim.openstreetmap.org/search"

    params = {
        "q": city_name,
        "format": "json",
    }

    response = requests.get(base_url, params=params, timeout=10)
    data = response.json()

    if data and len(data) > 0:
        city_coords = {
            "lat": float(data[0]["lat"]),
            "lng": float(data[0]["lon"])
        }
        return city_coords
    else:
        return None