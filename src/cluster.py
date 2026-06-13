"""Clustering de canciones por 'vibe' de audio (K-Means) y nombrado interpretable."""
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# Traducción de cada feature a un adjetivo, para nombrar los clusters como lo haría una persona.
_ADJ = {
    "danceability": "bailables", "energy": "enérgicas", "valence": "alegres",
    "tempo": "rápidas", "acousticness": "acústicas", "speechiness": "habladas",
    "instrumentalness": "instrumentales", "loudness": "potentes", "liveness": "en vivo",
}


def silhouette_curve(X, k_range, sample_size, seed):
    """Inercia (codo) y silhouette para cada K, para elegir el número de clusters.

    El silhouette se estima sobre una muestra porque es O(n^2) y aquí hay ~90k canciones.
    """
    rng = np.random.RandomState(seed)
    sample = rng.choice(len(X), min(sample_size, len(X)), replace=False)
    out = {}
    for k in k_range:
        km = KMeans(n_clusters=k, n_init=10, random_state=seed).fit(X)
        out[k] = {"inertia": float(km.inertia_),
                  "silhouette": float(silhouette_score(X[sample], km.labels_[sample]))}
    return out


def fit(X, k, seed):
    """Ajusta K-Means y devuelve (modelo, etiquetas)."""
    km = KMeans(n_clusters=k, n_init=10, random_state=seed).fit(X)
    return km, km.labels_


def name_clusters(df, labels, audio):
    """Pone nombre a cada cluster según qué feature destaca y cuál falta.

    Para cada grupo miramos el perfil en z-score frente a la media global: la feature más alta y
    la más baja dan el nombre (p. ej. 'Altas en acústicas, bajas en enérgicas'). Mucho más útil
    que 'Cluster 0/1/2'.
    """
    glob_mean = df[audio].mean()
    glob_std = df[audio].std().replace(0, 1)
    nombres = {}
    for c in sorted(set(labels)):
        perfil = df.loc[labels == c, audio].mean()
        z = (perfil - glob_mean) / glob_std
        alta, baja = z.idxmax(), z.idxmin()
        nombres[int(c)] = f"Altas en {_ADJ[alta]}, bajas en {_ADJ[baja]}"
    return nombres
