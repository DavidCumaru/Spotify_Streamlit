import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/processar_texto"

st.title("Recomendação de musicas Streamlit com FastAPI")

preferencias = st.text_input("Digite sua musica, banda ou cantor:")

if st.button("Recomendar"):
    if preferencias:
        try:
            st.write(f"Recomendações para pesquisa: {preferencias}")
            response = requests.post(API_URL, json={"preferencias": preferencias})          
            if response.status_code == 200:
                data = response.json()
                recomendacoes = data.get("recomendacoes", [])              
                if recomendacoes:
                    st.subheader("Recomendações de Músicas:")
                    for musica in recomendacoes:
                        st.write(
                            f"🎵 **Nome:** {musica['Nome']}\n"
                            f"👤 **Artista:** {musica['Artista']}\n"
                            f"💿 **Álbum:** {musica['Álbum']}\n"
                            f"⏱️ **Duração:** {musica['Duração']}\n"
                            f"⭐ **Popularidade:** {musica['Popularidade']}\n"
                        )
                else:
                    st.write("Nenhuma recomendação encontrada para as suas preferências.")
            else:
                st.write(f"Erro: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"Erro ao se conectar com a API: {e}")
    else:
        st.warning("Por favor, insira suas preferências para recomendação.")
