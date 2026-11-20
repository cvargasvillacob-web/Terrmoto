#!/usr/bin/env python3
"""Mantiene la base de anuncios del buscador de locales y arma la lista de llamadas.

Uso:
    python3 locales/armar_lista.py                   # regenera la lista y el reporte del día
    python3 locales/armar_lista.py hallazgos.json    # agrega hallazgos nuevos y regenera
    python3 locales/armar_lista.py --turno           # dice qué grupo de zonas toca en esta corrida

La base acumulada está en locales/datos/anuncios.json. Cada anuncio guarda cuándo
se vio por primera y por última vez. A partir de ella se escriben:
    locales/Locales para llamar AAAA-MM-DD.md    (para leer y llamar)
    locales/Locales para llamar AAAA-MM-DD.csv   (para llevar el seguimiento)
    locales/reportes/Reporte AAAA-MM-DD.txt      (texto para WhatsApp)
    locales/reportes/Enlace WhatsApp AAAA-MM-DD.txt  (enlace que abre WhatsApp con un
                                                  resumen ya escrito; el grupo se elige a mano)

Un anuncio se marca NUEVO durante las 24 horas siguientes a la primera vez que
se vio. Las fechas usan la hora de Panamá. Solo usa la biblioteca estándar.
"""
import csv
import json
import re
import sys
import unicodedata
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import quote

PANAMA = timezone(timedelta(hours=-5))   # Panamá no cambia de hora
CARPETA = Path(__file__).resolve().parent
BASE_DATOS = CARPETA / "datos" / "anuncios.json"
TURNO = CARPETA / "datos" / "turno.json"
# Mapa interactivo de locales; el resumen para WhatsApp lo enlaza para mandar un solo mensaje al grupo
MAPA_URL = "https://claude.ai/artifact/YXzGaM6k8gaTgC1sfAazKk"
MESES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]

# Grupos de zonas: las corridas se turnan entre ellos, uno por corrida.
GRUPOS = [
    ("Este", "Tocumen (Nuevo Tocumen, Altos de Tocumen), 24 de Diciembre (La Doña, Felipillo), Pacora y "
             "Las Mañanitas; oportunista: Juan Díaz y Pedregal"),
    ("Norte y San Miguelito", "Ernesto Córdoba Campos (Villa Zaita, Gonzalillo), Las Cumbres y Alcalde Díaz "
                              "(Milla 8); oportunista: alrededores de las estaciones San Miguelito y Los Andes, "
                              "Villa Lucre y Brisas del Golf"),
    ("Oeste", "barrios interiores de La Chorrera (Barrio Colón, Barrio Balboa, El Coco, Guadalupe) y Arraiján "
              "(Vista Alegre, Nuevo Arraiján, Juan D. Arosemena, Burunga, Cerro Silvestre, Vacamonte)"),
]

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

    if planta == "varios niveles":
        # el área anunciada suma varias plantas: no se sabe si la planta baja alcanza
        faltan_datos = True
        confirmar.append("cuánto mide la planta baja sola")
    elif planta in ("", "n/d"):
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


TITULOS = {
    "A": "Prioridad A: cumplen área y alquiler, llamar primero",
    "B": "Prioridad B: faltan datos o el área queda cerca del rango",
    "C": "Prioridad C: incumplen algo negociable (alquiler o tamaño)",
    "D": "Descartados (no cumplen)",
}


def fusionar(base, hallazgos, ahora):
    """Agrega los hallazgos a la base. Devuelve la base actualizada y cuántos eran nuevos."""
    marca = ahora.isoformat(timespec="minutes")
    indice = {clave(x): x for x in base}
    nuevos = 0
    for h in hallazgos:
        if not h.get("url"):
            continue  # sin enlace no se puede comprobar ni llamar
        k = clave(h)
        previo = indice.get(k)
        if previo is None:
            indice[k] = {**h, "primera_vez": marca, "ultima_vez": marca}
            nuevos += 1
        else:
            for campo, valor in h.items():
                if valor not in (None, "") and campo not in ("primera_vez", "ultima_vez"):
                    previo[campo] = valor
            previo["ultima_vez"] = marca
    return list(indice.values()), nuevos


def es_nuevo(item, ahora):
    try:
        return ahora - datetime.fromisoformat(item["primera_vez"]) < timedelta(hours=24)
    except (KeyError, TypeError, ValueError):
        return False


def linea_corta(r, largo=70):
    titulo = (r.get("titulo") or "Sin título").strip()
    if len(titulo) > largo:
        titulo = titulo[:largo - 1].rstrip() + "…"
    datos = " · ".join(x for x in [
        f"{r['area']:g} m²" if r["area"] else None,
        f"{dinero(r['precio'])}/mes" if r["precio"] else None,
        f"US${r['por_m2']:g}/m²" if r["por_m2"] else None,
    ] if x) or "datos por confirmar"
    return f"{r.get('zona') or 'Zona n/d'} — {titulo}\n   {datos}" + (" · NUEVO" if r["nuevo"] else "")


def reporte_whatsapp(filas, conteo, ahora):
    """Texto corto con el formato de WhatsApp (*negrita*, _cursiva_)."""
    activos = [r for r in filas if r["prioridad"] != "D"]
    nuevos = [r for r in activos if r["nuevo"]]
    t = [
        "*Locales para supermercado de 250 m²*",
        f"Reporte del {ahora.day} {MESES[ahora.month - 1]} {ahora.year}",
        "",
        f"En seguimiento: {len(activos)} anuncios ({conteo['A']} A · {conteo['B']} B · {conteo['C']} C)",
        f"Nuevos en las últimas 24 horas: {len(nuevos)}",
    ]
    grupo_a = [r for r in filas if r["prioridad"] == "A"]
    if grupo_a:
        t += ["", f"*Prioridad A: llamar primero ({len(grupo_a)})*"]
        for i, r in enumerate(grupo_a, 1):
            t += [f"{i}. {linea_corta(r)}", f"   {r.get('url')}"]
    otros = [r for r in nuevos if r["prioridad"] in ("B", "C")]
    if otros:
        t += ["", f"*Otros nuevos, con datos por confirmar ({len(otros)})*"]
        for r in otros[:8]:
            t += [f"• {linea_corta(r)}", f"   {r.get('url')}"]
        if len(otros) > 8:
            t.append(f"…y {len(otros) - 8} más en la lista completa.")
    t += ["", "_Datos tomados del buscador web: confirmar área, precio y vigencia al llamar._"]
    return "\n".join(t) + "\n"


def resumen_corto(filas, conteo, ahora, maximo=5):
    """Versión breve del reporte, pensada para caber en un enlace de WhatsApp."""
    activos = [r for r in filas if r["prioridad"] != "D"]
    nuevos = sum(1 for r in activos if r["nuevo"])
    t = [
        "*Locales para supermercado de 250 m²*",
        f"Resumen del {ahora.day} {MESES[ahora.month - 1]} {ahora.year}",
        "",
        f"En seguimiento: {len(activos)} anuncios ({conteo['A']} A · {conteo['B']} B · {conteo['C']} C). "
        f"Nuevos en 24 horas: {nuevos}.",
    ]
    primeros = [r for r in filas if r["prioridad"] == "A"][:maximo]
    if primeros:
        t += ["", "*Primeros de la lista*"]
        for i, r in enumerate(primeros, 1):
            datos = f"{r['area']:g} m² · {dinero(r['precio'])}/mes (US${r['por_m2']:g}/m²)"
            t += [f"{i}. {r.get('zona') or 'Zona n/d'}: {datos}", str(r.get("url"))]
    t += ["", f"*Mapa con todos los locales y el plan de recorrido:* {MAPA_URL}",
          "", "_Datos del buscador web: confirmar área, precio y vigencia al llamar._"]
    return "\n".join(t)


def enlace_whatsapp(texto):
    """Enlace que abre WhatsApp con el texto escrito; la persona elige el chat o grupo y envía."""
    return "https://wa.me/?text=" + quote(texto)


def generar(base, ahora):
    """Puntúa la base y escribe la lista (Markdown y CSV) y el reporte del día."""
    fecha = ahora.date().isoformat()
    filas = []
    for item in base:
        r = evaluar(item)
        r["nuevo"] = es_nuevo(item, ahora)
        filas.append(r)
    filas.sort(key=lambda r: (r["prioridad"], -r["puntos"], r["ola"], r["por_m2"] or 999))
    conteo = {p: sum(r["prioridad"] == p for r in filas) for p in TITULOS}

    salida = [
        f"# Locales para llamar — {fecha}",
        "",
        f"{len(filas)} anuncios revisados: {conteo['A']} de prioridad A, {conteo['B']} de prioridad B, "
        f"{conteo['C']} de prioridad C y {conteo['D']} descartados. "
        f"Actualizado el {ahora.day} {MESES[ahora.month - 1]} a las {ahora:%H:%M} (hora de Panamá).",
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
    for p, titulo in TITULOS.items():
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

    lista = CARPETA / f"Locales para llamar {fecha}"
    lista.with_suffix(".md").write_text("\n".join(salida).rstrip() + "\n", encoding="utf-8")

    columnas = ["codigo", "prioridad", "puntos", "nuevo", "zona", "ola", "titulo", "tipo", "area_m2",
                "precio_mensual_usd", "usd_por_m2", "planta", "ubicacion", "anunciante", "telefono",
                "url", "confirmar", "notas", "primera_vez", "ultima_vez", "llamado", "resultado"]
    with lista.with_suffix(".csv").open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=columnas, extrasaction="ignore")
        w.writeheader()
        for r in filas:
            w.writerow({**r, "area_m2": f"{r['area']:g}" if r["area"] else "",
                        "precio_mensual_usd": f"{r['precio']:g}" if r["precio"] else "",
                        "usd_por_m2": r["por_m2"] or "", "nuevo": "sí" if r["nuevo"] else "",
                        "confirmar": "; ".join(r["confirmar"]) or r["descarte"] or "",
                        "llamado": "", "resultado": ""})

    reporte = CARPETA / "reportes" / f"Reporte {fecha}.txt"
    reporte.parent.mkdir(exist_ok=True)
    reporte.write_text(reporte_whatsapp(filas, conteo, ahora), encoding="utf-8")
    enlace = CARPETA / "reportes" / f"Enlace WhatsApp {fecha}.txt"
    enlace.write_text(enlace_whatsapp(resumen_corto(filas, conteo, ahora)) + "\n", encoding="utf-8")
    return filas, conteo, [lista.with_suffix(".md"), lista.with_suffix(".csv"), reporte, enlace]


def siguiente_grupo(ahora):
    """Turno rotativo entre los grupos de zonas, guardado en datos/turno.json.

    Cada corrida toma el grupo que sigue al de la corrida anterior. Si se pregunta
    otra vez en menos de dos horas, responde el mismo grupo y no avanza el turno.
    """
    nombres = [g[0] for g in GRUPOS]
    try:
        estado = json.loads(TURNO.read_text(encoding="utf-8"))
        ultimo = estado.get("ultimo")
        reciente = ahora - datetime.fromisoformat(estado["cuando"]) < timedelta(hours=2)
    except (OSError, ValueError, KeyError, TypeError, AttributeError):
        ultimo, reciente = None, False
    if ultimo in nombres and reciente:
        return GRUPOS[nombres.index(ultimo)]
    i = (nombres.index(ultimo) + 1) % len(nombres) if ultimo in nombres else 0
    TURNO.parent.mkdir(parents=True, exist_ok=True)
    TURNO.write_text(json.dumps({"ultimo": nombres[i], "cuando": ahora.isoformat(timespec="minutes")},
                                ensure_ascii=False) + "\n", encoding="utf-8")
    return GRUPOS[i]


def main():
    ahora = datetime.now(PANAMA)
    args = sys.argv[1:]
    if args == ["--turno"]:
        nombre, zonas = siguiente_grupo(ahora)
        print(f"Grupo de esta corrida ({ahora:%H:%M} en Panamá): {nombre}")
        print(f"Zonas: {zonas}")
        return
    if len(args) > 1 or (args and args[0].startswith("-")):
        sys.exit(__doc__)

    base = json.loads(BASE_DATOS.read_text(encoding="utf-8")) if BASE_DATOS.exists() else []
    agregados = 0
    if args:
        hallazgos = json.loads(Path(args[0]).read_text(encoding="utf-8"))
        if not isinstance(hallazgos, list):
            sys.exit("El archivo de hallazgos debe ser un arreglo JSON de anuncios.")
        base, agregados = fusionar(base, hallazgos, ahora)
        BASE_DATOS.parent.mkdir(parents=True, exist_ok=True)
        BASE_DATOS.write_text(json.dumps(base, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    filas, conteo, archivos = generar(base, ahora)
    nuevos_24h = [r for r in filas if r["nuevo"] and r["prioridad"] != "D"]
    if args:
        print(f"Hallazgos recibidos: {len(hallazgos)} · anuncios que no estaban en la base: {agregados}")
    print(f"{len(filas)} anuncios -> A:{conteo['A']} B:{conteo['B']} C:{conteo['C']} descartados:{conteo['D']}"
          f" · nuevos en 24 h: {len(nuevos_24h)}")
    for a in archivos:
        print(a.relative_to(CARPETA.parent))


if __name__ == "__main__":
    main()
