from flask import Flask, render_template

app = Flask(__name__)


@app.route('/<int:amountOfMovie>')
def homepage(amountOfMovie):
    movies = ['Sss', 'ddd', 'sdaw']
    return render_template("homepage.html", movies=movies[0:amountOfMovie])


if __name__ == "__main__":
    app.run(debug=True)
