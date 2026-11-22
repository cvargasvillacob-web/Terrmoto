"""Exporta las formas del logo (edificio y textos convertidos a trazos) para la escena 3D.

Uso: python3 sitio/marca/logo3d/exportar_formas.py   -> formas.json
"""
import json
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent))
from generar_logos import MARCA, SANS, SERIF  # noqa: E402

textos = {
    "PACIFICA": SANS.texto("PACIFICA", 230, 0, 0, tracking=SANS.tracking_para("PACIFICA", 230, 1700)),
    "INMOBILIARIA": SERIF.texto("INMOBILIARIA", 150, 0, 0, tracking=SERIF.tracking_para("INMOBILIARIA", 150, 1700)),
    "20": SERIF.texto("20", 820, 0, 0, tracking=-0.03),
    "AÑOS": SANS.texto("AÑOS", 150, 0, 0, tracking=SANS.tracking_para("AÑOS", 150, 700)),
}
(AQUI / "formas.json").write_text(json.dumps({"marca": MARCA, "textos": textos}))
print("formas.json", {k: len(v) for k, v in textos.items()})
