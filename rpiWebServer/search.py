import webbrowser
import os
from quart import Quart, request
import asyncio
import utils.fetch as fetch


app = Quart(__name__)


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
    app.run(host='0.0.0.0')
