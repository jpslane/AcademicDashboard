import requests
from bs4 import BeautifulSoup
from googlesearch import search
import pickle


def load_data_from_cache():
    try:
        with open('cache.pickle', 'rb') as f:
            data = pickle.load(f)
    except FileNotFoundError:
        data = {}
    return data


def save_data_to_cache(data):
    with open('cache.pickle', 'wb') as f:
        pickle.dump(data, f)


def get_coordinate(university):
    cache = load_data_from_cache()
    if university in cache:
        return cache[university]

    university_name = university

    search_query = f"{university_name} coordinates"
    for j in search(search_query, num_results=1):
        response = requests.get(j)
        title = BeautifulSoup(response.text, 'html.parser').find(
            'title').prettify()
        if "Latitude" in title:
            latitude_start = title.find("Latitude: ") + len("Latitude: ")
            latitude_end = title.find(" Longitude: ")
            latitude = title[latitude_start:latitude_end].strip()

            longitude_start = title.find("Longitude: ") + len("Longitude: ")
            longitude_end = title.find("</title>")
            longitude = title[longitude_start:longitude_end].strip()
            cache[university] = latitude, longitude
            save_data_to_cache(cache)
            return latitude, longitude
    return None, None
