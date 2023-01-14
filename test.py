from flask import Flask, request
import spotipy
from spotipy import oauth2
from dotenv import load_dotenv
from os import getenv

load_dotenv()

spotify_id = getenv('SPOTIFY_CLIENT_ID')
spotify_secret = getenv('SPOTIFY_CLIENT_SECRET')
spotify_redirect = 'http://127.0.0.1:5000/callback'
scopes = [
    'user-read-playback-state',
    'user-modify-playback-state',
    'user-read-currently-playing'

]
cache = '.spotipyoauthcache'

app = Flask('raidio')

sp_oauth = oauth2.SpotifyOAuth(spotify_id, spotify_secret, spotify_redirect, scope=scopes)

@app.route('/')
def hello_world():
    return 'hello world'

@app.route('/callback')
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
        queue = sp.queue()
        print(queue)
        with open('token.txt', 'w+') as f:
            f.write(access_token)
        return results

    else:
        return htmlForLoginButton()

def htmlForLoginButton():
    auth_url = getSPOauthURI()
    htmlLoginButton = "<a href='" + auth_url + "'>Login to Spotify</a>"
    return htmlLoginButton

def getSPOauthURI():
    auth_url = sp_oauth.get_authorize_url()
    return auth_url

app.run()