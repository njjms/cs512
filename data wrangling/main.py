from lyrics_scraper import get_song_info, get_songs

import pandas as pd
import requests
import time
import re
from bs4 import BeautifulSoup

url = 'https://www.azlyrics.com/b/blink.html'

songinfo = get_songs(url)

blink = []

for song in songinfo:
    print("Working on: {}".format(song['title']))
    song_output = get_song_info(song['url'])
    blink.append(song_output)
    time.sleep(10)

song_info = pd.DataFrame(songinfo)
song_lyrics = pd.DataFrame(blink)

blink_songs = pd.merge(left = song_info, 
                       right = song_lyrics, 
                       left_on = 'url',
                       right_on = 'url')

blink_songs = blink_songs.drop_duplicates()

blink_songs.to_csv(r'blink_songs.csv',
                  index = None,
                  header = True)

blink_songs.to_json(r'blink_songs.json')

