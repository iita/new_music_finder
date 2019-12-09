import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from random import randint
import webbrowser
import os

client_credentials_manager = SpotifyClientCredentials()

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def get_artist(q):
    artist_result = sp.search(q, limit=1, offset=randint(1000, 10000), type='artist', market=None)
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


album_arts = []
album_names = []

while len(album_arts) < 8:
    album = get_random_album()
    if album is not None:
        album_arts.append(album['album_art'])
        album_names.append(album['album_name'])
    else:
        print('no albums')

filename = 'spotipy_results.html'
f = open(filename, 'w')
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
  background-color: #052d2e;
}}

.container:hover .overlay {{
  opacity: 1;
}}

.text {{
  color: white;
  font-size: 18px;
  position: absolute;
  top: 50%;
  left: 50%;
  -webkit-transform: translate(-50%, -50%);
  -ms-transform: translate(-50%, -50%);
  transform: translate(-50%, -50%);
  text-align: center;
}}

.grid {{
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr;
  grid-gap: 5px;
  align-items: stretch;
  justify-items: center;
  }}
</style>
</head>
<body bgcolor="052d2e">
<main class="grid">
    <div class="container">
        <img src={} alt="test" class="image">
        <div class="overlay">
            <div class="text">{}</div>
        </div>
    </div>
    <div class="container">
        <img src={} alt="test" class="image">
        <div class="overlay">
            <div class="text">{}</div>
        </div>
    </div>
    <div class="container">
        <img src={} alt="test" class="image">
        <div class="overlay">
            <div class="text">{}</div>
        </div>
    </div>
    <div class="container">
        <img src={} alt="test" class="image">
        <div class="overlay">
            <div class="text">{}</div>
        </div>
    </div>
    <div class="container">
        <img src={} alt="test" class="image">
        <div class="overlay">
            <div class="text">{}</div>
        </div>
    </div>
    <div class="container">
        <img src={} alt="test" class="image">
        <div class="overlay">
            <div class="text">{}</div>
        </div>
    </div>
    <div class="container">
        <img src={} alt="test" class="image">
        <div class="overlay">
            <div class="text">{}</div>
        </div>
    </div>
    <div class="container">
        <img src={} alt="test" class="image">
        <div class="overlay">
            <div class="text">{}</div>
        </div>
    </div>
</div>
</body>
</html>
""".format(album_arts[0], album_names[0], album_arts[1], album_names[1], album_arts[2], album_names[2],
           album_arts[3], album_names[3], album_arts[4], album_names[4], album_arts[5], album_names[5],
           album_arts[6], album_names[6], album_arts[7], album_names[7])

f.write(html_string)
f.close()

webbrowser.open('file://'+os.path.realpath(filename))