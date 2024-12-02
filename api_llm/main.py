import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import torch
from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

class Song(BaseModel):
    Nome: str
    Artista: str
    Álbum: str
    Duração: str
    Popularidade: int
    Gêneros: List[str]

user_memories = {}

file_path = '../data/playlist_dados.csv'
df = pd.read_csv(file_path, quotechar='"')

songs_data = []
for _, row in df.iterrows():
    genres = row["Gêneros"]
    genres = genres.split(", ") if isinstance(genres, str) else []
    song = {
        "Nome": row["Nome"],
        "Artista": row["Artista"],
        "Álbum": row["Álbum"],
        "Duração": row["Duração"],
        "Popularidade": int(row["Popularidade"]),
        "Gêneros": genres,
    }
    songs_data.append(song)

def generate_embedding(text: str):
    inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze()

def recommend_songs(query: str):
    query_embedding = generate_embedding(query)
    
    song_embeddings = [generate_embedding(song["Nome"] + " " + song["Artista"]) for song in songs_data]
    similarities = [cosine_similarity(query_embedding.reshape(1, -1), song_embedding.reshape(1, -1))[0][0] for song_embedding in song_embeddings]
    
    recommended_songs = sorted(zip(songs_data, similarities), key=lambda x: x[1], reverse=True)
    
    return [song for song, _ in recommended_songs[:5]]

app = FastAPI()

@app.get("/songs", response_model=List[Song])
async def search_songs(
    artist: Optional[str] = None,
    genre: Optional[str] = None,
    popularity: Optional[int] = None,
):
    results = songs_data
    if artist:
        results = [song for song in results if artist.lower() in song["Artista"].lower()]
    if genre:
        results = [song for song in results if any(genre.lower() in g.lower() for g in song["Gêneros"])]
    if popularity is not None:
        results = [song for song in results if song["Popularidade"] >= popularity]
    user_memories["search_history"] = user_memories.get("search_history", []) + [{"artist": artist, "genre": genre, "popularity": popularity}]
    
    return results

@app.post("/add_songs", response_model=Song)
async def add_song(song: Song):
    new_song = song.dict()
    songs_data.append(new_song)
    df = pd.DataFrame(songs_data)
    df.to_csv(file_path, index=False, quotechar='"', sep=',', encoding='utf-8')
    return new_song

@app.get("/recommendations/{query}", response_model=List[Song])
async def get_recommendations(query: str):
    # Adicionar consulta à memória (se necessário)
    user_memories["search_history"] = user_memories.get("search_history", []) + [{"query": query}]
    
    recommended_songs = recommend_songs(query)
    return recommended_songs

@app.get("/memory")
async def get_memory():
    return user_memories
