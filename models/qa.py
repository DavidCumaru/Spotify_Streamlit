import streamlit as st
from transformers import pipeline
import pandas as pd

qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

dados = pd.read_csv('../data/playlist_dados.csv')

st.title("Assistente de Playlist")
st.write("Faça perguntas sobre a playlist!")

pergunta = st.text_input("Digite sua pergunta sobre a playlist:")

def buscar_maior_popularidade():
    musica_popular = dados.loc[dados['Popularidade'].idxmax()]
    return f"A música mais popular é '{musica_popular['Nome']}' do artista {musica_popular['Artista']} com popularidade {musica_popular['Popularidade']}."

def buscar_musicas_artista(artista):
    artista_dados = dados[dados['Artista'].str.contains(artista, case=False, na=False)]
    if not artista_dados.empty:
        return f"O artista {artista} tem {artista_dados.shape[0]} músicas na playlist."
    else:
        return f"O artista {artista} não está na playlist."

if pergunta:
    if "mais popularidade" in pergunta.lower() or "qual música tem mais popularidade" in pergunta.lower():
        resposta = buscar_maior_popularidade()
    elif "quantas musicas" in pergunta.lower() and "artista" in pergunta.lower():
        artista = pergunta.lower().split("artista")[-1].strip()
        resposta = buscar_musicas_artista(artista)
    else:
        resposta = qa_pipeline({
            'context': dados.to_string(),
            'question': pergunta
        })['answer']
    st.write("Resposta:", resposta)