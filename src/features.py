"""Preparación de las features de audio para el clustering."""
import numpy as np
from sklearn.preprocessing import StandardScaler


def scale(df, cfg, scaler: StandardScaler | None = None):
    """Escala las features de audio. Sin escalar, tempo y loudness (en otras unidades)
    dominarían las distancias y sesgarían los clusters.

    Si se pasa un scaler ya ajustado lo reutiliza (para puntuar canciones nuevas); si no, lo
    ajusta. Devuelve (X escalado, scaler).
    """
    audio = cfg["features"]["audio"]
    X = df[audio].to_numpy(dtype=np.float64)
    if scaler is None:
        scaler = StandardScaler()
        X = scaler.fit_transform(X)
    else:
        X = scaler.transform(X)
    return X, scaler
