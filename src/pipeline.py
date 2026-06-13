"""Pipeline de clustering de punta a punta.

Correr con:  python -m src.pipeline

Carga el dataset, lo limpia, escala las features de audio, agrupa con K-Means y guarda el modelo
(scaler + KMeans + nombres de cluster), las métricas y una fila en el registro de experimentos.
Hace lo mismo que el notebook 03, pero de una vez y sin copy-paste.
"""
import csv
import json
from datetime import datetime

import numpy as np
from sklearn.metrics import silhouette_score

from . import cluster, data, features
from .config import load_config, path


def run(cfg: dict | None = None) -> dict:
    cfg = cfg or load_config()
    seed = cfg["seed"]
    audio = cfg["features"]["audio"]
    k = cfg["clustering"]["k"]

    # 1) Datos a nivel canción
    songs, n_dups = data.clean(data.load_raw(cfg))
    print(f"Canciones únicas: {len(songs):,} (quitados {n_dups:,} duplicados por track_id)")

    # 2) Escalar + agrupar
    X, scaler = features.scale(songs, cfg)
    km, labels = cluster.fit(X, k, seed)
    songs = songs.assign(cluster=labels)

    # 3) Silhouette (sobre muestra) y nombres interpretables
    rng = np.random.RandomState(seed)
    sample = rng.choice(len(X), min(cfg["clustering"]["silhouette_sample"], len(X)), replace=False)
    sil = float(silhouette_score(X[sample], labels[sample]))
    nombres = cluster.name_clusters(songs, labels, audio)
    print(f"K={k} | silhouette={sil:.3f}")
    for c in sorted(nombres):
        print(f"  cluster {c} ({int((labels == c).sum()):,}): {nombres[c]}")

    # 4) Guardar modelo + métricas + experimento
    _save_model(km, scaler, audio, nombres, k, cfg)
    _write_metrics(k, sil, songs, nombres, cfg)
    _log_experiment(k, sil, cfg)
    return {"k": k, "silhouette": sil, "names": nombres}


def _save_model(km, scaler, audio, nombres, k, cfg):
    import pickle
    artefacto = {"kmeans": km, "scaler": scaler, "audio": audio, "names": nombres, "k": k}
    with open(path(cfg["data"]["model"]), "wb") as f:
        pickle.dump(artefacto, f)


def _write_metrics(k, sil, songs, nombres, cfg):
    sizes = songs["cluster"].value_counts().to_dict()
    metrics = {
        "k": k, "silhouette": round(sil, 4), "n_songs": int(len(songs)),
        "clusters": [{"id": int(c), "name": nombres[int(c)], "size": int(sizes[c])}
                     for c in sorted(sizes)],
    }
    with open(path(cfg["paths"]["metrics"]), "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)


def _log_experiment(k, sil, cfg):
    fp = path(cfg["paths"]["experiments"])
    fila = {"timestamp": datetime.now().isoformat(timespec="seconds"),
            "k": k, "silhouette": round(sil, 4)}
    nuevo = not fp.exists()
    with open(fp, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(fila.keys()))
        if nuevo:
            w.writeheader()
        w.writerow(fila)


if __name__ == "__main__":
    run()
