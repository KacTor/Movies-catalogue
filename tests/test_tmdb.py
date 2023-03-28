import tmdb_client
from unittest.mock import Mock
from main import app
import pytest

def test_get_poster_url_uses_default_size():
   # Przygotowanie danych
   poster_api_path = "some-poster-path"
   expected_default_size = 'w342'
   # Wywołanie kodu, który testujemy
   poster_url = tmdb_client.get_poster_url(poster_api_path)
   # Porównanie wyników
   assert expected_default_size in poster_url
   
def test_call_tmdb_api(monkeypatch):  
   mock_movies_list = ['Movie 1', 'Movie 2']

   requests_mock = Mock()   
   response = requests_mock.return_value
  
   response.json.return_value = mock_movies_list
   monkeypatch.setattr("tmdb_client.requests.get", requests_mock)

   movies_list = tmdb_client.call_tmdb_api("movie/popular")   
   assert movies_list == mock_movies_list
   
def test_get_single_movie():
   movieid= '631842'
   expected_result = ['title','tagline','overview','budget','genres']
   single_movie = tmdb_client.get_single_movie(movieid)
      
   for result in expected_result:
      assert result in single_movie
      
      
def test_get_movie_images():
   movieid= '631842'
   expected_result = 'backdrops'
   images = tmdb_client.get_movie_images(movieid)      
   
   assert expected_result in images and len(images[expected_result])>=2
   
def test_get_single_movie_cast():
   movieid= '631842'
   expected_result = ['profile_path','name','character']
   single_movie = tmdb_client.get_single_movie_cast(movieid)
      
   for result in expected_result:
      assert result in single_movie[0]



@pytest.mark.parametrize('n', (('popular'),('now_playing'),('lateddst')))
def test_homepage(monkeypatch,n):
   print(n)
   api_mock = Mock(return_value={'results': []})
   monkeypatch.setattr("tmdb_client.call_tmdb_api", api_mock)

   with app.test_client() as client:
      response = client.get(f'/?list_type={n}')
      assert response.status_code == 200 
      api_mock.assert_called_once_with(f'movie/{n}')