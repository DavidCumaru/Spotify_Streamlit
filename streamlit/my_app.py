# Rodar o Streamlit: No terminal, você deverá executar o comando:
# cd streamlit
# streamlit run my_app.py

import streamlit as st
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import credencial as creds

client_credentials_manager = SpotifyClientCredentials(client_id=creds.client_id, client_secret=creds.client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_top_tracks():
    results = sp.playlist_tracks("37i9dQZEVXbMDoHDwVN2tF", limit=50)
    tracks = results['items']
    track_data = []
    for item in tracks:
        track = item['track']
        track_data.append({
            'Nome': track['name'],
            'Artista': ", ".join([artist['name'] for artist in track['artists']]),
            'Álbum': track['album']['name'],
            'Popularidade': track['popularity'],
            'Duração (ms)': track['duration_ms']
        })
    return pd.DataFrame(track_data)

st.title("Análise e Recomendação de Músicas com API do Spotify")

st.markdown("""
### Descrição do Projeto
O objetivo deste projeto é utilizar a API do Spotify para realizar uma análise das músicas mais populares e criar um sistema de recomendação. Através da exploração de dados como gêneros, popularidade e características das músicas, buscamos fornecer insights úteis para profissionais da indústria musical e usuários que desejam descobrir novas músicas.
""")

st.markdown("""
### Links Úteis
- [Documentação da API do Spotify](https://developer.spotify.com/documentation/web-api)
- [Aplicação Top Songs](https://top-songs.streamlit.app)
""")

# Exibe diretamente os dados das 50 músicas mais populares globalmente
df_tracks = get_top_tracks()
st.markdown("### Top 50 músicas mais populares globalmente")
st.dataframe(df_tracks)