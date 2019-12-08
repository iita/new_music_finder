import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from random import randint
import webbrowser
import os

client_credentials_manager = SpotifyClientCredentials()

randint(1000, 2000)

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
q = 'year:2011-2012'


def get_artist():
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


ar1 = get_artist()
alb1 = get_album_ids(ar1['id'])
alb2 = get_album(alb1[0])
print(alb1)
print(ar1)
print(alb2)


filename = 'spotipy_results.html'
f = open(filename, 'w')
html_string = """
<!DOCTYPE html>
<html lang="en">
<title>W3.CSS Template</title>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Raleway">
<style>
body,h1,h2,h3,h4,h5 {{font-family: "Raleway", sans-serif}}

.w3-quarter img{{margin-bottom: -6px; cursor: pointer}}
.w3-quarter img:hover{{opacity: 0.6; transition: 0.3s}}
</style>
<body class="w3-light-grey">

<!-- Top menu on small screens -->
<header class="w3-container w3-top w3-white w3-xlarge w3-padding-16">
  <span class="w3-left w3-padding">EXPLORE</span>
  <a href="javascript:void(0)" class="w3-right w3-button w3-white" onclick="w3_open()">☰</a>
</header>

<!-- !PAGE CONTENT! -->
<div class="w3-main w3-content" style="max-width:1600px;margin-top:83px">
  
  <!-- Photo grid -->
  <div class="w3-row w3-grayscale-min">
    <div class="w3-quarter">
    <img src={} style="width:100%" onclick="onClick(this)" alt="{}">
    <img src={} style="width:100%" onclick="onClick(this)" alt="{}">
    <img src={} style="width:100%" onclick="onClick(this)" alt="{}">
  </div>
    
   <div class="w3-quarter">
    <img src={} style="width:100%" onclick="onClick(this)" alt="{}">
    <img src={} style="width:100%" onclick="onClick(this)" alt="{}">
    <img src={} style="width:100%" onclick="onClick(this)" alt="{}">
  </div>
  
  <div class="w3-quarter">
    <img src={} style="width:100%" onclick="onClick(this)" alt="{}">
    <img src={} style="width:100%" onclick="onClick(this)" alt="{}">
    <img src={} style="width:100%" onclick="onClick(this)" alt="{}">
  </div>

  <div class="w3-quarter">
    <img src={} style="width:100%" onclick="onClick(this)" alt="{}">
    <img src={} style="width:100%" onclick="onClick(this)" alt="{}">
    <img src={} style="width:100%" onclick="onClick(this)" alt="{}">
  </div>
</div>

  <!-- Modal for full size images on click-->
  <div id="modal01" class="w3-modal w3-black" style="padding-top:0" onclick="this.style.display='none'">
    <span class="w3-button w3-black w3-xlarge w3-display-topright">×</span>
    <div class="w3-modal-content w3-animate-zoom w3-center w3-transparent w3-padding-64">
      <img id="img01" class="w3-image">
      <p id="caption"></p>
    </div>
  </div>

<!-- End page content -->
</div>

<script>
// Script to open and close sidebar
function w3_open() {{
  document.getElementById("mySidebar").style.display = "block";
  document.getElementById("myOverlay").style.display = "block";
}}

function w3_close() {{
  document.getElementById("mySidebar").style.display = "none";
  document.getElementById("myOverlay").style.display = "none";
}}

// Modal Image Gallery
function onClick(element) {{
  document.getElementById("img01").src = element.src;
  document.getElementById("modal01").style.display = "block";
  var captionText = document.getElementById("caption");
  captionText.innerHTML = element.alt;
}}

</script>


</body>
</html>
""".format(album_arts[0], album_names[0], album_arts[1], album_names[1], album_arts[2], album_names[2],
           album_arts[3], album_names[3], album_arts[4], album_names[4], album_arts[5], album_names[5],
           album_arts[6], album_names[6], album_arts[7], album_names[7], album_arts[8], album_names[8],
           album_arts[9], album_names[9], album_arts[10], album_names[10], album_arts[11], album_names[11])


def add_album(artist, album_name, album_art, tracks, link):
    album_string = """
    <img src={}>
    <h1>{}</h1
    <h2><b>{}</b></h2>
    """.format(album_art, artist, album_name)
    f.write(album_string)
    for i in tracks:
        f.write('<li>'+i+'</li>')
    f.write('<p><a href={}>Spotify link</a></p>'.format(link))


def write_selection(n):
    f.write(html_string)
    u = 1
    while u<n:
        artist, album_name, album_art, tracks, link = get_artist_album_tracks(randint(1000, 10000))
        add_album(artist, album_name, album_art, tracks, link)
        u = u+1
    f.write("""</body>
    </html>
    """)
    f.close()

f.write(html_string)
f.close()

webbrowser.open('file://'+os.path.realpath(filename))