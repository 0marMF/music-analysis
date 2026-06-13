"""¿Predicen las features de audio la popularidad? (spoiler: no).

El EDA ya mostraba correlaciones casi nulas. Aquí lo demostramos en serio: entrenamos modelos a
predecir `popularity` (0-100) desde el audio y medimos el R². Si ni un Random Forest pasa de un
R² ridículo, queda probado que la popularidad depende de cosas que el audio no captura
(marketing, artista, viralidad). Un resultado "negativo" pero honesto y valioso.
"""
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from . import data
from .config import load_config


def train_models(cfg: dict | None = None) -> dict:
    """Entrena Linear Regression y Random Forest y devuelve R²/MAE + predicciones del mejor."""
    cfg = cfg or load_config()
    audio = cfg["features"]["audio"]
    songs, _ = data.clean(data.load_raw(cfg))

    X = songs[audio].to_numpy(dtype=np.float64)
    y = songs["popularity"].to_numpy(dtype=np.float64)
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=cfg["seed"])

    # Escalamos para la regresión lineal; a los árboles les da igual, pero no les perjudica.
    scaler = StandardScaler().fit(X_tr)
    X_tr_s, X_te_s = scaler.transform(X_tr), scaler.transform(X_te)

    modelos = {
        "Linear Regression": (LinearRegression(), X_tr_s, X_te_s),
        "Random Forest": (RandomForestRegressor(n_estimators=100, max_depth=14, n_jobs=-1,
                                                random_state=cfg["seed"]), X_tr, X_te),
    }
    resultados, preds = {}, {}
    for nombre, (modelo, Xt, Xv) in modelos.items():
        modelo.fit(Xt, y_tr)
        p = modelo.predict(Xv)
        preds[nombre] = p
        resultados[nombre] = {"r2": float(r2_score(y_te, p)),
                              "mae": float(mean_absolute_error(y_te, p))}
    return {"results": resultados, "y_test": y_te, "preds": preds}
