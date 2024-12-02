import streamlit as st
import requests

def run_page():
    API_URL = "http://127.0.0.1:8000"

    st.title("Aplicativo de Músicas 🎵")
    st.sidebar.title("Navegação")
    option = st.sidebar.radio("Escolha uma opção", ["Buscar Músicas", "Adicionar Músicas"])

    if option == "Buscar Músicas":
        st.header("Buscar Músicas")
        artist = st.text_input("Artista (opcional)")
        genre = st.text_input("Gênero (opcional)")
        popularity = st.number_input("Popularidade mínima (opcional)", min_value=0, max_value=100, step=1, format="%d")

        if st.button("Buscar"):
            params = {}
            if artist:
                params["artist"] = artist
            if genre:
                params["genre"] = genre
            if popularity:
                params["popularity"] = popularity

            response = requests.get(f"{API_URL}/songs", params=params)

            if response.status_code == 200:
                songs = response.json()
                if songs:
                    st.success(f"Encontradas {len(songs)} músicas!")
                    for song in songs:
                        st.write(f"🎶 **{song['Nome']}** - {song['Artista']}")
                        st.write(f"Álbum: {song['Álbum']}, Popularidade: {song['Popularidade']}, Duração: {song['Duração']}")
                        st.write(f"Gêneros: {', '.join(song['Gêneros'])}")
                        st.write("---")
                else:
                    st.warning("Nenhuma música encontrada.")
            else:
                st.error("Erro ao buscar músicas. Verifique a API.")

    if option == "Adicionar Músicas":
        st.header("Adicionar Nova Música")

        nome = st.text_input("Nome da Música")
        artista = st.text_input("Artista")
        album = st.text_input("Álbum")
        duracao = st.text_input("Duração (Ex: 3:45)")
        popularidade = st.number_input("Popularidade (0 a 100)", min_value=0, max_value=100, step=1, format="%d")
        generos = st.text_area("Gêneros (separados por vírgula)")

        if st.button("Adicionar"):
            if nome and artista and album and duracao and popularidade is not None and generos:
                song_data = {
                    "Nome": nome,
                    "Artista": artista,
                    "Álbum": album,
                    "Duração": duracao,
                    "Popularidade": popularidade,
                    "Gêneros": [g.strip() for g in generos.split(",")]
                }

                response = requests.post(f"{API_URL}/add_songs", json=song_data)

                if response.status_code == 200:
                    st.success("Música adicionada com sucesso!")
                else:
                    st.error("Erro ao adicionar música. Verifique os dados e tente novamente.")
            else:
                st.warning("Por favor, preencha todos os campos.")
