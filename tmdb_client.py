import requests
import os


api_token = os.environ.get("TMDB_API_TOKEN", "")
api_token2 = os.environ.get("TMDB_API_TOKEN2", "")


def call_tmdb_api(endpoint):
   full_url = f"https://api.themoviedb.org/3/{endpoint}"
   headers = {
       "Authorization": f"Bearer {api_token}"
   }
   response = requests.get(full_url, headers=headers)
   response.raise_for_status()
   
   return response.json()

def get_movies(listType='popular'):
    return call_tmdb_api(f'movie/{listType}')

def get_poster_url(url, size='w342'):
    baseUrl = 'https://image.tmdb.org/t/p/'
    return f'{baseUrl}{size}{url}'

def get_movie_database(howMany, listType='popular'):
    data = get_movies(listType)['results'][:howMany]
    return data

def get_single_movie(movieId):    
    return call_tmdb_api(f'movie/{movieId}')

def get_single_movie_cast(movieId):    
    return call_tmdb_api(f'movie/{movieId}/credits')['cast']

def get_movie_images(movieId):    
    return call_tmdb_api(f'movie/{movieId}/images')

def get_series_today(howMany):    
    return call_tmdb_api(f'/tv/airing_today')['results'][:howMany]

def search(searchQuery):
    baseUrl = 'https://api.themoviedb.org/3'
    endpoint = f'{baseUrl}/search/movie?api_key={api_token2}&query={searchQuery}'
    response = requests.get(endpoint)

    return response.json()['results']

def save_fav_in_file(movieId):
    with open("favlist.txt", "r+", encoding="UTF-8") as file:
        flag = True

        for line in file.readlines():            
            if movieId == line.replace('\n', ''):
                flag = False                

        if flag:
            file.write(movieId + '\n')
    return flag
