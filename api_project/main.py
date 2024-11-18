from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd

df = '../data/playlist_dados.csv'

def save_data(data):
    try:
        data.to_csv(df, index=False)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao salvar os dados: {str(e)}")

app = FastAPI(
    title="API de Gerenciamento de Playlist",
    description="Uma API simples para interagir com playlists de música."
)

class Song(BaseModel):
    title: str
    artist: str
    album: str

@app.get("/songs", summary="Obter todas as músicas", description="Retorna a lista de todas as músicas disponíveis.")
async def get_songs():
    data = df()
    return data.to_dict(orient="records")

@app.post("/songs", summary="Adicionar uma nova música", description="Adiciona uma nova música à playlist.")
async def add_song(song: Song):
    data = df()
    new_song = pd.DataFrame([song.dict()])
    updated_data = pd.concat([data, new_song], ignore_index=True)
    save_data(updated_data)
    return {"message": "Música adicionada com sucesso!", "song": song.dict()}