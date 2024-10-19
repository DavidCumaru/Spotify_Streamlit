import requests
from bs4 import BeautifulSoup

# URL do artista no Spotify
url = "https://open.spotify.com/artist/1uNFoZAHBGtllmzznpCI3s"  # Substitua pelo URL desejado

# Fazer a requisição
response = requests.get(url)

# Verificar se a requisição foi bem-sucedida
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')

    # Exemplo: Obter o nome do artista
    artist_name = soup.find('h1').text.strip()
    print(f"Nome do Artista: {artist_name}")

    # Exemplo: Obter o número de seguidores
    followers = soup.find('div', class_='followers').text.strip()  # Altere a classe conforme necessário
    print(f"Número de Seguidores: {followers}")

else:
    print("Erro ao acessar a página:", response.status_code)