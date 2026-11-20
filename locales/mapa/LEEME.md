# Mapa de locales

Página interactiva con la población por corregimiento, el Metro (líneas 1 y 2) y los
anuncios de locales de `locales/datos/anuncios.json`, con el plan de llamadas y recorrido.

- Publicado en: https://claude.ai/artifact/YXzGaM6k8gaTgC1sfAazKk
- Para actualizarlo: `python3 locales/mapa/construir.py` y publicar `locales/mapa/publicar/index.html`
  con los archivos `datos/corregimientos.json`, `datos/metro.json` y `datos/locales.json` al lado,
  en la misma URL.

Fuentes:
- Límites de corregimientos: geoBoundaries, nivel ADM3 de Panamá (CC BY 4.0). Pueden no reflejar
  divisiones recientes.
- Población: Censo 2023 (INEC), tomada de las notas del estudio en `research_notes/`.
- Estaciones del Metro: dos conjuntos de datos públicos cruzados; difieren 121 m como máximo.
- La posición de cada local es aproximada (estación del Metro que nombra el anuncio o centro del
  corregimiento).
