# 🔎 Hallazgos y Aprendizajes — Music Data Analysis (Spotify)

> Detecciones del EDA, el análisis por género y el clustering, más los aprendizajes del proyecto.

**Autor:** Omar Mora Flores · **Última actualización:** 2026-06-06

---

## 🧭 Resumen ejecutivo

Sobre **114,000 pistas** de Spotify (89,741 canciones únicas, 114 géneros), el resultado más
importante es **negativo y revelador**: las features de audio **no predicen la popularidad**
(todas las correlaciones |r| < 0.1). El valor del proyecto está en el **análisis por género** y
en el **clustering por "vibes"**, que agrupa canciones por similitud sonora cruzando las
etiquetas de género.

---

## 📊 Detecciones del EDA (Fase 1)

| # | Detección | Evidencia |
|---|---|---|
| 1 | **El audio no explica la popularidad** — máx |r| = 0.095 (instrumentalness) | `02_audio_features_correlation.png` |
| 2 | **Popularidad sesgada a valores bajos** — media 33, solo 4.3% > 70 | `01_popularity_distribution.png` |
| 3 | **24,259 duplicados por `track_id`** (misma canción en varios géneros) | `01_EDA` → se deduplica a nivel canción |
| 4 | Populares ligeramente **más bailables/enérgicas**, menos acústicas — diferencia modesta | `04_popular_vs_unpopular.png` |

---

## 🎸 Detecciones por género (Fase 2)

- Los géneros **sí tienen perfiles de audio diferenciados**: el radar separa classical (acústica/
  instrumental) de metal/edm (enérgica). Ver `06_genre_audio_profile.png` y `07_genre_heatmap.png`.
- La popularidad media varía mucho entre géneros → la popularidad es más de **género y contexto**
  que de features de audio aisladas.
- ⚠️ El dataset **no tiene año de lanzamiento** → el análisis de evolución temporal no es aplicable.

---

## 🧩 Detecciones del clustering (Fase 3)

- El **silhouette es máximo en K=2** (0.261), pero K=2 solo separa "enérgicas vs acústicas".
  Elegimos **K=4** (silhouette 0.171) por interpretabilidad: la métrica óptima no es el objetivo.
- **Cuatro "vibes" nombradas:** acústicas/tranquilas (18,648), en vivo (7,001), alegres (36,646),
  enérgicas/poco acústicas (27,445).
- **UMAP** separa los grupos visualmente mejor que PCA (`reports/09_clusters_pca.png`).
- **Los clusters cruzan géneros** (género dominante minoritario por cluster) → no son un
  re-etiquetado del género, sino agrupaciones por sonoridad. Base del recomendador por similitud.

---

## 🎓 Aprendizajes

**Técnicos**
1. **Un resultado "negativo" es un resultado válido.** Demostrar con datos que el audio no predice
   la popularidad es un hallazgo honesto y valioso (y evita construir un modelo predictivo inútil).
2. **Escalar antes de K-Means / PCA** es imprescindible: features en escalas distintas (tempo,
   loudness vs 0-1) sesgarían los clusters.
3. **El silhouette sobre una muestra** evita el costo O(n²) en datasets grandes (~90k).
4. **Deduplicar por `track_id`** para análisis a nivel canción, pero conservar los duplicados de
   género para el análisis por género.
5. **La métrica no es el objetivo.** El silhouette pedía K=2, pero K=4 da "vibes" mucho más
   útiles; nombrarlas por su perfil z-score las hace accionables (no "Cluster 0/1/2/3").

**De proceso**
6. **Validar el roadmap contra los datos reales:** descubrir temprano que falta la columna de año
   evitó planificar un análisis imposible.

---

## ⚠️ Limitaciones y próximos pasos

- [ ] Probar **clustering jerárquico / DBSCAN** y comparar con K-Means.
- [ ] Visualización **t-SNE/UMAP** para separación más fina de "vibes".
- [ ] Enriquecer con metadatos externos (año, número de reproducciones) para modelar popularidad.
- [ ] Construir un mini-recomendador "canciones similares" usando los clusters/embeddings.

---

*Documento vivo — se actualiza conforme evoluciona el proyecto.*
