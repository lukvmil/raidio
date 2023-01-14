import json
from utils import generate_text

with open('prompts.json', 'r') as f:
    prompts = json.load(f)

print(prompts)

def welcome(song):
    print(f'Generating welcome and intro for {song}...')
    text = generate_text(
        prompts['background'] + prompts['introduction'].format(song)
    )
    print(text)
    return text

def reminder(prev_song, next_song):
    print(f'Generating reminder for {prev_song} and intro for {next_song}...')
    text = generate_text(
        prompts['background'] + prompts['reminder'].format(prev_song, next_song)
    )
    print(text)
    return text

def story(prev_song):
    print(f'Generating story for {prev_song}...')
    text = generate_text(
        prompts['background'] + prompts['story'].format(prev_song)
    )
    print(text)
    return text

