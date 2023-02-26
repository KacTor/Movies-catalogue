from flask import Flask, render_template, request
import tmdb_client
import configparser
import os
import random
from datetime import date
from pprint import pprint


def get_permission_api(fileName: str, variable: str):
    config = configparser.ConfigParser()
    config.read(
        os.path.join(os.path.dirname(
            os.path.abspath(__file__)), fileName))

    APIKEY = config['DEFAULT'][variable]

    return APIKEY


app = Flask(__name__)


@app.route('/')
def homepage():
    today = date.today().strftime("%d.%m.%Y")
    availableLists = ['popular', 'now_playing',
                      'top_rated', 'upcoming', 'latest']
    selected_list = request.args.get('list_type', 'popular')
    try:
        dataBase = tmdb_client.get_movie_database(8, selected_list)
        pprint(dataBase)

    except:
        selected_list = 'popular'
        dataBase = tmdb_client.get_movie_database(8, selected_list)

    random.shuffle(dataBase)
    return render_template("homepage.html", dataBase=dataBase, availableLists=availableLists, selected_list=selected_list, today=today)


@app.route("/movie/<movieId>")
def movie_details(movieId):
    details = tmdb_client.get_single_movie(movieId)
    cast = tmdb_client.get_single_movie_cast(movieId)[:4]
    image = random.choice(tmdb_client.get_movie_images(movieId)['backdrops'])

    return render_template("movie_details.html", movie=details, cast=cast, image=image)


@app.route("/search")
def search():
    searchQuery = request.args.get('q', '')
    searchMovie = tmdb_client.search(searchQuery)[:8]
    print(searchMovie)

    return render_template('search.html', searchMovie=searchMovie)


@app.route("/today")
def today_series():
    today = date.today().strftime("%d.%m.%Y")
    dataBase = tmdb_client.get_series_today(8)
    pprint(dataBase)

    return render_template('today.html', dataBase=dataBase, today=today)


@app.context_processor
def utility_processor():
    def tmdb_image_url(path, size):
        return tmdb_client.get_poster_url(path, size)
    return {"tmdb_image_url": tmdb_image_url}


if __name__ == "__main__":
    app.run(debug=True)
