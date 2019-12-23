import aiospotipy
import asyncio
from spotipy.oauth2 import SpotifyClientCredentials
from random import randint


def get_sp():
    client_credentials_manager = SpotifyClientCredentials()
    sp = aiospotipy.Spotify(client_credentials_manager=client_credentials_manager)
    return sp


async def get_artist():
    sp = get_sp()
    year1, year2 = get_random_years()
    q = 'year:{}-{}'.format(year1, year2)
    search_index = randint(100, 10000)
    artist_result = await sp.search_artist(q, limit=1, offset=search_index, market=None)
    artist = {
        "name": artist_result['artists']['items'][0]['name'],
        "id": artist_result['artists']['items'][0]['id'],
        "genres": artist_result['artists']['items'][0]['genres'],
        "popularity": artist_result['artists']['items'][0]['popularity']
    }
    return artist

def get_artist_from_genre(genre):
    sp = get_sp()
    q = 'genre:"{}"'.format(genre)
    search_max = 1000
    search_index = randint(0, search_max)
    artist_result = sp.search(q, limit=1, offset=search_index, type='artist', market=None)
    while len(artist_result['artists']['items']) == 0:
        search_max = search_index
        search_index = randint(0, search_max)
        artist_result = sp.search(q, limit=1, offset=search_index, type='artist', market=None)
        if search_index == 0:
            artist = 'no artists found'
            return artist
    artist = {
        "name": artist_result['artists']['items'][0]['name'],
        "id": artist_result['artists']['items'][0]['id'],
        "genres": artist_result['artists']['items'][0]['genres'],
        "popularity": artist_result['artists']['items'][0]['popularity']
    }
    return artist


def get_album_ids(artist_id):
    sp = get_sp()
    album_result = sp.artist_albums(artist_id, album_type='album')
    album_ids = []
    for album in album_result['items']:
        if len(album['images'])!=0:
            album_ids.append(album['id'])
    return album_ids


def get_tracks(album_id):
    sp = get_sp()
    tracks = []
    tracks_result = sp.album_tracks(album_id)
    for track in tracks_result['items']:
        tracks.append(
            track['name']
            )
    return tracks


def get_album(album_id):
    sp = get_sp()
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


def get_random_years(start=1950, end=2020):
    year1 = randint(start, end)
    year2 = year1+5
    year1 = str(year1)
    year2 = str(year2)
    return year1, year2


def get_artist_album(genre=None):
    if genre is None:
        artist = get_artist()
    else:
        artist = get_artist_from_genre(genre)
    if artist == 'no artists found':
        return 'NOPE'
    album_list = get_album_ids(artist['id'])
    if album_list == 'NOPE':
        return 'NOPE'
    n = len(album_list)
    if n == 0:
        return None
    elif n == 1:
        return album_list[0]
    else:
        return album_list[randint(0, n-1)]


def get_album_list(genre=None):
    album_ids = []
    while len(album_ids) < 15:
        album = get_artist_album(genre)
        if album == 'NOPE':
            return album
        elif album is not None:
            album_ids.append(album)
    return album_ids


def get_albums(genre=None):
    sp = get_sp()
    album_ids = get_album_list(genre)
    if album_ids == 'NOPE':
        return 'NOPE'
    album_result = sp.albums(album_ids)['albums']
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


async def get_artist_genre():
    artist = await get_artist()
    genre_list = artist['genres']
    n = len(genre_list)
    if n == 0:
        return None
    elif n == 1:
        return genre_list[0]
    else:
        return genre_list[randint(0, n-1)]


async def get_one_genre():
    genre = await get_artist_genre()
    while genre is None:
        genre = await get_artist_genre()
    return genre


async def get_genres():
    genres = await asyncio.gather(
        get_one_genre(),
        get_one_genre(),
        get_one_genre(),
        get_one_genre(),
        get_one_genre(),
        get_one_genre(),
        get_one_genre(),
        get_one_genre(),
        get_one_genre(),
        get_one_genre(),
        get_one_genre(),
        get_one_genre()
    )
    return genres

artist = asyncio.run(get_artist())
print(artist)

async def get_genre_html(error=False, fail=None):
    genres = await get_genres()
    if error is True:
        background = 'error'
        message = 'Nothing found for "'+fail+'" - try something new instead?'
        query = 'Or try again:'
    else:
        background = 'bg'
        message = 'Go Outside Your Comfort Zone'
        query = 'Or input genre:'

    html_string = """
                <!DOCTYPE html>
            <html>
               <head>
                  <title>Try it yourself</title>
                  <style>
                    html {{
                        border: 0;
                        margin: 0;
                        padding: 0;
                        width: 100%;
                        height: auto;
                        -webkit-box-sizing: border-box;
                        -moz-box-sizing: border-box;
                        box-sizing: border-box;
                    }}

                    *,*:before,*:after {{
                        -webkit-box-sizing: inherit;
                        -moz-box-sizing: inherit;
                        box-sizing: inherit;
                    }}

                    body {{
                        background-image: url("/static/{12}.jpg");
                        padding: 0;
                        margin: 0;
                        height: auto;
                        width: 100%;
                    }}

                    b {{
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
                    }}

                    b span {{
                    font-size: 0.785em;
                    font-weight: 400;
                    opacity: 0.4;
                    }}

                    #intro {{
                    width: 200px;
                    margin: 100px auto 0;
                    text-align: center;
                    }}

                    .button {{
                        display: inline-block;
                        text-decoration: none;
                        position: relative;
                        margin-top: 80px;
                    }}

                    .button .bottom {{
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
                    }}

                    .button .top {{
                        position: relative;
                        left: 0;
                        top: 0;
                        width: 100%;
                        height: 100%;
                        padding: 20px 24px 18px 24px;
                        border: 2px solid #1d3c51;
                    }}

                    .button-dark .top {{
                        border: 2px solid #375737;
                    }}

                    .button .top .label {{
                        font-family: sans-serif;
                        font-weight: 800;
                        color: #1d3c51;
                        font-size: 12px;
                        line-height: 140%;
                        letter-spacing: 2px;
                        text-align: center;
                        text-transform: uppercase;
                        -webkit-transition: all .15s ease-out;
                        -moz-transition: all .15s ease-out;
                        -o-transition: all .15s ease-out;
                        transition: all .15s ease-out;
                    }}

                    .button-dark .top .label {{
                        color: #375737;
                    }}

                    .button:hover .bottom {{
                        left: 0;
                        top: 0;
                        opacity: 0.05;
                        background-color: #f5f6d7;
                    }}

                    .button:hover .top .label {{
                        color: #59c6c0;
                    }}

                    .button-border {{
                        position: absolute;
                        background-color: #59c6c0;
                        -webkit-transition: all .25s ease-out;
                        -moz-transition: all .25s ease-out;
                        -o-transition: all .25s ease-out;
                        transition: all .25s ease-out;
                    }}

                    .button:hover .top .button-border-left,.button:hover .top .button-border-right {{
                        height: calc(100% + 2px);
                    }}

                    .button:hover .top .button-border-top,.button:hover .top .button-border-bottom {{
                        width: calc(100% + 2px);
                    }}

                    .button-border-left {{
                        left: -2px;
                        bottom: -2px;
                        width: 2px;
                        height: 0;
                    }}

                    .button-border-top {{
                        left: -2px;
                        top: -2px;
                        width: 0;
                        height: 2px;
                    }}

                    .button-border-right {{
                        right: -2px;
                        top: -2px;
                        width: 2px;
                        height: 0;
                    }}

                    .button-border-bottom {{
                        right: -2px;
                        bottom: -2px;
                        width: 0;
                        height: 2px;
                    }}
                .container{{
                    display: block;
                    margin-top: 200px;
                    text-align: center;
                }}
                .button1{{
                    display:inline-block;
                    padding:0.4em 0.8em;
                    border:0.15em solid #283b4c;
                    margin:0.1em 0.2em 0.4em 0.2em;
                    border-radius:0.2em;
                    box-sizing: border-box;
                    text-decoration:none;
                    font-family:sans-serif;
                    font-weight:600;
                    font-size: medium;
                    color:#296965;
                    background-color: #6e9b8a;
                    text-align:center;
                    transition: all 0.1s;
                    opacity: 0.9;
                }}
    .button1:hover{{
        background-color:#283b4c;
    }}
    @media all and (max-width:30em){{
        .button1{{
            display:block;
            margin:0.8em auto;
            }}
    }}
                .bouncy{{
                    animation: bouncy 10s infinite;
                    position:relative;
                    }}
                @keyframes bouncy {{
                    0%{{top:0em}}
                    20%{{top:0em}}
                    23%{{top:-0.4em}}
                    26%{{top:0em}}
                    28%{{top:-0.2em}}
                    30%{{top:0em}}
                    50%{{top:0em;}}
                }}
                input {{
                width: fit-content;
                text-align: center;
                font-family: sans-serif;
                font-weight: 600;
                margin-top: 100px;
                color:#296965;
                background-color: #f6f5d7;
                border: none;
                border-bottom:1px solid;
                border-color:#296965 ;
                outline: none;
                box-shadow: none;
                opacity: 0.8;
            }}
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

                              <div class="label">{13}</div>

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
                <div class="container">
                        <a href="/genre/{0}" class="button1 bouncy" style="color:#375737;">{0}</a>
                        <a href="/genre/{1}" class="button1 bouncy" style="animation-delay:0.3s;color:#375754">{1}</a>
                        <a href="/genre/{2}" class="button1 bouncy" style="animation-delay:2.4s">{2}</a>
                        <a href="/genre/{3}" class="button1 bouncy" style="color:#535948;animation-delay:1s">{3}</a>
                        <a href="/genre/{4}" class="button1 bouncy" style="animation-delay:1.2s;color:#375754">{4}</a>
                        <a href="/genre/{5}" class="button1 bouncy" style="animation-delay:1.3s">{5}</a>
                        <a href="/genre/{6}" class="button1 bouncy" style="animation-delay:0.4s">{6}</a>
                        <a href="/genre/{7}" class="button1 bouncy" style="animation-delay:1.8s;color:#535948">{7}</a>
                        <a href="/genre/{8}" class="button1 bouncy" style="color:#375737;animation-delay:2s">{8}</a>
                        <a href="/genre/{9}" class="button1 bouncy" style="animation-delay:0.9s">{9}</a>
                        <a href="/genre/{10}" class="button1 bouncy" style="animation-delay:2.1s;color:#535948">{10}</a>
                        <a href="/genre/{11}" class="button1 bouncy" style="animation-delay:2.7s">{11}</a>
                    </div>
                    <form style="text-align: center;"">
                        <input type="text" name="genre" class="input" style="display:inline-block" placeholder="{14}">
                    </form>
               </body>
            </html>
       """.format(genres[0], genres[1], genres[2], genres[3],
                  genres[4], genres[5], genres[6], genres[7], genres[8],
                  genres[9], genres[10], genres[11], background, message, query)
    return html_string


def get_website(genre=None):
    album_arts = []
    album_names = []
    artist_names = []
    album_links = []

    albums = get_albums(genre)
    if albums == 'NOPE':
        html_string = get_genre_html(True, genre)
        return html_string
    for album in albums:
        album_arts.append(album['album_art'])
        album_names.append(album['album_name'])
        artist_names.append(album['artist_name'])
        album_links.append(album['album_link'])

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

    return html_string


