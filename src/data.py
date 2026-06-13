"""Carga y limpieza del dataset de Spotify."""
import pandas as pd

from .config import load_config, path


def load_raw(cfg: dict | None = None) -> pd.DataFrame:
    cfg = cfg or load_config()
    return pd.read_csv(path(cfg["data"]["raw_csv"]))


def clean(df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    """Deja una fila por canción.

    El CSV trae una columna índice ('Unnamed: 0') y la misma canción aparece en varios géneros
    (~24k duplicados por track_id). Para el clustering analizamos a nivel canción, así que
    deduplicamos por track_id. También quitamos la fila con nombre nulo. Devuelvo cuántos
    duplicados quité para poder reportarlo.
    """
    df = df.drop(columns=[c for c in df.columns if c.startswith("Unnamed")], errors="ignore")
    df = df.dropna(subset=["track_name", "artists"])
    antes = len(df)
    songs = df.drop_duplicates("track_id").reset_index(drop=True)
    return songs, antes - len(songs)
