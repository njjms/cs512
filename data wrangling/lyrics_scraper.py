#!/usr/bin/env python

import pandas as pd
import requests
import time
import re
from bs4 import BeautifulSoup

def get_songs(url):
    """
    Function to get list of songs and corresponding URLs under an artist page
    Input: url to an artist's page on azlyrics.com
    Output: Returns a list of dicts ({'title' : [TITLE], 'url' : [URL]})
    """
    songlist = requests.get(url)
    soup = BeautifulSoup(songlist.text)

    songinfo = []

    for row in soup.findAll('div', attrs = {'class' : 'listalbum-item'}):
        song = {}
        song['title'] = row.a.text
        song['url'] = row.a['href'].replace("..", "https://www.azlyrics.com")
        songinfo.append(song)

    return(songinfo)

def get_song_info(url):
    """
    Function to get lyrics, album, and year information for individual song
    Input: url to a song's page on azlyrics.com
    Output: Dict ({'lyrics' : [string LYRICS],
                   'url' : [string URL],
                   'album_name' : [string ALBUM_NAME],
                   'year': [int YEAR]})
    """
    tmp = requests.get(url)
    tmpsoup = BeautifulSoup(tmp.text)
    
    try:
        tmpalbum = tmpsoup.find('div', attrs = {'class' : 'songinalbum_title'}).text.replace("album: ", "")
        albumpattern = r'"([A-Za-z0-9]*)"'
        album_name = re.search(albumpattern, tmpalbum).group(0).replace('\"', '')
    
        yearpattern = r'\([0-9]*\)'
        album_year = re.search(yearpattern, tmpalbum).group(0).replace('(', '').replace(')', '')
    except:
        album_name = "None"
        album_year = 0
    
    try:
        tmplyrics = tmpsoup.select('body > div.container.main-page > div > div.col-xs-12.col-lg-8.text-center > div:nth-child(8)')[0].text
        lyrics = tmplyrics.replace('\n', ' ').replace('\r', ' ').strip()
    except:
        tmplyrics = tmpsoup.select('body > div.container.main-page > div > div.col-xs-12.col-lg-8.text-center > div:nth-child(10)')[0].text
        lyrics = tmplyrics.replace('\n', ' ').replace('\r', ' ').strip()
    
    output = {}
    output['lyrics'] = lyrics
    output['album_name'] = album_name
    output['year'] = album_year
    output['url'] = url
    
    return(output)

def json_to_csv(json_file):
    '''
    Converts json to csv files.

    Args:
        json_file (str) : PATH to json file

    Returns:
        .csv file in current working directory
    '''
        
    try:
        df = pd.read_json(json_file)
        output = df.to_csv(encoding='utf-8', 
                           index=False)
        return(output)
    except:
        print("Error in converting to json")

