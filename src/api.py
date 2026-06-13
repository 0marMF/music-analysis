"""API de recomendación de canciones similares (FastAPI).

Levantar en local:  uvicorn src.api:app --reload
Docs interactivas en  http://localhost:8000/docs

Expone el recomendador como servicio: le pasas una canción y devuelve N parecidas por sonido.
El recomendador se construye una sola vez (carga el dataset + modelo y arma el índice de vecinos).
"""
from fastapi import FastAPI, HTTPException, Query

from .recommend import Recommender

app = FastAPI(
    title="Music Similarity API",
    version="1.1.0",
    description="Recomendador de canciones similares por features de audio (K-Means + vecinos).",
)

_rec: Recommender | None = None


def _recommender() -> Recommender:
    global _rec
    if _rec is None:
        _rec = Recommender()        # carga perezosa: dataset + modelo + índice
    return _rec


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/similar")
def similar(track: str = Query(..., description="Nombre o track_id de la canción semilla"),
            n: int = Query(10, ge=1, le=50, description="Cuántas similares devolver")) -> dict:
    try:
        return _recommender().similar(track, n)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
