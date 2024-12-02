import streamlit as st
import requests

def run_page():
    API_URL = "http://127.0.0.1:8000"

    st.title("Recomendação de Músicas com BERT")
    if "search_history" not in st.session_state:
        st.session_state["search_history"] = []
    query = st.text_input("Descreva uma música ou artista:")
    if st.button("Buscar Recomendações"):
        if query:
            response = requests.get(f"{API_URL}/recommendations/{query}")
            if response.status_code == 200:
                recommended_songs = response.json()
                st.write("Músicas recomendadas:")
                for song in recommended_songs:
                    st.write(f"**{song['Nome']}** - {song['Artista']} ({song['Álbum']})")
                st.session_state["search_history"].append(
                    {
                        "query": query,
                        "results": recommended_songs,
                    }
                )
            else:
                st.error("Erro ao buscar recomendações.")
        else:
            st.warning("Por favor, insira uma descrição para buscar recomendações.")
    if st.session_state["search_history"]:
        st.write("### Histórico de Consultas:")
        for idx, history in enumerate(st.session_state["search_history"]):
            st.write(f"**Consulta {idx + 1}:** {history['query']}")
            st.write("**Resultados:**")
            for song in history["results"]:
                st.write(f"  - {song['Nome']} - {song['Artista']} ({song['Álbum']})")