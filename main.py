import uberduck
import asyncio
import spotipy
from spotipy.oauth2 import SpotifyOAuth

from dotenv import load_dotenv
from os import getenv

load_dotenv()

uberduck_key = getenv('UBERDUCK_API_PUB')
uberduck_secret = getenv('UBERDUCK_API_PK')
spotify_id = getenv('SPOTIFY_CLIENT_ID')
spotify_secret = getenv('SPOTIFY_CLIENT_SECRET')
spotify_redirect = 'http://127.0.0.1:5000/callback'
scopes = [
    'user-read-playback-state',
    'user-modify-playback-state',
    'user-read-currently-playing'

]

# with open('token.txt', 'r') as f:
#     token = f.read()


#     sp = spotipy.Spotify(token)

#     print(sp.current_user_playing_track())


client = uberduck.UberDuck(uberduck_key, uberduck_secret)
voices = uberduck.get_voices(return_only_names=True)

text = """
Up next is "Dynamite" by BTS. This one is a bright and upbeat track with a feel-good vibe that will lift your spirits. It's a song about finding strength and self-confidence, and it's sure to put a smile on your face! So get ready to dance, because this one is going to be a banger!
"""

sound = client.speak(text, "simon-cowell")

import pdb; pdb.set_trace()