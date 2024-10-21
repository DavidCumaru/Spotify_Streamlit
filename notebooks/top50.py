import streamlit as st
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import credencial as creds

def run_page():
    st.title("Página 1 - my_app.py")
    st.write("Conteúdo da Página 1.")

    client_credentials_manager = SpotifyClientCredentials(client_id=creds.client_id, client_secret=creds.client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    def get_all_tracks():
        playlist_id = "37i9dQZEVXbMDoHDwVN2tF"
        results = sp.playlist_tracks(playlist_id, limit=100)
        tracks = results['items']
        while results['next']:
            results = sp.next(results)
            tracks.extend(results['items'])

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
    ### Links utilizados
    - [Documentação da API do Spotify](https://developer.spotify.com/documentation/web-api)
    - [Aplicação Top Songs](https://top-songs.streamlit.app)
    """)

    df_tracks = get_all_tracks()

    artist_filter = st.text_input("Filtrar por nome do artista")

    if artist_filter:
        df_filtered = df_tracks[df_tracks['Artista'].str.contains(artist_filter, case=False)]
        st.markdown(f"### Resultados filtrados para: {artist_filter}")
        st.dataframe(df_filtered)
    else:
        st.markdown("### Top 50 músicas populares")
        st.dataframe(df_tracks)