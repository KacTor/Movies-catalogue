from flask import Flask, render_template, request, url_for, redirect, flash
import tmdb_client
import random
from datetime import date


app = Flask(__name__)

app.secret_key = b'h5tfr6g'


FAVORITES = set()


@app.route('/')
def homepage():
    today = date.today().strftime("%d.%m.%Y")
    availableLists = ['popular', 'now_playing',
                      'top_rated', 'upcoming', 'latest']
    selected_list = request.args.get('list_type', 'popular')
    try:
        dataBase = tmdb_client.get_movie_database(8, selected_list)        

    except:
        selected_list = 'popular'
        dataBase = tmdb_client.get_movie_database(8, selected_list)

    random.shuffle(dataBase)
    return render_template("homepage.html", dataBase=dataBase, availableLists=availableLists, selected_list=selected_list, today=today)


@app.route("/movie/<movieId>")
def movie_details(movieId):
    print(movieId)
    details = tmdb_client.get_single_movie(movieId)
    cast = tmdb_client.get_single_movie_cast(movieId)[:4]
    image = random.choice(tmdb_client.get_movie_images(movieId)['backdrops'])

    return render_template("movie_details.html", movie=details, cast=cast, image=image)


@app.route("/search")
def search():
    searchQuery = request.args.get('q', '')
    searchMovie = tmdb_client.search(searchQuery)[:8]

    return render_template('search.html', searchMovie=searchMovie)


@app.route("/today")
def today_series():
    today = date.today().strftime("%d.%m.%Y")
    dataBase = tmdb_client.get_series_today(8)

    return render_template('today.html', dataBase=dataBase, today=today)


@app.route("/favorites/add", methods=['POST'])
def add_favorite():
    movieId = request.form.get('movieId')
    flag = tmdb_client.save_fav_in_file(movieId)
    title = tmdb_client.get_single_movie(movieId)['title']

    if flag:
        flash(f'{title} was successfully add.')
    else:
        flash(f'{title} is already in favorite.')

    return redirect(url_for('homepage'))


@app.route("/favorites/list")
def show_favorite():
    dataBase = []

    with open("favlist.txt", "r", encoding="UTF-8") as file:
        idList = file.read().splitlines()

    for id in idList:
        dataBase.append(tmdb_client.get_single_movie(id))

    return render_template('fav.html', dataBase=dataBase)


@app.context_processor
def utility_processor():
    def tmdb_image_url(path, size):
        return tmdb_client.get_poster_url(path, size)
    return {"tmdb_image_url": tmdb_image_url}


if __name__ == "__main__":
    app.run(debug=True)
