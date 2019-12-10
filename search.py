import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from random import randint
import webbrowser
import os
from flask import Flask, render_template


client_credentials_manager = SpotifyClientCredentials()

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def get_artist(q):
    artist_result = sp.search(q, limit=1, offset=randint(100, 10000), type='artist', market=None)
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


def get_random_album():
    year1, year2 = get_random_years(1980,2010)
    q = 'year:{}-{}'.format(year1, year2)
    artist = get_artist(q)
    album_ids = get_album_ids(artist['id'])
    n = len(album_ids)
    if n > 1:
        random_album = randint(0, n-1)
    elif n == 0:
        return None
    else:
        random_album = 0
    album_info = get_album(album_ids[random_album])
    return album_info


def get_random_years(start=1950, end=2020):
    year1 = randint(start, end)
    year2 = year1+5
    year1 = str(year1)
    year2 = str(year2)
    return year1, year2


def get_website():
    album_arts = []
    album_names = []
    artist_names = []
    album_links = []

    while len(album_arts) < 15:
        album = get_random_album()
        if album is not None:
            album_arts.append(album['album_art'])
            album_names.append(album['album_name'])
            artist_names.append(album['artist_name'])
            album_links.append(album['album_link'])
        else:
            print('no albums')

   # filename = 'spotipy_results.html'
   # f = open(filename, 'w')
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

   # f.write(html_string)
   # f.close()
    return html_string


get_website()


app = Flask(__name__)

@app.route("/")
def index():
    content = """
            <!DOCTYPE html>
        <html>
           <head>
              <title>Title of the document</title>
              <style>
                 .button {
                 background-color: #1c87c9;
                 border: none;
                 color: white;
                 padding: 20px 34px;
                 text-align: center;
                 text-decoration: none;
                 display: inline-block;
                 font-size: 20px;
                 margin: 4px 2px;
                 cursor: pointer;
                 }
              </style>
           </head>
           <body>
              <a href="/results" class="button">Click Here</a>
           </body>
        </html>"""
    return content


@app.route("/results")
def results():
    content = get_website()
    return content

if __name__ == "__main__":
    app.run(debug=True)