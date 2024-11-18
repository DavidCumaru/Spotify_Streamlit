import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import credencial as creds
import os

# Autenticação com a API do Spotify
client_credentials_manager = SpotifyClientCredentials(client_id=creds.client_id, client_secret=creds.client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Lista de playlists para adicionar ao dataset
playlist_ids = [
    '5PTle1rPTwJHvyuJiky9XQ',
    '37i9dQZEVXbMDoHDwVN2tF',
]

def format_duration(ms):
    """Converte a duração de milissegundos para minutos e segundos."""
    seconds = ms // 1000
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes}:{seconds:02d}"

def get_all_tracks(playlist_id):
    """Extrai todas as faixas de uma playlist do Spotify."""
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

# Coleta de dados de todas as playlists
all_tracks = pd.DataFrame()
for playlist_id in playlist_ids:
    df_tracks = get_all_tracks(playlist_id)
    all_tracks = pd.concat([all_tracks, df_tracks], ignore_index=True)

# Salva os dados no CSV
all_tracks.to_csv('../data/playlist_dados.csv', index=False)
st.title("Dados extraídos e salvos em 'data/playlist_dados.csv'")