import spotipy
from multiprocessing import Process
from flask import Flask, request
from spotipy import oauth2
from dotenv import load_dotenv
from os import getenv

load_dotenv()

spotify_id = getenv('SPOTIFY_CLIENT_ID')
spotify_secret = getenv('SPOTIFY_CLIENT_SECRET')
spotify_redirect = 'http://127.0.0.1:5000/'
scopes = [
    'user-read-playback-state',
    'user-modify-playback-state',
    'user-read-currently-playing'
]

app = Flask('raidio')

sp_oauth = oauth2.SpotifyOAuth(spotify_id, spotify_secret, spotify_redirect, scope=scopes)

@app.route('/')
def callback():
    access_token = ""

    token_info = sp_oauth.get_cached_token()

    if token_info:
        print("Found cached token!")
        access_token = token_info['access_token']
    else:
        url = request.url
        code = sp_oauth.parse_response_code(url)
        if code != url:
            print("Found Spotify auth code in Request URL! Trying to get valid access token...")
            token_info = sp_oauth.get_access_token(code)
            access_token = token_info['access_token']

    if access_token:
        print("Access token available! Trying to get user information...")
        sp = spotipy.Spotify(access_token)
        results = sp.current_user()

        return f"Welcome {results['display_name']}, <a href='/start'>click here to start the show!</a>"

    else:
        return f"<a href='{sp_oauth.get_authorize_url()}'>Login to Spotify</a>"

@app.route('/start')
def start():
    with open('start_show', 'w') as f:
        pass

    return "The show has started! Feel free to close this window."