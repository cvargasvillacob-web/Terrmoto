#!/usr/bin/env python3
"""Arma el mapa de locales listo para publicar.

Uso: python3 locales/mapa/construir.py

Lee la base de anuncios (locales/datos/anuncios.json) y escribe en
locales/mapa/publicar/ la página index.html y sus datos (datos/*.json).
La página se publica como artifact con esos tres archivos de datos al lado.
"""
import shutil
import subprocess
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
REPO = AQUI.parent.parent
SALIDA = AQUI / "publicar"
(SALIDA / "datos").mkdir(parents=True, exist_ok=True)

for nombre in ("corregimientos.json", "metro.json"):
    shutil.copy(AQUI / "base" / nombre, SALIDA / "datos" / nombre)
subprocess.run([sys.executable, str(AQUI / "preparar_locales.py"), str(REPO), str(AQUI / "base"),
                str(SALIDA / "datos" / "locales.json")], check=True)
css = (AQUI / "base" / "leaflet-1.9.4.css").read_text(encoding="utf-8")
pagina = (AQUI / "plantilla.html").read_text(encoding="utf-8").replace("/*LEAFLET_CSS*/", css)
(SALIDA / "index.html").write_text(pagina, encoding="utf-8")
print("Mapa listo en", SALIDA.relative_to(REPO))
