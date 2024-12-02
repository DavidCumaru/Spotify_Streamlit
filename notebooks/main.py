import streamlit as st
import importlib

st.set_page_config(page_title="Navegação de Páginas", layout="wide")
st.sidebar.title("Menu de Navegação")
page = st.sidebar.selectbox("Escolha a página", ("Página 1", "Página 2", "Página 3"))

if page == "Página 1":
    top50 = importlib.import_module('search_and_add')
    top50.run_page()
elif page == "Página 2":
    analise = importlib.import_module('analisys')
    analise.run_page()
elif page == "Página 3":
    analise = importlib.import_module('rec')
    analise.run_page()
