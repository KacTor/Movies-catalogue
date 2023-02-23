import requests
from main import get_permission_api


api_token = get_permission_api('config.ini')


def get_movies(listType='popular'):
    endpoint = f"https://api.themoviedb.org/3/movie/{listType}"
    headers = {
        "Authorization": f"Bearer {api_token}"
    }
    response = requests.get(endpoint, headers=headers)
    response.raise_for_status()
    return response.json()


def get_poster_url(url, size='w342'):
    baseUrl = 'https://image.tmdb.org/t/p/'
    return f'{baseUrl}{size}{url}'


def get_movie_database(howMany, listType='popular'):
    data = get_movies(listType)['results'][:howMany]
    return data


def get_single_movie(movieId):
    endpoint = f"https://api.themoviedb.org/3/movie/{movieId}"
    headers = {
        "Authorization": f"Bearer {api_token}"
    }
    response = requests.get(endpoint, headers=headers)
    return response.json()


def get_single_movie_cast(movieId):
    endpoint = f"https://api.themoviedb.org/3/movie/{movieId}/credits"
    headers = {
        "Authorization": f"Bearer {api_token}"
    }
    response = requests.get(endpoint, headers=headers)
    return response.json()['cast']


def get_movie_images(movieId):
    endpoint = f"https://api.themoviedb.org/3/movie/{movieId}/images"
    headers = {
        "Authorization": f"Bearer {api_token}"
    }
    response = requests.get(endpoint, headers=headers)
    return response.json()


def get_movie_list(movieId):
    endpoint = f"https://api.themoviedb.org/3/movie/{movieId}/lists"
    headers = {
        "Authorization": f"Bearer {api_token}"
    }
    response = requests.get(endpoint, headers=headers)
    return response.json()['results']
