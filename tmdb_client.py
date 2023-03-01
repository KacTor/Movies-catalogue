import requests
from main import get_permission_api


api_token = get_permission_api('config.ini', 'apiKey')
api_token2 = get_permission_api('config.ini', 'apiKey2')


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


def search(searchQuery):
    baseUrl = 'https://api.themoviedb.org/3'
    endpoint = f'{baseUrl}/search/movie?api_key={api_token2}&query={searchQuery}'
    response = requests.get(endpoint)

    return response.json()['results']


def get_series_today(howMany):
    baseUrl = 'https://api.themoviedb.org/3'
    endpoint = f'{baseUrl}/tv/airing_today'
    headers = {
        "Authorization": f"Bearer {api_token}"
    }
    response = requests.get(endpoint, headers=headers)
    response.raise_for_status()
    return response.json()['results'][:howMany]


def save_fav_in_file(movieId):
    with open("favlist.txt", "r+", encoding="UTF-8") as file:
        flag = True

        for line in file.readlines():            
            if movieId == line.replace('\n', ''):
                flag = False                

        if flag:
            file.write(movieId + '\n')
        else:
            flag = True
