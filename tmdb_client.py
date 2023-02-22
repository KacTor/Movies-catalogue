import requests
import random
from main import get_permission_api


def get_popular_movies():
    endpoint = "https://api.themoviedb.org/3/movie/popular"
    api_token = get_permission_api('config.ini')
    headers = {
        "Authorization": f"Bearer {api_token}"
    }
    response = requests.get(endpoint, headers=headers)
    return response.json()


def get_poster_url(url, size='w342'):
    baseUrl = 'https://image.tmdb.org/t/p/'
    return f'{baseUrl}{size}{url}'


def get_movie_info(howMany):
    data = get_popular_movies()['results'][:howMany]
    database = []

    for movie in data:
        database.append({'title': movie['original_title'],
                        'url_poster': get_poster_url(movie['poster_path']),
                         'id': movie['id']})
    random.shuffle(database)

    return database


def get_single_movie(movie_id):
    endpoint = f"https://api.themoviedb.org/3/movie/{movie_id}"
    api_token = get_permission_api('config.ini')
    headers = {
        "Authorization": f"Bearer {api_token}"
    }
    response = requests.get(endpoint, headers=headers)
    return response.json()


def get_single_movie_cast(movie_id):
    endpoint = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"
    api_token = get_permission_api('config.ini')
    headers = {
        "Authorization": f"Bearer {api_token}"
    }
    response = requests.get(endpoint, headers=headers)
    return response.json()['cast']


def get_movie_images(movie_id):
    endpoint = f"https://api.themoviedb.org/3/movie/{movie_id}/images"
    api_token = get_permission_api('config.ini')
    headers = {
        "Authorization": f"Bearer {api_token}"
    }
    response = requests.get(endpoint, headers=headers)
    return response.json()
