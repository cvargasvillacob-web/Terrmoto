"""Prepara locales.json para el mapa: prioridad, ubicación aproximada y grupo de recorrido.

Uso: python3 preparar_locales.py <repo> <carpeta_geo> <salida.json>

La posición de cada anuncio es aproximada: si el texto nombra una estación del
Metro se ubica junto a ella; si no, en un punto interior del corregimiento. Se le
suma un desplazamiento fijo de unos cientos de metros para que no se encimen.
"""
import hashlib
import json
import math
import re
import sys
import unicodedata
from pathlib import Path

REPO, GEO, SALIDA = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
sys.path.insert(0, str(REPO / "locales"))
import armar_lista as a  # noqa: E402


def plano(t):
    t = unicodedata.normalize("NFD", str(t or "").lower())
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", "".join(c for c in t if unicodedata.category(c) != "Mn"))).strip()


metro = json.loads((GEO / "metro.json").read_text(encoding="utf-8"))
corr = json.loads((GEO / "corregimientos.json").read_text(encoding="utf-8"))["features"]
punto_corr = {plano(f["properties"]["nombre"]): (f["properties"]["cy"], f["properties"]["cx"]) for f in corr}
punto_est = {plano(s["nombre"]): (s["lat"], s["lon"], s["nombre"]) for s in metro}

# Barrios y referencias que no son nombre de estación ni de corregimiento -> corregimiento
BARRIO = {
    "nuevo tocumen": "tocumen", "altos de tocumen": "tocumen", "la dona": "24 de diciembre", "felipillo": "24 de diciembre",
    "nuevo belen": "24 de diciembre", "cabuya": "24 de diciembre", "ciudad del sol": "pacora", "las garzas": "pacora",
    "llano bonito": "juan diaz", "los pueblos": "juan diaz", "crystal plaza": "juan diaz", "villa zaita": "ernesto cordoba campos",
    "milla 8": "las cumbres", "ciudad del lago": "las cumbres", "lucha franco": "las cumbres", "la castellana": "jose domingo espinar",
    "brisas del golf": "rufina alfaro", "cerro viento": "rufina alfaro", "villa lucre": "jose domingo espinar",
    "paraiso": "victoriano lorenzo", "gran estacion": "victoriano lorenzo", "altos de panama": "omar torrijos",
    "los andes": "jose domingo espinar", "costa verde": "barrio colon", "mariano rivera": "barrio colon",
    "alto de pradera": "barrio colon", "plaza 2 000": "burunga", "plaza 2000": "burunga", "vacamonte": "arraijan cabecera",
    "nuevo arraijan": "juan demostenes arosemena", "panamericana": "arraijan cabecera",
}
ZONA_CORR = {
    "tocumen": "tocumen", "24 de diciembre": "24 de diciembre", "pacora": "pacora", "las mananitas": "las mananitas",
    "juan diaz": "juan diaz", "ernesto cordoba campos": "ernesto cordoba campos", "las cumbres": "las cumbres",
    "alcalde diaz": "alcalde diaz", "san miguelito": "belisario porras", "la chorrera": "barrio colon",
    "burunga": "burunga", "cerro silvestre": "cerro silvestre", "vista alegre": "vista alegre",
    "arraijan": "arraijan cabecera", "juan d arosemena": "juan demostenes arosemena",
    "nuevo arraijan": "juan demostenes arosemena", "vacamonte": "arraijan cabecera",
}
# Estaciones cuyo nombre es también un barrio: si el texto lo nombra, el local está cerca
ESTACIONES_REFERENCIA = ["nuevo tocumen", "24 de diciembre", "altos de tocumen", "las mananitas", "hospital del este",
                         "villa zaita", "san isidro", "los andes", "pan de azucar", "san miguelito", "paraiso",
                         "cincuentenario", "villa lucre", "el crisol", "brisas del golf", "cerro viento", "san antonio",
                         "pedregal", "don bosco"]
RECORRIDO = {
    "Este": {"tocumen", "24 de diciembre", "pacora", "las mananitas", "juan diaz"},
    "Norte": {"ernesto cordoba campos", "las cumbres", "alcalde diaz"},
    "San Miguelito": {"san miguelito"},
    "Oeste": {"la chorrera", "burunga", "cerro silvestre", "vista alegre", "arraijan", "juan d arosemena",
              "nuevo arraijan", "vacamonte"},
}


def desplazar(lat, lon, semilla, metros=(120, 380)):
    h = int(hashlib.sha1(semilla.encode()).hexdigest(), 16)
    ang = (h % 360) * math.pi / 180
    r = metros[0] + (h // 360) % (metros[1] - metros[0])
    return round(lat + r * math.sin(ang) / 111000, 5), round(lon + r * math.cos(ang) / 109500, 5)


def ubicar(x):
    texto = plano(" ".join(str(x.get(k) or "") for k in ("ubicacion", "titulo")))
    zona = plano(x.get("zona"))
    zona_ok = ZONA_CORR.get(zona)
    for e in ESTACIONES_REFERENCIA:
        if re.search(rf"\b{e}\b", texto) and e in punto_est:
            # la estación debe quedar en la zona del anuncio (evita "San Miguelito" como distrito)
            if e == "san miguelito" and "estacion" not in texto and "metro" not in texto:
                continue
            la, lo, n = punto_est[e]
            return la, lo, f"cerca de la estación {n} (aproximada)", "estacion"
    for b, c in BARRIO.items():
        if re.search(rf"\b{b}\b", texto) and c in punto_corr:
            la, lo = punto_corr[c]
            return la, lo, f"centro del corregimiento por la referencia «{b.title()}» (aproximada)", "corregimiento"
    for c in sorted(punto_corr, key=len, reverse=True):
        if len(c) > 5 and re.search(rf"\b{c}\b", texto):
            la, lo = punto_corr[c]
            return la, lo, "centro del corregimiento que nombra el anuncio (aproximada)", "corregimiento"
    if zona.startswith("via transistmica") and "san isidro" in punto_est:
        # tramo sin confirmar: se usa la estación San Isidro solo como referencia sobre la vía
        la, lo, _ = punto_est["san isidro"]
        return la, lo, "de referencia sobre la Vía Transístmica; el tramo está sin confirmar", "corregimiento"
    if zona_ok and zona_ok in punto_corr:
        la, lo = punto_corr[zona_ok]
        return la, lo, "centro del corregimiento de la zona (aproximada)", "corregimiento"
    return None


def grupo(x):
    z = plano(x.get("zona"))
    if z.startswith("via transistmica"):
        return "Norte"
    for g, zs in RECORRIDO.items():
        if z in zs:
            return g
    return "Otras"


base = json.loads((REPO / "locales" / "datos" / "anuncios.json").read_text(encoding="utf-8"))
salida, sin_lugar = [], 0
for x in base:
    r = a.evaluar(x)
    u = ubicar(x)
    if not u:
        sin_lugar += 1
        continue
    la, lo, como, tipo = u
    la, lo = desplazar(la, lo, x["url"])
    notas = re.sub(r"\s+", " ", str(x.get("notas") or "")).strip()
    salida.append({
        "id": hashlib.sha1(x["url"].encode()).hexdigest()[:10],
        "prioridad": r["prioridad"], "puntos": r["puntos"], "zona": x.get("zona"), "grupo": grupo(x),
        "titulo": re.sub(r"\s*\((t[ií]tulo|titulo)[^)]*\)\s*", " ", str(x.get("titulo") or "")).strip(),
        "tipo": x.get("tipo"), "area": r["area"], "precio": r["precio"], "por_m2": r["por_m2"],
        "planta": x.get("planta"), "ubicacion": x.get("ubicacion"), "anunciante": x.get("anunciante"),
        "telefono": x.get("telefono"), "url": x.get("url"), "es_listado": bool(x.get("url_es_listado")),
        "confirmar": r["confirmar"], "descarte": r["descarte"], "notas": notas[:600],
        "primera_vez": (x.get("primera_vez") or "")[:10], "lat": la, "lon": lo, "precision": como, "tipo_pos": tipo,
    })
orden = {"A": 0, "B": 1, "C": 2, "D": 3}
salida.sort(key=lambda r: (orden[r["prioridad"]], -r["puntos"], r["por_m2"] or 999))
SALIDA.write_text(json.dumps(salida, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
from collections import Counter
print(len(salida), "anuncios ubicados;", sin_lugar, "sin ubicar;", Counter(r["prioridad"] for r in salida),
      Counter(r["grupo"] for r in salida if r["prioridad"] == "A"), Counter(r["tipo_pos"] for r in salida))
