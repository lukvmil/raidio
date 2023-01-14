import pyaudio
import wave
import openai
import uberduck
import spotipy
from spotipy import oauth2
from dotenv import load_dotenv
from os import getenv

load_dotenv()

uberduck_key = getenv('UBERDUCK_API_PUB')
uberduck_secret = getenv('UBERDUCK_API_PK')

openai.api_key = getenv('OPENAI_API_PK')
uberduck_client = uberduck.UberDuck(uberduck_key, uberduck_secret)

spotify_id = getenv('SPOTIFY_CLIENT_ID')
spotify_secret = getenv('SPOTIFY_CLIENT_SECRET')
spotify_redirect = 'http://127.0.0.1:5000/'
scopes = [
    'user-read-playback-state',
    'user-modify-playback-state',
    'user-read-currently-playing'
]

sp_oauth = oauth2.SpotifyOAuth(spotify_id, spotify_secret, spotify_redirect, scope=scopes)

token_info = sp_oauth.get_cached_token()
access_token = token_info['access_token']
spotify = spotipy.Spotify(access_token)

def play_temp_file():
    chunk = 1024
    p = pyaudio.PyAudio()

    f = wave.open("temp.wav")

    stream = p.open(
        format = p.get_format_from_width(f.getsampwidth()),
        channels = f.getnchannels(),
        rate = f.getframerate(),
        output = True
        )

    data = f.readframes(chunk)

    while data:
        stream.write(data)
        data = f.readframes(chunk)

    stream.stop_stream()
    stream.close()

    p.terminate()

def generate_text(prompt):
    completion = openai.Completion.create(
        engine='text-davinci-003',
        temperature=0.8,
        frequency_penalty=0.5,
        max_tokens=400,
        prompt=prompt)

    resp = completion.choices[0].text

    return resp

def generate_voice(text, voice='dj-professor-k'):
    uberduck_client.speak(text, voice, file_path="temp.wav")

def format_song(title, artist):
    return f'"{title}" by {artist}'

def process_song(song):
    title = song['name']
    artist = song['artists'][0]['name']
    return format_song(title, artist)

def song_time_remaining():
    data = spotify.current_playback()
    progress = data['progress_ms']
    duration = data['item']['duration_ms']
    return (duration - progress) / 1000

def get_next_song():
    return process_song(spotify.queue()['queue'][0])

def is_playing():
    return spotify.current_playback()['is_playing']

def pause():
    if is_playing(): spotify.pause_playback()

def resume():
    if not is_playing(): spotify.start_playback()