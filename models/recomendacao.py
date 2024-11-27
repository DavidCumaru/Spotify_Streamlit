from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd

app = FastAPI(
    title="API de Recomendação de Músicas",
    description="Recomenda músicas com base no dataset fornecido."
)

df = pd.read_csv('../data/playlist_dados.csv')

class GostoMusical(BaseModel):
    preferencias: str

def recomendar_musicas(preferencias, n_recomendacoes=5):
    try:
        filtro_musica = df[df["Nome"].str.contains(preferencias, case=False, na=False)]
        if not filtro_musica.empty:
            artista = filtro_musica.iloc[0]["Artista"]
            album = filtro_musica.iloc[0]["Álbum"]
            recomendacoes = df[(df["Artista"] == artista) | (df["Álbum"] == album)]
            recomendacoes = recomendacoes.drop_duplicates(subset=["Nome"])
            return recomendacoes.sample(min(len(recomendacoes), n_recomendacoes)).to_dict(orient="records")
        
        filtro_artista = df[df["Artista"].str.contains(preferencias, case=False, na=False)]
        if not filtro_artista.empty:
            recomendacoes = df[df["Artista"] == filtro_artista.iloc[0]["Artista"]]
            recomendacoes = recomendacoes.drop_duplicates(subset=["Nome"])
            return recomendacoes.sample(min(len(recomendacoes), n_recomendacoes)).to_dict(orient="records")
        
        filtro_album = df[df["Álbum"].str.contains(preferencias, case=False, na=False)]
        if not filtro_album.empty:
            album = filtro_album.iloc[0]["Álbum"]
            artista = filtro_album.iloc[0]["Artista"]
            recomendacoes = df[(df["Álbum"] == album) | (df["Artista"] == artista)]
            recomendacoes = recomendacoes.drop_duplicates(subset=["Nome"])
            return recomendacoes.sample(min(len(recomendacoes), n_recomendacoes)).to_dict(orient="records")
        return []
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao recomendar músicas: {str(e)}")

@app.post("/processar_texto", summary="Recomendar músicas")
async def recomendar(gosto: GostoMusical):
    recomendacoes = recomendar_musicas(gosto.preferencias)
    if not recomendacoes:
        raise HTTPException(status_code=404, detail="Nenhuma música encontrada com base nas preferências fornecidas.")
    return {"recomendacoes": recomendacoes}
