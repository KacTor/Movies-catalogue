from flask import Flask, render_template
import tmdb_client
import configparser
import os
import random


def get_permission_api(fileName: str):
    config = configparser.ConfigParser()
    config.read(
        os.path.join(os.path.dirname(
            os.path.abspath(__file__)), fileName))

    APIKEY = config['DEFAULT']['apiKey']

    return APIKEY


app = Flask(__name__)


@app.route('/')
def homepage():
    dataBase = tmdb_client.get_movie_info(8)
    return render_template("homepage.html", dataBase=dataBase)


@app.route("/movie/<movieId>")
def movie_details(movieId):
    details = tmdb_client.get_single_movie(movieId)
    cast = tmdb_client.get_single_movie_cast(movieId)[:4]
    image = random.choice(tmdb_client.get_movie_images(movieId)['backdrops'])

    return render_template("movie_details.html", movie=details, cast=cast, image=image)


@app.context_processor
def utility_processor():
    def tmdb_image_url(path, size):
        return tmdb_client.get_poster_url(path, size)
    return {"tmdb_image_url": tmdb_image_url}


if __name__ == "__main__":
    app.run(debug=True)
