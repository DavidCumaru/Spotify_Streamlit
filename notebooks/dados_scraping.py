import streamlit as st 
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import credencial as creds
import os

if not os.path.exists('../data'):
    os.makedirs('../data')

client_credentials_manager = SpotifyClientCredentials(client_id=creds.client_id, client_secret=creds.client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


playlist_ids = [
    '5PTle1rPTwJHvyuJiky9XQ',
    '3zHikRjMYsFLhz5KvgD6WS',
    '2NkSAzNx0jU23xaeap1HGv',
]

def format_duration(ms):
    
    seconds = ms // 1000
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes}:{seconds:02d}"

def get_artist_genres(artist_name):

    results = sp.search(q=artist_name, type='artist', limit=1)
    if results['artists']['items']:
        artist = results['artists']['items'][0]
        return artist['genres']
    else:
        return []

def get_all_tracks(playlist_id):
    
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']
    track_data = []
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    for item in tracks:
        track = item['track']
        artist_names = ", ".join([artist['name'] for artist in track['artists']])
        genres = []
        for artist in track['artists']:
            artist_genres = get_artist_genres(artist['name'])
            genres.extend(artist_genres)
        genres = ", ".join(set(genres))

        track_data.append({
            'Nome': track['name'],
            'Artista': artist_names,
            'Álbum': track['album']['name'],
            'Duração': format_duration(track['duration_ms']),
            'Popularidade': track['popularity'],
            'Gêneros': genres
        })

    return pd.DataFrame(track_data)
all_tracks = pd.DataFrame()
for playlist_id in playlist_ids:
    df_tracks = get_all_tracks(playlist_id)
    all_tracks = pd.concat([all_tracks, df_tracks], ignore_index=True)
all_tracks.to_csv('../data/playlist_dados.csv', index=False)
st.title("Dados extraídos e salvos em 'data/playlist_dados.csv'")