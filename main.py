from flask import Flask, render_template

app = Flask(__name__)


@app.route('/<int:amountOfMovie>')
def homepage(amountOfMovie):
    movies = ['Movie1', 'Movie2', 'Movie3']
    return render_template("homepage.html", movies=movies[0:amountOfMovie])


if __name__ == "__main__":
    app.run(debug=True)
