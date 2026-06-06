# 🎵 Music Data Analysis (Spotify)

> **¿Qué hace popular a una canción? ¿Y podemos agrupar temas por "vibes"?**
> *EDA, análisis por género y clustering (K-Means + PCA) sobre 114,000 pistas de Spotify*

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://python.org)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.5+-F7931E?logo=scikit-learn)](https://scikit-learn.org)
[![Seaborn](https://img.shields.io/badge/Seaborn-viz-4c72b0)](https://seaborn.pydata.org)

---

## 📌 Objetivo

Explorar qué características de audio se asocian con la popularidad, comparar perfiles de audio
entre géneros y **agrupar canciones por similitud sonora sin usar la etiqueta de género**.

---

## 🎯 Hallazgos principales

| Hallazgo | Detalle |
|---|---|
| **El audio NO predice la popularidad** | Todas las correlaciones audio↔popularidad son |r| < 0.1 (máx: instrumentalness −0.095) |
| **Popularidad sesgada** | Media 33/100; solo **4.3%** de las canciones superan 70 |
| **Géneros con perfiles distintos** | classical (acústica/instrumental) vs metal/edm (enérgica) bien separados |
| **2 grandes "vibes"** | El clustering óptimo (K=2) separa **enérgicas** (67,438) de **acústicas** (22,302) |
| **Los clusters cruzan géneros** | El género dominante de cada cluster es solo 1–4% → no es re-etiquetado |

---

## 🔬 Metodología

1. **EDA** (`01_EDA.ipynb`) — distribución de popularidad, correlación audio↔popularidad,
   top canciones/artistas, perfil populares vs. poco populares.
2. **Análisis por género** (`02_genre_analysis.ipynb`) — popularidad por género, radar de perfiles
   de audio, heatmap géneros × features.
3. **Clustering** (`03_clustering.ipynb`) — escalado + PCA, codo + silhouette para elegir K,
   K-Means, interpretación de clusters y cruce con géneros.

> ⚠️ El dataset **no tiene año de lanzamiento**, por lo que el análisis de evolución temporal
> previsto en el roadmap no es aplicable. La fase de predicción de popularidad (opcional) se
> omite porque el EDA ya demuestra que las features de audio no la explican.

---

## 🧩 Clustering — "vibes" de audio

K-Means con K=2 (máximo silhouette = 0.261) produce dos grupos nítidos e interpretables:

![Clusters PCA](reports/09_clusters_pca.png)

- 🔵 **Enérgicas / poco acústicas** (67,438 temas) — incluye los grandes hits (Unholy, Quevedo BZRP).
- 🟢 **Acústicas / poco enérgicas** (22,302 temas) — Glimpse of Us, Another Love, Running Up That Hill.

Ambos grupos **mezclan muchos géneros**, capturando la "vibe" sonora más allá de la etiqueta.

---

## 🏗️ Estructura

```
music-analysis/
├── data/dataset.csv              # 114,000 pistas (no versionado)
├── notebooks/
│   ├── 01_EDA.ipynb
│   ├── 02_genre_analysis.ipynb
│   └── 03_clustering.ipynb
├── reports/                      # 10 visualizaciones
├── HALLAZGOS.md
├── README.md
└── ROADMAP.md
```

---

## 🚀 Cómo ejecutar

```bash
pip install -r requirements.txt
jupyter nbconvert --to notebook --execute --inplace notebooks/01_EDA.ipynb
jupyter nbconvert --to notebook --execute --inplace notebooks/02_genre_analysis.ipynb
jupyter nbconvert --to notebook --execute --inplace notebooks/03_clustering.ipynb
```

> Dataset: [Spotify Tracks Dataset — Kaggle](https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset).
> Colócalo en `data/dataset.csv` (no se versiona).

> 📄 Detalle de detecciones y aprendizajes en [`HALLAZGOS.md`](HALLAZGOS.md).

---

## 👨‍💻 Autor

**Omar Mora Flores** · Data Analyst & ML Engineer
📧 omar13mor@gmail.com · 🔗 [linkedin.com/in/omar-mora-flores](https://linkedin.com/in/omar-mora-flores)
