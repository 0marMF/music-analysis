# Roadmap — Music Data Analysis (Spotify)

**Proyecto de portfolio:** Omar Mora Flores
**Objetivo:** Analizar patrones en datos musicales de Spotify para descubrir qué hace popular a una canción y agrupar canciones con características similares, demostrando habilidades en EDA, visualización y clustering.

**Dataset:** [Spotify Tracks Dataset — Kaggle](https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset)

---

## Estado general

| Fase | Componente | Estado |
|---|---|---|
| 0 | Setup del entorno | Completado |
| 1 | EDA — Qué hace popular a una canción | Completado |
| 2 | Análisis por género | Completado |
| 3 | Clustering — Agrupación de canciones | Completado |
| 4 | (Opcional) Predicción de popularidad | Descartada — el EDA demuestra que el audio no predice popularidad |
| 5 | Cierre de portfolio | Completado |

Leyenda: Pendiente · En progreso · Completado

> **v1.0.0 completo.** Ver abajo **Mejoras planificadas (v1.1)** — el clustering quedó pobre
> (K=2) y faltó *demostrar* el hallazgo de popularidad; ambos son focos declarados del proyecto.

---

## Mejoras planificadas (v1.1) — auditoría 2026-06-06

### P1 — Clustering interpretable (no solo el K óptimo por silhouette)
El silhouette favorece **K=2** ("enérgicas vs acústicas"), pero el objetivo eran clusters ricos
e interpretables ("melancólicas acústicas", "instrumentales tranquilas"…).
- [ ] Presentar también **K=4–5 con nombres descriptivos**, además del K=2
- [ ] Documentar el trade-off **silhouette ↔ interpretabilidad** (la métrica no es el objetivo)
- [ ] Visualización **t-SNE/UMAP** para separar mejor las "vibes" → `reports/`

### P2 — Fase 4: *demostrar* (no solo citar) que el audio no predice popularidad
- [ ] Modelo de regresión/clasificación de `popularity` con features de audio
- [ ] Reportar el **R²/AUC bajo** como evidencia empírica del hallazgo estrella

**Por qué:** el proyecto promete "agrupar por vibes" y "qué hace popular"; K=2 y citar correlaciones
se quedan cortos frente a clusters nombrados y una prueba empírica del resultado negativo.

---

## Backlog de mejoras — v1.1.0 *(en progreso: CP1-CP2 hechos)*

> Derivado de la revisión de calidad (2026-06-06). El clustering quedó por debajo del foco del proyecto.

- [x] **Clustering interpretable (K=4)** además del K=2 óptimo por silhouette — 4 "vibes" nombradas (acústicas/tranquilas, en vivo, alegres, enérgicas); silhouette 0.17 vs 0.26, trade-off documentado.
- [ ] **Reactivar la Fase 4 (predicción de popularidad)** — entrenar un modelo simple para *demostrar empíricamente* el R² bajo (CP4).
- [x] **Visualización UMAP** para una separación visual más fina de los clusters (`reports/09_clusters_pca.png`).

---

## Fase 0 — Setup del entorno

- [ ] Descargar dataset de Kaggle y colocar en `data/`
- [ ] Crear `requirements.txt` con: pandas, numpy, matplotlib, seaborn, plotly, scikit-learn
- [ ] Crear `.gitignore` (excluir `data/`, `*.csv`, `__pycache__/`)
- [ ] Cargar dataset y explorar columnas disponibles

### Columnas clave del dataset de Spotify
| Feature | Descripción |
|---|---|
| `track_name` | Nombre de la canción |
| `artists` | Artista(s) |
| `track_genre` | Género musical |
| `popularity` | Popularidad (0-100) — variable objetivo |
| `danceability` | Qué tan bailable es (0-1) |
| `energy` | Intensidad y actividad (0-1) |
| `valence` | Positividad musical (0-1) |
| `tempo` | BPM |
| `acousticness` | Qué tan acústica es (0-1) |
| `speechiness` | Presencia de palabras habladas (0-1) |
| `instrumentalness` | Qué tan instrumental es (0-1) |
| `loudness` | Volumen en dB |
| `duration_ms` | Duración en milisegundos |

### Entregables
- `requirements.txt` funcional
- Dataset cargado sin errores

---

## Fase 1 — EDA — ¿Qué hace popular a una canción?

**Archivo:** `notebooks/01_EDA.ipynb`
**Pregunta central:** ¿Qué características de audio se asocian con mayor popularidad?

### Secciones

#### 1.1 Carga y descripción del dataset
- [ ] Shape, dtypes, valores nulos, estadísticas descriptivas
- [ ] Cantidad de géneros, artistas únicos, rango de popularidad

#### 1.2 Distribución de popularidad
- [ ] Histograma de popularidad general
- [ ] ¿Qué porcentaje de canciones tiene popularidad > 70?
- [ ] Guardar → `reports/01_popularity_distribution.png`

#### 1.3 Correlación de features de audio con popularidad
- [ ] Heatmap de correlaciones
- [ ] Scatter plots de las 4 features más correlacionadas con popularity
- [ ] Guardar → `reports/02_audio_features_correlation.png`

#### 1.4 Top canciones y artistas
- [ ] Top 10 canciones más populares del dataset
- [ ] Top 10 artistas con mayor popularidad promedio
- [ ] Guardar → `reports/03_top_tracks_artists.png`

#### 1.5 Características de canciones muy populares vs. poco populares
- [ ] Comparar promedios de danceability, energy, valence, tempo entre:
  - Populares (popularity > 70)
  - No populares (popularity < 30)
- [ ] Gráfico tipo radar o barras comparativas
- [ ] Guardar → `reports/04_popular_vs_unpopular.png`

#### 1.6 Duración y popularidad
- [ ] ¿Las canciones más cortas son más populares?
- [ ] Convertir `duration_ms` a minutos y analizar distribución
- [ ] Scatter plot duración vs. popularidad

#### 1.7 Conclusiones del EDA
- [ ] Top 3-5 hallazgos sobre qué hace popular a una canción

### Entregables
- `notebooks/01_EDA.ipynb` sin errores
- 4 imágenes en `reports/`

---

## Fase 2 — Análisis por género

**Archivo:** `notebooks/02_genre_analysis.ipynb`
**Pregunta central:** ¿Tienen diferentes géneros patrones de audio distintos?

### Secciones

#### 2.1 Popularidad por género
- [ ] Popularidad promedio por género (top 15 géneros)
- [ ] Boxplot de popularidad por género
- [ ] Guardar → `reports/05_popularity_by_genre.png`

#### 2.2 Perfil de audio por género
- [ ] Radar chart con danceability, energy, valence, acousticness por género
- [ ] Comparar 5 géneros contrastantes (ej: pop, classical, metal, jazz, reggaeton)
- [ ] Guardar → `reports/06_genre_audio_profile.png`

#### 2.3 Tempo y energía por género
- [ ] ¿El metal tiene mayor BPM que el jazz? ¿El reggaeton más que el classical?
- [ ] Heatmap: géneros × features de audio
- [ ] Guardar → `reports/07_genre_heatmap.png`

#### 2.4 Evolución (si el dataset tiene año de lanzamiento)
- [ ] ¿Ha cambiado la energía o danceability promedio con el tiempo?
- [ ] Gráfico de línea de features por año

### Entregables
- `notebooks/02_genre_analysis.ipynb` sin errores
- 3 imágenes en `reports/`

---

## Fase 3 — Clustering — Agrupación de canciones

**Archivo:** `notebooks/03_clustering.ipynb`
**Pregunta central:** ¿Podemos agrupar canciones por "vibes" similares sin usar el género?
**Algoritmos:** K-Means + visualización con PCA/t-SNE

### Secciones

#### 3.1 Preparación de features para clustering
- [ ] Seleccionar features de audio: danceability, energy, valence, tempo, acousticness, speechiness, instrumentalness, loudness
- [ ] Escalar con `StandardScaler`
- [ ] Reducir dimensionalidad con PCA (2 componentes para visualización)

#### 3.2 Determinar número óptimo de clusters
- [ ] Método del codo (Elbow Method) con inercia vs. K
- [ ] Silhouette Score para K entre 2 y 10
- [ ] Guardar → `reports/08_elbow_silhouette.png`

#### 3.3 Aplicar K-Means
- [ ] Entrenar K-Means con el K óptimo
- [ ] Asignar cluster a cada canción

#### 3.4 Visualización de clusters
- [ ] Scatter plot 2D con PCA coloreado por cluster
- [ ] Guardar → `reports/09_clusters_pca.png`
- [ ] (Opcional) Visualización t-SNE para mejor separación visual

#### 3.5 Interpretación de clusters
- [ ] Calcular promedios de features por cluster
- [ ] Asignar nombre descriptivo a cada cluster:
  - Ejemplo: "Energéticas y bailables" / "Melancólicas acústicas" / "Instrumentales tranquilas"
- [ ] Top 5 canciones representativas por cluster
- [ ] Guardar → `reports/10_cluster_profiles.png`

#### 3.6 ¿Los clusters coinciden con géneros?
- [ ] Cruzar asignación de cluster con género real
- [ ] ¿Captura el modelo patrones musicales reales?

### Entregables
- `notebooks/03_clustering.ipynb` sin errores
- 3 imágenes en `reports/`
- Tabla de canciones representativas por cluster

---

## Fase 4 — (Opcional) Predicción de popularidad

**Archivo:** `notebooks/04_popularity_model.ipynb`
**Meta:** Modelo de regresión o clasificación para predecir popularidad.

### Opción A — Regresión
- [ ] Predecir `popularity` (0-100) con features de audio
- [ ] Modelos: Linear Regression, Random Forest, XGBoost
- [ ] Métricas: MAE, R²

### Opción B — Clasificación
- [ ] Crear variable binaria: `is_popular` = 1 si popularity > 70
- [ ] Modelos: Logistic Regression, Random Forest, XGBoost
- [ ] Métricas: ROC-AUC, F1

> **Nota:** Este modelo suele tener R² bajo porque la popularidad depende de factores externos (marketing, viralidad) no capturados en features de audio. Eso es un hallazgo válido e interesante para documentar.

---

## Fase 5 — Cierre de portfolio

- [ ] Ejecutar todos los notebooks sin errores en entorno limpio
- [ ] Escribir `README.md` con: descripción, hallazgos clave, instrucciones de ejecución, visualizaciones
- [ ] Incluir al menos el radar chart de géneros y el scatter de clusters en el README
- [ ] `.gitignore` excluye el dataset

### Checklist de calidad
- [ ] Narrativa en Markdown entre celdas
- [ ] Gráficos con títulos, ejes etiquetados y leyendas en español
- [ ] Sin rutas absolutas hardcodeadas
- [ ] Los clusters tienen nombres interpretables (no solo "Cluster 0, 1, 2")

---

## De análisis a proyecto de Ciencia de Datos (Track DS — planificado)

Este proyecto no tiene un "modelo" central, pero sí puede convertirse en un mini-producto: un
recomendador por similitud de audio. Eso es lo que lo lleva de "EDA bonito" a proyecto de DS.

**Código modular → `src/`**
- [ ] `src/data.py` (carga + dedup por `track_id`), `src/features.py` (escalado + PCA),
      `src/cluster.py` (entrenar KMeans, nombrar clusters). Los notebooks orquestan.
- [ ] `config.yaml` (features de audio, K, semilla) + `python -m src.pipeline`.

**Tests con pytest**
- [ ] Validación de datos: columnas de audio presentes, rangos 0-1 donde toca, dedup correcto.
- [ ] Test de que el clustering es reproducible con la semilla fija.

**Mini-producto: recomendador de "canciones similares"**
- [ ] Función/CLI `similar(track_id, n=10)` que devuelve canciones del mismo cluster o las más
      cercanas por embedding (vecinos más próximos).
- [ ] (Opcional) API pequeña con FastAPI envolviendo esa función.

**Reproducibilidad y CI**
- [ ] Persistir el modelo de clustering + scaler + PCA (`src/*.pkl`) para no recalcular.
- [ ] GitHub Actions que corre `pytest` en cada push.
- [ ] Model/Data card: qué representa cada cluster, límites (el audio no explica popularidad),
      y que faltan metadatos (año, reproducciones).

> **Estilo:** comentarios y docs con voz de persona. Nombrar clusters como los nombraría un
> humano ("acústicas tristes", no "Cluster 1"), y explicar el *porqué* de cada decisión.

---

## Orden de desarrollo

```
Fase 0 → Fase 1 → Fase 2 → Fase 3 → (Fase 4) → Fase 5
  Setup    EDA    Géneros  Clustering  Model     Cierre
```

---

## Notas técnicas

- Si el dataset tiene duplicados por la misma canción en múltiples géneros, deduplicar por `track_id` antes del clustering
- K-Means requiere escalar antes de aplicar — features en distintas escalas sesgan los clusters
- La fase 4 (predicción) probablemente no logrará R² alto — eso es un resultado válido: la popularidad no depende solo de las features de audio
- El análisis más visualmente impactante para portfolio es el radar chart por género y el scatter de clusters coloreado
