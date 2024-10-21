import streamlit as st
import importlib

st.set_page_config(page_title="Navegação de Páginas", layout="wide")

st.title("Aplicação com Múltiplas Páginas")

st.sidebar.title("Menu de Navegação")
page = st.sidebar.selectbox("Escolha a página", ("Página 1", "Página 2"))

if page == "Página 1":
    my_app = importlib.import_module('my_app')
    my_app.run_page()
elif page == "Página 2":
    mys_app = importlib.import_module('parte2')
    mys_app.run_page()