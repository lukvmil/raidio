import uberduck
import asyncio
import spotify.sync as spotify

from dotenv import load_dotenv
from os import getenv

load_dotenv()

uberduck_key = getenv('UBERDUCK_API_PUB')
uberduck_secret = getenv('UBERDUCK_API_PK')

spotify_id = getenv('SPOTIFY_CLIENT_ID')
spotify_secret = getenv('SPOTIFY_CLIENT_SECRET')

# client = uberduck.UberDuck(uberduck_key, uberduck_secret)
# voices = uberduck.get_voices(return_only_names=True)

# text = """
# Up next is "Dynamite" by BTS. This one is a bright and upbeat track with a feel-good vibe that will lift your spirits. It's a song about finding strength and self-confidence, and it's sure to put a smile on your face! So get ready to dance, because this one is going to be a banger!
# """

# client.speak(text, "simon-cowell", play_sound=True)

client = spotify.Client(spotify_id, spotify_secret)

user = spotify.User.from_token(client, '')
import pdb; pdb.set_trace()
tracks = user.recently_played()
print(tracks)
