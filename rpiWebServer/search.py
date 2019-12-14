import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from random import randint
import webbrowser
import os
from flask import Flask, render_template


def get_sp():
    client_credentials_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    return sp



def get_artist():
    year1, year2 = get_random_years()
    q = 'year:{}-{}'.format(year1, year2)
    search_index = randint(100, 10000)
    artist_result = sp.search(q, limit=1, offset=search_index, type='artist', market=None)
    artist = {
        "name": artist_result['artists']['items'][0]['name'],
        "id": artist_result['artists']['items'][0]['id'],
        "genres": artist_result['artists']['items'][0]['genres'],
        "popularity": artist_result['artists']['items'][0]['popularity']
    }
    return artist


def get_album_ids(artist_id):
    album_result = sp.artist_albums(artist_id, album_type='album')
    album_ids = []
    for album in album_result['items']:
        album_ids.append(album['id'])
    return album_ids


def get_tracks(album_id):
    tracks = []
    tracks_result = sp.album_tracks(album_id)
    for track in tracks_result['items']:
        tracks.append(
            track['name']
            )
    return tracks


def get_album(album_id):
    album_result = sp.album(album_id)
    albums = {
            "artist_name": album_result['artists'][0]['name'],
            "album_name": album_result['name'],
            "album_id": album_result['id'],
            "album_art": album_result['images'][0]['url'],
            "release_date": album_result['release_date'],
            "album_genres": album_result['genres'],
            "album_link": album_result['external_urls']['spotify'],
            "album_tracks": get_tracks(album_result['id'])
        }
    return albums


def get_random_album(artist):
    album_ids = get_album_ids(artist['id'])
    n = len(album_ids)
    if n > 1:
        random_album = randint(0, n-1)
    elif n == 0:
        return None
    else:
        random_album = 0
    album_info = album_ids[random_album]
    return album_info


def get_random_years(start=1950, end=2020):
    year1 = randint(start, end)
    year2 = year1+5
    year1 = str(year1)
    year2 = str(year2)
    return year1, year2


def get_artist_album():
    artist = get_artist()
    album_list = get_album_ids(artist['id'])
    n = len(album_list)
    if n == 0:
        return None
    elif n == 1:
        return album_list[0]
    else:
        return album_list[randint(0, n-1)]


def get_lists():
    albums = []
    while len(albums) < 15:
        album = get_artist_album()
        if album is not None:
            albums.append(album)
    return albums


def get_albums(albums):
    album_result = sp.albums(albums)['albums']
    albums_list = []
    for album in album_result:
        dict = {
            "artist_name": album['artists'][0]['name'],
            "album_name": album['name'],
            "album_id": album['id'],
            "album_art": album['images'][0]['url'],
            "release_date": album['release_date'],
            "album_genres": album['genres'],
            "album_link": album['external_urls']['spotify'],
            "album_tracks": get_tracks(album['id'])
        }
        albums_list.append(dict)
    return albums_list





def get_website():
    album_arts = []
    album_names = []
    artist_names = []
    album_links = []

    album_ids = get_lists()
    albums = get_albums(album_ids)
    for album in albums:
        album_arts.append(album['album_art'])
        album_names.append(album['album_name'])
        artist_names.append(album['artist_name'])
        album_links.append(album['album_link'])

    #filename = 'spotipy_results.html'
    #f = open(filename, 'w')
    html_string = """
    <!DOCTYPE html>
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
    .container {{
      position: relative;
      width: 100%;
    }}

    .image {{
      display: block;
      width: 100%;
      height: auto;
    }}

    .overlay {{
      position: absolute;
      top: 0;
      bottom: 0;
      left: 0;
      right: 0;
      height: 100%;
      width: 100%;
      opacity: 0;
      transition: .2s ease;
      background-color: #000000;
    }}

    .container:hover .overlay {{
      opacity: 0.8;
    }}

    .album_text {{
      color: #d8dee3;
      font-size: 18px;
      position: absolute;
      top: 60%;
      left: 50%;
      -webkit-transform: translate(-50%, -50%);
      -ms-transform: translate(-50%, -50%);
      transform: translate(-50%, -50%);
      text-align: center;
    }}

    .artist_text {{
      color: #d8dee3;
      font-size: 22px;
      position: absolute;
      top: 20%;
      left: 50%;
      -webkit-transform: translate(-50%, -50%);
      -ms-transform: translate(-50%, -50%);
      transform: translate(-50%, -50%);
      text-align: center;
    }}

    .grid {{
      display: grid;
      grid-template-columns: 1fr 1fr 1fr 1fr 1fr;
      grid-gap: 5px;
      align-items: stretch;
      justify-items: center;
      }}
    </style>
    </head>
    <body bgcolor="000000">
    <main class="grid">
        <a href="{}" class="container">
            <img src={} alt="test" class="image">
            <div class="overlay">
                <div class="artist_text">{}</div>
                <div class="album_text">{}</div>
            </div>
        </a>
        <a href="{}" class="container">
            <img src={} alt="test" class="image">
            <div class="overlay">
                <<div class="artist_text">{}</div>
                <div class="album_text">{}</div>
            </div>
        </a>
        <a href="{}" class="container">
            <img src={} alt="test" class="image">
            <div class="overlay">
                <div class="artist_text">{}</div>
                <div class="album_text">{}</div>
            </div>
        </a>
        <a href="{}" class="container">
            <img src={} alt="test" class="image">
            <div class="overlay">
                <div class="artist_text">{}</div>
                <div class="album_text">{}</div>
            </div>
        </a>
        <a href="{}" class="container">
            <img src={} alt="test" class="image">
            <div class="overlay">
                <<div class="artist_text">{}</div>
                <div class="album_text">{}</div>
            </div>
        </a>
        <a href="{}" class="container">
            <img src={} alt="test" class="image">
            <div class="overlay">
                <div class="artist_text">{}</div>
                <div class="album_text">{}</div>
            </div>
        </a>
        <a href="{}" class="container">
            <img src={} alt="test" class="image">
            <div class="overlay">
                <div class="artist_text">{}</div>
                <div class="album_text">{}</div>
            </div>
        </a>
        <a href="{}" class="container">
            <img src={} alt="test" class="image">
            <div class="overlay">
                <div class="artist_text">{}</div>
                <div class="album_text">{}</div>
            </div>
        </a>
        <a href="{}" class="container">
            <img src={} alt="test" class="image">
            <div class="overlay">
                <div class="artist_text">{}</div>
                <div class="album_text">{}</div>
            </div>
        </a>
        <a href="{}" class="container">
            <img src={} alt="test" class="image">
            <div class="overlay">
                <div class="artist_text">{}</div>
                <div class="album_text">{}</div>
            </div>
        </a>
        <a href="{}" class="container">
            <img src={} alt="test" class="image">
            <div class="overlay">
                <div class="artist_text">{}</div>
                <div class="album_text">{}</div>
            </div>
        </a>
        <a href="{}" class="container">
            <img src={} alt="test" class="image">
            <div class="overlay">
                <div class="artist_text">{}</div>
                <div class="album_text">{}</div>
            </div>
        </a>
        <a href="{}" class="container">
            <img src={} alt="test" class="image">
            <div class="overlay">
                <div class="artist_text">{}</div>
                <div class="album_text">{}</div>
            </div>
        </a>
        <a href="{}" class="container">
            <img src={} alt="test" class="image">
            <div class="overlay">
                <div class="artist_text">{}</div>
                <div class="album_text">{}</div>
            </div>
        </a>
        <a href="{}" class="container">
            <img src={} alt="test" class="image">
            <div class="overlay">
                <div class="artist_text">{}</div>
                <div class="album_text">{}</div>
            </div>
        </a>
    </div>
    </body>
    </html>
    """.format(album_links[0], album_arts[0], artist_names[0], album_names[0],
               album_links[1], album_arts[1], artist_names[1], album_names[1],
               album_links[2], album_arts[2], artist_names[2], album_names[2],
               album_links[3], album_arts[3], artist_names[3], album_names[3],
               album_links[4], album_arts[4], artist_names[4], album_names[4],
               album_links[5], album_arts[5], artist_names[5], album_names[5],
               album_links[6], album_arts[6], artist_names[6], album_names[6],
               album_links[7], album_arts[7], artist_names[7], album_names[7],
               album_links[8], album_arts[8], artist_names[8], album_names[8],
               album_links[9], album_arts[9], artist_names[9], album_names[9],
               album_links[10], album_arts[10], artist_names[10], album_names[10],
               album_links[11], album_arts[11], artist_names[11], album_names[11],
               album_links[12], album_arts[12], artist_names[12], album_names[12],
               album_links[13], album_arts[13], artist_names[13], album_names[13],
               album_links[14], album_arts[14], artist_names[14], album_names[14])

    #f.write(html_string)
    #f.close()
    return html_string

sp = get_sp()
app = Flask(__name__)

@app.route("/")
def index():
    content = """
        <!DOCTYPE html>
        <html>
           <head>
              <title>Try it yourself</title>
              <style>
                html {
                    border: 0;
                    margin: 0;
                    padding: 0;
                    width: 100%;
                    height: auto;
                    -webkit-box-sizing: border-box;
                    -moz-box-sizing: border-box;
                    box-sizing: border-box;
                }

                *,*:before,*:after {
                    -webkit-box-sizing: inherit;
                    -moz-box-sizing: inherit;
                    box-sizing: inherit;
                }

                body {
                    background-image: url("/static/bg.jpg");
                    padding: 0;
                    margin: 0;
                    height: auto;
                    width: 100%;
                }

                b {
                position: relative;
                display: block;
                font-family: helvetica neue, helvetica, sans-serif;
                line-height: 1.15em;
                margin-top: -1.15em;
                top: 2.3em;
                font-size: 0.67em;
                font-weight: 400;
                letter-spacing: 0.025em;
                opacity: 0.75;
                text-align: center;
                }

                b span {
                font-size: 0.785em;
                font-weight: 400;
                opacity: 0.4;
                }

                #intro {
                width: 200px;
                margin: 100px auto 0;
                }

                .button {
                    display: inline-block;
                    text-decoration: none;
                    position: relative;
                    margin-top: 80px;
                }

                .button .bottom {
                    position: absolute;
                    left: 7px;
                    top: 7px;
                    width: 100%;
                    height: 100%;
                    background-color: #a1c2a7;
                    display: block;
                    -webkit-transition: all .15s ease-out;
                    -moz-transition: all .15s ease-out;
                    -o-transition: all .15s ease-out;
                    transition: all .15s ease-out;
                }

                .button .top {
                    position: relative;
                    left: 0;
                    top: 0;
                    width: 100%;
                    height: 100%;
                    padding: 24px 34px 22px 34px;
                    border: 2px solid #1d3c51;
                }

                .button-dark .top {
                    border: 2px solid #f7f7df;
                }

                .button .top .label {
                    font-family: sans-serif;
                    font-weight: 600;
                    color: #1d3c51;
                    font-size: 12px;
                    line-height: 110%;
                    letter-spacing: 2px;
                    text-align: center;
                    text-transform: uppercase;
                    -webkit-transition: all .15s ease-out;
                    -moz-transition: all .15s ease-out;
                    -o-transition: all .15s ease-out;
                    transition: all .15s ease-out;
                }

                .button-dark .top .label {
                    color: #f7f7df;
                }

                .button:hover .bottom {
                    left: 0;
                    top: 0;
                    opacity: 0.05;
                    background-color: #f5f6d7;
                }

                .button:hover .top .label {
                    color: #59c6c0;
                }

                .button-border {
                    position: absolute;
                    background-color: #59c6c0;
                    -webkit-transition: all .25s ease-out;
                    -moz-transition: all .25s ease-out;
                    -o-transition: all .25s ease-out;
                    transition: all .25s ease-out;
                }

                .button:hover .top .button-border-left,.button:hover .top .button-border-right {
                    height: calc(100% + 2px);
                }

                .button:hover .top .button-border-top,.button:hover .top .button-border-bottom {
                    width: calc(100% + 2px);
                }

                .button-border-left {
                    left: -2px;
                    bottom: -2px;
                    width: 2px;
                    height: 0;
                }

                .button-border-top {
                    left: -2px;
                    top: -2px;
                    width: 0;
                    height: 2px;
                }

                .button-border-right {
                    right: -2px;
                    top: -2px;
                    width: 2px;
                    height: 0;
                }

                .button-border-bottom {
                    right: -2px;
                    bottom: -2px;
                    width: 0;
                    height: 2px;
                }
              </style>
           </head>
           <body>

                <section id="intro">

                  <div id="intro-content" class="center-content">

                    <div class="center-content-inner">

                      <div class="content-section content-section-margin">

                        <div class="content-section-grid clearfix">

                        <a href="/results" class="button nav-link">

                          <div class="bottom"></div>

                          <div class="top">

                          <div class="label">Discover</div>

                                <div class="button-border button-border-left"></div>
                              <div class="button-border button-border-top"></div>
                              <div class="button-border button-border-right"></div>
                                <div class="button-border button-border-bottom"></div>

                          </div>

                            </a>

                        </div>

                       </div>

                      </div>

                     </div>

                  </section>
            </div>
           </body>
        </html>
   """
    return content


@app.route("/results")
def results():
    content = get_website()
    return content


if __name__ == "__main__":
    app.run(debug=True, port=1025, host='0.0.0.0')
