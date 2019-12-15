import webbrowser
import os
from flask import Flask, request

import utils.fetch as fetch


app = Flask(__name__)


@app.route("/")
def input_genre():
    if 'genre' in request.args:
        name = request.args['genre']
        content = fetch.get_website(name)
    else:
        content = fetch.get_genre_html()
    return content


@app.route("/genre/<name>")
def genre(name):
    content = fetch.get_website(name)
    return content


@app.route("/results")
def results():
    content = fetch.get_website()
    return content


if __name__ == "__main__":
    app.run(debug=True, port=1025, host='0.0.0.0')
