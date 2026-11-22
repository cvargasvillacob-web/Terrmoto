"""Exporta las formas del logo (edificio y textos convertidos a trazos) para la escena 3D.

Uso: python3 sitio/marca/logo3d/exportar_formas.py   -> formas.json
"""
import json
import math
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent))
from generar_logos import MARCA, SANS, SERIF  # noqa: E402
from shapely.geometry import LineString, Point, Polygon  # noqa: E402
from shapely.ops import unary_union  # noqa: E402

textos = {
    "PACIFICA": SANS.texto("PACIFICA", 230, 0, 0, tracking=SANS.tracking_para("PACIFICA", 230, 1700)),
    "INMOBILIARIA": SERIF.texto("INMOBILIARIA", 150, 0, 0, tracking=SERIF.tracking_para("INMOBILIARIA", 150, 1700)),
    "20": SERIF.texto("20", 820, 0, 0, tracking=-0.03),
    "AÑOS": SANS.texto("AÑOS", 150, 0, 0, tracking=SANS.tracking_para("AÑOS", 150, 700)),
}


def bezier(p0, p1, p2, p3, n=40):
    return [tuple((1 - t) ** 3 * a + 3 * (1 - t) ** 2 * t * b + 3 * (1 - t) * t ** 2 * c + t ** 3 * d
                  for a, b, c, d in zip(p0, p1, p2, p3)) for t in (i / n for i in range(n + 1))]


def a_d(geom):
    """Polígonos de shapely -> trazo SVG (contornos y huecos)."""
    polis = getattr(geom, "geoms", [geom])
    partes = []
    for pol in polis:
        for anillo in [pol.exterior, *pol.interiors]:
            pts = list(anillo.coords)
            partes.append("M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + "Z")
    return "".join(partes)


def pin():
    """Gota con centro hueco atravesada por tres ondas como las del logo (mismas medidas que el pin 2D)."""
    cx, cy, r = 200, 190, 160
    arco = [(cx + r * math.cos(a), cy + r * math.sin(a)) for a in (math.pi + math.pi * i / 80 for i in range(81))]
    derecha = bezier((360, 190), (360, 300), (252, 392), (200, 470))
    izquierda = bezier((200, 470), (148, 392), (40, 300), (40, 190))
    gota = Polygon(arco + derecha[1:] + izquierda[1:]).buffer(0)
    hueco = Point(cx, cy).buffer(70, 96)
    cuerpo = gota.difference(hueco)
    ondas = []
    for k in range(3):
        o = k * 50
        linea = bezier((-20, 326 + o), (70, 346 + o), (150, 340 + o), (232, 300 + o)) + \
            bezier((232, 300 + o), (314, 260 + o), (362, 220 + o), (430, 210 + o))[1:]
        ondas.append(LineString(linea).buffer(14, cap_style=2))
    ondas = unary_union(ondas).intersection(cuerpo)
    return {"cuerpo": a_d(cuerpo.difference(ondas)), "ondas": a_d(ondas)}


(AQUI / "formas.json").write_text(json.dumps({"marca": MARCA, "textos": textos, "pin": pin()}))
print("formas.json", {k: len(v) for k, v in textos.items()})
