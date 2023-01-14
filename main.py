import time
import personality
import utils
from utils import spotify
from server import app
from threading import Thread
from pathlib import Path
import os
import random

try:
    os.remove('start_show')
except FileNotFoundError:
    pass

thread = Thread(target=app.run)
thread.start()

while not Path('start_show').is_file():
    time.sleep(1)

queue = spotify.queue()
first_song = utils.process_song(queue['currently_playing'])

text = personality.welcome(first_song)
utils.generate_voice(text)

utils.pause()
spotify.seek_track(0)
utils.play_temp_file()
utils.resume()

prev_song = first_song

while True:
    time_remaining = utils.song_time_remaining()
    # print(f'{time_remaining} seconds left in current song')

    if time_remaining < 20:
        next_song = utils.get_next_song()

        if random.randint(0, 3) == 0:
            text = personality.story(prev_song)
        else:
            text = personality.reminder(prev_song, next_song)

        prev_song = next_song
        utils.generate_voice(text)

        time_remaining = utils.song_time_remaining()
        time.sleep(time_remaining)

        utils.pause()
        utils.play_temp_file()
        utils.resume()

    time.sleep(5)