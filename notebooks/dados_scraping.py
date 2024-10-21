import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import credencial as creds
import os

# Autenticação na API do Spotify
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# ID da playlist que você deseja acessar
playlist_id = '5PTle1rPTwJHvyuJiky9XQ'

# Função para formatar duração
def format_duration(ms):
    seconds = ms // 1000
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes}:{seconds:02d}"

# Função para obter todas as músicas de uma playlist
def get_all_tracks(playlist_id):
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']

    # Lista para armazenar os dados das músicas
    track_data = []

    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])

    # Extraindo informações das faixas
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

# Obtém as faixas da playlist
df_tracks = get_all_tracks(playlist_id)

# Salva os dados em um arquivo CSV no diretório existente 'data'
df_tracks.to_csv('../data/playlist_dados.csv', index=False)

print("Dados extraídos e salvos em 'data/playlist_dados.csv'")