import streamlit as st
import importlib

st.set_page_config(page_title="Navegação de Páginas", layout="wide")

st.title("Aplicação com Múltiplas Páginas")

st.sidebar.title("Menu de Navegação")
page = st.sidebar.selectbox("Escolha a página", ("Página 1", "Página 2"))

if page == "Página 1":
    top50 = importlib.import_module('top50')
    top50.run_page()
elif page == "Página 2":
    analise = importlib.import_module('analise')
    analise.run_page()