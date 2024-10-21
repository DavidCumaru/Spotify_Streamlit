import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import credencial as creds
import os

client_id = st.secrets["general"]["SPOTIFY_CLIENT_ID"]
client_secret = st.secrets["general"]["SPOTIFY_CLIENT_SECRET"]

# Configure o cliente do Spotify
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = Spotify(client_credentials_manager=client_credentials_manager)

playlist_id = '5PTle1rPTwJHvyuJiky9XQ'

def format_duration(ms):
    seconds = ms // 1000
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes}:{seconds:02d}"

def get_all_tracks(playlist_id):
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']
    track_data = []
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    for item in tracks:
        track = item['track']
        track_data.append({
            'Nome': track['name'],
            'Artista': ", ".join([artist['name'] for artist in track['artists']]),
            'Álbum': track['album']['name'],
            'Duração': format_duration(track['duration_ms']),
            'Popularidade': track['popularity']
        })

    return pd.DataFrame(track_data)

df_tracks = get_all_tracks(playlist_id)
df_tracks.to_csv('../data/playlist_dados.csv', index=False)
print("Dados extraídos e salvos em 'data/playlist_dados.csv'")