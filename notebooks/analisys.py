import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns
def run_page():
    API_URL = "http://127.0.0.1:8000/songs"

    st.title("Análise de Dados das Músicas 🎵📊")

    @st.cache_data
    def load_data():
        response = requests.get(API_URL)
        if response.status_code == 200:
            return pd.DataFrame(response.json())
        else:
            st.error("Erro ao carregar dados da API.")
            return pd.DataFrame()
    data = load_data()
    if not data.empty:
        st.subheader("Tabela de Dados")
        st.dataframe(data)
        st.sidebar.title("Opções de Análise")
        analysis_type = st.sidebar.selectbox(
            "Escolha a análise:",
            [
                "Popularidade Média por Gênero",
                "Duração Média por Artista",
                "Distribuição de Popularidade",
                "Músicas por Gênero"
            ]
        )
        if analysis_type == "Popularidade Média por Gênero":
            st.subheader("Popularidade Média por Gênero")
            genre_popularity = (
                data.explode("Gêneros")
                .groupby("Gêneros")["Popularidade"]
                .mean()
                .sort_values(ascending=False)
            )
            st.bar_chart(genre_popularity)
            st.write(genre_popularity)
        elif analysis_type == "Duração Média por Artista":
            st.subheader("Duração Média por Artista")
            def duration_to_seconds(duration):
                try:
                    minutes, seconds = map(int, duration.split(":"))
                    return minutes * 60 + seconds
                except ValueError:
                    return 0
            data["Duração (s)"] = data["Duração"].apply(duration_to_seconds)
            artist_duration = (
                data.groupby("Artista")["Duração (s)"]
                .mean()
                .sort_values(ascending=False)
                .head(10)
            )
            st.bar_chart(artist_duration)
            st.write(artist_duration)
        elif analysis_type == "Distribuição de Popularidade":
            st.subheader("Distribuição de Popularidade")
            fig, ax = plt.subplots()
            sns.histplot(data["Popularidade"], bins=10, kde=True, ax=ax, color="blue")
            ax.set_title("Distribuição de Popularidade")
            ax.set_xlabel("Popularidade")
            ax.set_ylabel("Frequência")
            st.pyplot(fig)
        elif analysis_type == "Músicas por Gênero":
            st.subheader("Músicas por Gênero")
            genre_count = data.explode("Gêneros")["Gêneros"].value_counts()
            fig, ax = plt.subplots()
            genre_count.plot(kind="bar", ax=ax, color="orange")
            ax.set_title("Quantidade de Músicas por Gênero")
            ax.set_xlabel("Gênero")
            ax.set_ylabel("Quantidade")
            st.pyplot(fig)
            st.write(genre_count)
    else:
        st.warning("Nenhum dado disponível para análise.")
