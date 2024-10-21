import streamlit as st
import pandas as pd
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os

def run_page():
    @st.cache_data
    def load_data():
        data_path = '../data/playlist_dados.csv'
        if os.path.exists(data_path):
            df = pd.read_csv(data_path)
            return df
        else:
            st.error("Arquivo de dados não encontrado.")
            return pd.DataFrame()
    df_tracks = load_data()

    if not df_tracks.empty:
        st.title("Informações da Playlist")
        st.subheader("Tabela de Músicas")
        st.dataframe(df_tracks)
        st.subheader("Estatísticas")
        st.write(f"Número total de músicas: {df_tracks.shape[0]}")
        st.write(f"Média de popularidade: {df_tracks['Popularidade'].mean():.2f}")
        st.subheader("Nuvem de Palavras dos Artistas")
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(" ".join(df_tracks['Artista']))
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        st.pyplot(plt)
    st.subheader("Upload de Arquivo CSV")

    uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="csv")

    if uploaded_file is not None:
        new_data = pd.read_csv(uploaded_file)
        
        if 'Nome' in new_data.columns and 'Artista' in new_data.columns:
            df_tracks = pd.concat([df_tracks, new_data], ignore_index=True)
            st.success("Dados adicionados com sucesso!")
        else:
            st.error("O arquivo deve conter as colunas 'Nome' e 'Artista'.")
    if not df_tracks.empty:
        st.subheader("Download dos Dados Atualizados")
        csv = df_tracks.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV", csv, "playlist_atualizada.csv", "text/csv")