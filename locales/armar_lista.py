#!/usr/bin/env python3
"""Arma la lista de llamadas a partir de los hallazgos del agente buscador de locales.

Uso:
    python3 locales/armar_lista.py locales/datos/2026-11-19.json

Lee el JSON de hallazgos del día, descarta duplicados, puntúa cada local contra
los criterios del proyecto (supermercado de proximidad de ~250 m²) y escribe:
    locales/Locales para llamar AAAA-MM-DD.md   (para leer y llamar)
    locales/Locales para llamar AAAA-MM-DD.csv  (para llevar el seguimiento)

Si hay archivos de días anteriores en la misma carpeta de datos, marca como
NUEVO lo que no se había visto antes. Solo usa la biblioteca estándar.
"""
import csv
import json
import re
import sys
import unicodedata
from pathlib import Path

# --- Criterios del proyecto (ver reports/Penetración supermercados 250 m2 Panamá.md) ---
AREA_IDEAL = (280, 350)        # m² arrendables para ~250 m² de sala
AREA_ACEPTABLE = (220, 400)
AREA_LIMITE = (180, 500)
RENTA_IDEAL = 15               # US$/m²/mes
RENTA_TOPE = 21
RENTA_DESCARTE = 25
TOTAL_MAXIMO = 6500            # US$/mes, sin mantenimiento ni ITBMS

OLA_1 = ["tocumen", "24 de diciembre", "pacora", "mananitas", "ernesto cordoba",
         "villa zaita", "las cumbres", "alcalde diaz"]
OLA_2 = ["chorrera", "vista alegre", "arraijan", "arosemena", "burunga",
         "cerro silvestre", "vacamonte", "nuevo chorrillo"]

TIPOS_APTOS = ("local", "esquiner", "edificio", "plaza")
TIPOS_NO_APTOS = ("galera", "bodega", "oficina", "consultorio", "terreno")


def plano(texto):
    """Minúsculas y sin tildes, para comparar nombres de zonas."""
    texto = unicodedata.normalize("NFD", str(texto or "").lower())
    return "".join(c for c in texto if unicodedata.category(c) != "Mn")


def ola(zona):
    z = plano(zona)
    if any(n in z for n in OLA_1):
        return 1
    if any(n in z for n in OLA_2):
        return 2
    return 3  # oportunista


def clave(item):
    """Identifica un anuncio. En Encuentra24 el número final es el id del anuncio.

    Varias fichas pueden compartir la URL de una página de listado; en ese caso
    se distinguen por el área o, si no hay, por el título.
    """
    url = str(item.get("url") or "").strip().rstrip("/")
    m = re.search(r"encuentra24\.com/.*/(\d{6,})$", url)
    if m:
        return "e24:" + m.group(1)
    k = re.sub(r"^https?://(www\.)?", "", url).lower()
    if item.get("url_es_listado"):
        area = numero(item.get("area_m2"))
        k += "#" + (f"{area:g}" if area else plano(item.get("titulo"))[:40])
    return k


def numero(valor):
    try:
        n = float(valor)
        return n if n > 0 else None
    except (TypeError, ValueError):
        return None


def evaluar(item):
    """Puntúa un anuncio y le asigna prioridad.

    A: área y alquiler conocidos y dentro de los criterios.
    B: falta algún dato o el área queda cerca del rango; hay que llamar para saber.
    C: se sabe que incumple algo negociable (alquiler sobre el tope, local muy grande).
    D: descartado (tipo no apto, planta alta, área o alquiler muy fuera de rango).
    """
    area = numero(item.get("area_m2"))
    precio = numero(item.get("precio_mensual_usd"))
    por_m2 = round(precio / area, 1) if area and precio else None
    tipo = plano(item.get("tipo"))
    planta = plano(item.get("planta"))
    confirmar, descarte = [], None
    faltan_datos = incumple = False

    if any(t in tipo for t in TIPOS_NO_APTOS):
        descarte = f"tipo no apto ({item.get('tipo')})"
    elif planta == "alta":
        descarte = "planta alta"
    elif not any(t in tipo for t in TIPOS_APTOS):
        faltan_datos = True
        confirmar.append("qué tipo de inmueble es y si sirve como local de venta")

    if area is None:
        p_area, faltan_datos = 1, True
        confirmar.append("área arrendable")
    elif AREA_IDEAL[0] <= area <= AREA_IDEAL[1]:
        p_area = 3
    elif AREA_ACEPTABLE[0] <= area <= AREA_ACEPTABLE[1]:
        p_area = 2
    elif AREA_LIMITE[0] <= area <= AREA_LIMITE[1]:
        p_area, faltan_datos = 1, True
        confirmar.append(f"si hay una unidad de {AREA_ACEPTABLE[0]}-{AREA_ACEPTABLE[1]} m² o se puede ajustar el área")
    elif area > AREA_LIMITE[1] and precio is not None and precio <= TOTAL_MAXIMO:
        p_area, incumple = 0, True
        confirmar.append("área techada real y si se puede subdividir (el total sí entra en presupuesto)")
    else:
        p_area = 0
        descarte = descarte or f"área fuera de rango ({area:g} m²)"

    if precio is None:
        p_renta, faltan_datos = 1, True
        confirmar.append("alquiler mensual, mantenimiento e ITBMS")
    elif por_m2 is None:
        p_renta = 1
    elif por_m2 <= RENTA_IDEAL:
        p_renta = 3
    elif por_m2 <= RENTA_TOPE:
        p_renta = 2
    elif por_m2 <= RENTA_DESCARTE:
        p_renta, incumple = 1, True
        confirmar.append(f"si el alquiler es negociable (está sobre el tope de US${RENTA_TOPE}/m²)")
    else:
        p_renta = 0
        descarte = descarte or f"alquiler alto (US${por_m2:g}/m²)"

    if precio is not None and precio > TOTAL_MAXIMO and not descarte and p_area > 0:
        p_renta, incumple = min(p_renta, 1), True
        confirmar.append(f"si el total es negociable (supera el máximo de US${TOTAL_MAXIMO:,}/mes)")

    n_ola = ola(item.get("zona"))
    p_zona = {1: 3, 2: 2, 3: 1}[n_ola]

    if planta in ("", "n/d", "varios niveles"):
        confirmar.append("que sea planta baja a pie de calle")

    puntos = p_area + p_renta + p_zona
    if descarte:
        prioridad = "D"
    elif incumple:
        prioridad = "C"
    elif faltan_datos:
        prioridad = "B"
    else:
        prioridad = "A"

    return {**item, "area": area, "precio": precio, "por_m2": por_m2, "ola": n_ola,
            "puntos": puntos, "prioridad": prioridad, "descarte": descarte,
            "confirmar": confirmar}


def dinero(n):
    return f"US${n:,.0f}" if n is not None else "n/d"


def ficha(codigo, r):
    datos = " · ".join([
        f"{r['area']:g} m²" if r["area"] else "área n/d",
        f"{dinero(r['precio'])}/mes" if r["precio"] else "alquiler n/d",
        f"US${r['por_m2']:g}/m²" if r["por_m2"] else "US$/m² n/d",
    ])
    contacto = " — ".join(x for x in [r.get("anunciante"), r.get("telefono")] if x)
    es_listado = bool(r.get("url_es_listado"))
    sin_contacto = ("buscar la ficha en el listado para ver el teléfono" if es_listado
                    else "abrir el anuncio para ver el teléfono")
    lineas = [
        f"### {codigo} · {r.get('zona') or 'Zona n/d'} — {r.get('titulo') or 'Sin título'}"
        + (" · NUEVO" if r.get("nuevo") else ""),
        f"- **Datos:** {datos} · planta {r.get('planta') or 'n/d'} · ola {r['ola']} · {r['puntos']}/9 puntos",
        f"- **Ubicación:** {r.get('ubicacion') or 'n/d'}",
        f"- **Contacto:** {contacto + ' (teléfono en el anuncio)' if contacto and not r.get('telefono') else contacto or sin_contacto}",
        f"- **{'Listado donde aparece' if es_listado else 'Anuncio'}:** <{r.get('url')}>",
    ]
    if r["confirmar"]:
        lineas.append(f"- **Confirmar en la llamada:** {'; '.join(r['confirmar'])}")
    if r.get("notas"):
        lineas.append(f"- **Notas:** {r['notas']}")
    return "\n".join(lineas)


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    origen = Path(sys.argv[1])
    fecha = origen.stem
    hallazgos = json.loads(origen.read_text(encoding="utf-8"))

    vistos_antes = set()
    anteriores = [p for p in origen.parent.glob("*.json") if p.stem < fecha]
    for p in anteriores:
        vistos_antes.update(clave(i) for i in json.loads(p.read_text(encoding="utf-8")))

    unicos = {}
    for item in hallazgos:
        if not item.get("url"):
            continue  # sin enlace no se puede comprobar ni llamar
        k = clave(item)
        previo = unicos.get(k)
        # ante duplicados, se queda el que trae más datos
        if previo is None or sum(v is not None for v in item.values()) > sum(v is not None for v in previo.values()):
            unicos[k] = item

    filas = []
    for k, item in unicos.items():
        r = evaluar(item)
        r["nuevo"] = bool(anteriores) and k not in vistos_antes
        filas.append(r)
    filas.sort(key=lambda r: (r["prioridad"], -r["puntos"], r["ola"], r["por_m2"] or 999))

    titulos = {
        "A": "Prioridad A: cumplen área y alquiler, llamar primero",
        "B": "Prioridad B: faltan datos o el área queda cerca del rango",
        "C": "Prioridad C: incumplen algo negociable (alquiler o tamaño)",
        "D": "Descartados (no cumplen)",
    }
    conteo = {p: sum(r["prioridad"] == p for r in filas) for p in titulos}
    salida = [
        f"# Locales para llamar — {fecha}",
        "",
        f"{len(filas)} anuncios revisados: {conteo['A']} de prioridad A, {conteo['B']} de prioridad B, "
        f"{conteo['C']} de prioridad C y {conteo['D']} descartados.",
        "",
        "> Los datos salen de resultados del buscador web, no de la lectura del anuncio completo "
        "(los portales bloquean el acceso automatizado). Área, precio y vigencia deben confirmarse "
        "al abrir el anuncio y en la llamada.",
        "",
        "## Qué busca el proyecto",
        "",
        f"- Local en planta baja, en plaza de barrio o a pie de calle; {AREA_ACEPTABLE[0]}-{AREA_ACEPTABLE[1]} m² "
        f"arrendables (ideal {AREA_IDEAL[0]}-{AREA_IDEAL[1]}).",
        f"- Alquiler ideal hasta US${RENTA_IDEAL}/m² al mes; tope US${RENTA_TOPE}/m² y US${TOTAL_MAXIMO:,} en total.",
        "- Ola 1: Tocumen, 24 de Diciembre, Pacora, Las Mañanitas, Ernesto Córdoba Campos, Las Cumbres y Alcalde Díaz. "
        "Ola 2: La Chorrera y Arraiján. El resto es oportunista.",
        "",
        "## Preguntas para cada llamada",
        "",
        "1. ¿Sigue disponible? ¿Desde cuándo se puede ocupar?",
        "2. Área arrendable exacta, frente del local y altura libre.",
        "3. Alquiler mensual, cuota de mantenimiento, ITBMS, depósito y aumentos anuales.",
        "4. Plazo mínimo del contrato y meses de gracia para adecuar el local.",
        "5. ¿Se entrega en gris o terminado? ¿Tiene energía trifásica y capacidad para refrigeración y aire acondicionado?",
        "6. Estacionamientos, acceso y horario para camión de reparto.",
        "7. ¿El uso de suelo permite supermercado y venta de licor? ¿Hay exclusividad de otro inquilino?",
        "8. ¿Tiene inspección o certificación estructural posterior al sismo del 9 de octubre de 2026?",
        "9. ¿Qué otros negocios hay en la plaza y qué supermercado queda más cerca?",
        "",
    ]
    for p, titulo in titulos.items():
        grupo = [r for r in filas if r["prioridad"] == p]
        if not grupo:
            continue
        salida += [f"## {titulo}", ""]
        for i, r in enumerate(grupo, 1):
            r["codigo"] = f"{p}{i}"
            if p == "D":
                salida.append(f"- {r.get('zona') or 'Zona n/d'} — {r.get('titulo') or 'Sin título'}: "
                              f"{r['descarte']}. <{r.get('url')}>")
            else:
                salida += [ficha(r["codigo"], r), ""]
        salida.append("")

    base = origen.parent.parent / f"Locales para llamar {fecha}"
    base.with_suffix(".md").write_text("\n".join(salida).rstrip() + "\n", encoding="utf-8")

    columnas = ["codigo", "prioridad", "puntos", "nuevo", "zona", "ola", "titulo", "tipo", "area_m2",
                "precio_mensual_usd", "usd_por_m2", "planta", "ubicacion", "anunciante", "telefono",
                "url", "confirmar", "notas", "llamado", "resultado"]
    with base.with_suffix(".csv").open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=columnas, extrasaction="ignore")
        w.writeheader()
        for r in filas:
            w.writerow({**r, "area_m2": f"{r['area']:g}" if r["area"] else "",
                        "precio_mensual_usd": f"{r['precio']:g}" if r["precio"] else "",
                        "usd_por_m2": r["por_m2"] or "", "nuevo": "sí" if r["nuevo"] else "",
                        "confirmar": "; ".join(r["confirmar"]) or r["descarte"] or "",
                        "llamado": "", "resultado": ""})

    print(f"{len(filas)} anuncios -> A:{conteo['A']} B:{conteo['B']} C:{conteo['C']} descartados:{conteo['D']}")
    print(base.with_suffix(".md"))
    print(base.with_suffix(".csv"))


if __name__ == "__main__":
    main()
