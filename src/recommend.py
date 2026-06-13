"""Recomendador de canciones similares por 'vibe' de audio.

Idea: dos canciones son parecidas si están cerca en el espacio de features de audio (las mismas
que usamos para clustering). Dada una canción, devolvemos sus vecinas más cercanas. Reutiliza el
scaler y el modelo de clustering ya entrenados (`src/cluster_model.pkl`), así no recalcula nada.

Uso por terminal:  python -m src.recommend "Blinding Lights"
"""
import pickle

import numpy as np
from sklearn.neighbors import NearestNeighbors

from . import data, features
from .config import load_config, path


class Recommender:
    def __init__(self, cfg: dict | None = None):
        self.cfg = cfg or load_config()
        art = pickle.load(open(path(self.cfg["data"]["model"]), "rb"))
        self.scaler, self.km, self.names = art["scaler"], art["kmeans"], art["names"]

        songs, _ = data.clean(data.load_raw(self.cfg))
        X, _ = features.scale(songs, self.cfg, scaler=self.scaler)   # reusa el scaler entrenado
        self.songs = songs.reset_index(drop=True)
        self.songs["cluster"] = self.km.predict(X)
        self.X = X
        self.nn = NearestNeighbors(metric="euclidean").fit(X)
        self._by_id = {tid: i for i, tid in enumerate(self.songs["track_id"])}

    def _resolve(self, query: str) -> int:
        """Acepta un track_id o un nombre de canción (exacto, o por coincidencia parcial)."""
        if query in self._by_id:
            return self._by_id[query]
        nombre = self.songs["track_name"].str.lower()
        exacto = self.songs[nombre == str(query).lower()]
        if len(exacto):
            return int(exacto.index[0])
        parcial = self.songs[nombre.str.contains(str(query).lower(), na=False, regex=False)]
        if len(parcial):
            return int(parcial.index[0])
        raise ValueError(f"No encontré ninguna canción que coincida con '{query}'.")

    def similar(self, query: str, n: int = 10) -> dict:
        i = self._resolve(query)
        # pedimos n+1 porque el más cercano siempre es la propia canción.
        dist, idx = self.nn.kneighbors(self.X[i:i + 1], n_neighbors=n + 1)
        recs = []
        for d, j in zip(dist[0], idx[0]):
            if j == i:
                continue
            row = self.songs.iloc[j]
            recs.append({
                "track_name": row["track_name"], "artists": row["artists"],
                "track_genre": row["track_genre"], "cluster": int(row["cluster"]),
                "cluster_name": self.names[int(row["cluster"])], "distance": round(float(d), 3),
            })
            if len(recs) >= n:
                break
        s = self.songs.iloc[i]
        return {
            "seed": {"track_name": s["track_name"], "artists": s["artists"],
                     "cluster": int(s["cluster"]), "cluster_name": self.names[int(s["cluster"])]},
            "similar": recs,
        }


def _main():
    import sys
    # Los títulos de Spotify traen acentos y alfabetos no latinos; en consolas Windows (cp1252)
    # eso rompe el print. Forzamos UTF-8 para que el CLI no falle con nombres en otros idiomas.
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    query = " ".join(sys.argv[1:]) or "Blinding Lights"
    rec = Recommender()
    out = rec.similar(query, 10)
    s = out["seed"]
    print(f"Semilla: {s['track_name']} - {s['artists']}  [{s['cluster_name']}]\n")
    print("Similares:")
    for r in out["similar"]:
        print(f"  {r['track_name'][:40]:<40} {r['artists'][:25]:<25} "
              f"({r['track_genre']}, d={r['distance']})")


if __name__ == "__main__":
    _main()
