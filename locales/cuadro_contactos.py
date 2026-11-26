#!/usr/bin/env python3
"""Arma el cuadro de las mejores opciones (prioridad A) con enlaces y contactos.

Uso: python3 locales/cuadro_contactos.py

Lee los anuncios del mapa (locales/mapa/publicar/datos/locales.json, que arma
locales/mapa/construir.py) y los contactos encontrados (locales/datos/contactos.json),
y escribe en locales/reportes/:
- «Mejores opciones AAAA-MM-DD.xlsx»: cuadro completo con enlaces activos.
- «Mejores opciones AAAA-MM-DD.md»: el mismo cuadro en texto.
- «Enlace WhatsApp mejores AAAA-MM-DD.txt»: mensaje para el grupo con las opciones que
  tienen contacto o ficha directa.
"""
import datetime as dt
import json
import re
import urllib.parse
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

AQUI = Path(__file__).resolve().parent
PANAMA = dt.timezone(dt.timedelta(hours=-5))
MESES = "ene feb mar abr may jun jul ago sep oct nov dic".split()


def numero(x):
    return f"{x:,.0f}" if x and float(x).is_integer() else (f"{x:,.2f}" if x else "—")


def wa_link(tel):
    """Primer celular panameño del texto (8 dígitos que empiezan con 6) como enlace de WhatsApp."""
    if not tel:
        return None
    m = re.search(r"(?<!\d)6\d{3}-?\d{4}(?!\d)", tel)
    return f"https://wa.me/507{m.group(0).replace('-', '')}" if m else None


def opciones():
    locales = json.loads((AQUI / "mapa" / "publicar" / "datos" / "locales.json").read_text(encoding="utf-8"))
    contactos = json.loads((AQUI / "datos" / "contactos.json").read_text(encoding="utf-8"))
    a = [x for x in locales if x["prioridad"] == "A"]
    a.sort(key=lambda x: (-x["puntos"], x["por_m2"] or 99))
    filas = []
    for n, x in enumerate(a, 1):
        c = contactos.get(x["id"], {})
        directa = c.get("url_directa") or (None if x["es_listado"] else x["url"])
        filas.append({
            "n": n, "zona": x["zona"], "lugar": x.get("ubicacion") or "", "area": x["area"], "precio": x["precio"],
            "por_m2": x["por_m2"], "planta": x["planta"],
            "anunciante": c.get("anunciante") or x.get("anunciante") or "",
            "telefono": c.get("telefono") or x.get("telefono") or "",
            "whatsapp": c.get("whatsapp") or "", "correo": c.get("correo") or "",
            "enlace": directa or x["url"], "es_ficha": bool(directa),
            "vigente": {"si": "Vigente", "no": "No disponible"}.get(c.get("vigente"), "Por confirmar"),
            "confirmar": c.get("nota") or "",
        })
    return filas


def excel(filas, ruta, fecha):
    wb = Workbook()
    ws = wb.active
    ws.title = "Mejores opciones"
    cab = ["#", "Zona", "Lugar o plaza", "Área (m²)", "Alquiler (US$/mes)", "US$/m²", "Planta", "Anunciante",
           "Teléfono", "WhatsApp", "Correo", "Anuncio", "Tipo de enlace", "Vigencia", "Qué confirmar al llamar"]
    ws.append([f"Locales de prioridad A para el supermercado de 250 m² · actualizado el {fecha}"])
    ws["A1"].font = Font(bold=True, size=13)
    ws.append([])
    ws.append(cab)
    azul = PatternFill("solid", fgColor="203E98")
    for i in range(1, len(cab) + 1):
        celda = ws.cell(row=3, column=i)
        celda.font = Font(bold=True, color="FFFFFF")
        celda.fill = azul
        celda.alignment = Alignment(vertical="center", wrap_text=True)
    enlace = Font(color="2C56C8", underline="single")
    for f in filas:
        wa = wa_link(f["whatsapp"]) or wa_link(f["telefono"])
        ws.append([f["n"], f["zona"], f["lugar"], f["area"], f["precio"], f["por_m2"], f["planta"], f["anunciante"],
                   f["telefono"], "Escribir" if wa else "", f["correo"], "Abrir anuncio",
                   "Ficha del anuncio" if f["es_ficha"] else "Página de listado (buscar el local ahí)",
                   f["vigente"], f["confirmar"]])
        r = ws.max_row
        ws.cell(row=r, column=12).hyperlink = f["enlace"]
        ws.cell(row=r, column=12).font = enlace
        if wa:
            ws.cell(row=r, column=10).hyperlink = wa
            ws.cell(row=r, column=10).font = enlace
        for col in (4, 5, 6):
            ws.cell(row=r, column=col).number_format = "#,##0.00" if col == 6 else "#,##0"
        for col in range(1, len(cab) + 1):
            ws.cell(row=r, column=col).alignment = Alignment(vertical="top", wrap_text=col in (3, 8, 9, 11, 13, 15))
    anchos = [5, 16, 34, 10, 12, 9, 11, 26, 22, 11, 26, 14, 22, 14, 60]
    for i, w in enumerate(anchos, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = "C4"
    ws.auto_filter.ref = f"A3:{get_column_letter(len(cab))}{ws.max_row}"
    wb.save(ruta)


def markdown(filas, fecha):
    lineas = [f"# Mejores opciones — {fecha}", "",
              f"{len(filas)} locales de prioridad A, ordenados por puntaje y precio por m². "
              "Los datos de contacto salen de páginas públicas; confirmar al llamar.", "",
              "| # | Zona | m² | US$/mes | Anunciante | Teléfono / WhatsApp | Anuncio | Confirmar |",
              "|---|---|---|---|---|---|---|---|"]
    for f in filas:
        tel = " · ".join(t for t in (f["telefono"], f"WhatsApp {f['whatsapp']}" if f["whatsapp"] else "") if t) or "—"
        tipo = "ficha" if f["es_ficha"] else "listado"
        lineas.append(f"| {f['n']} | {f['zona']} | {numero(f['area'])} | {numero(f['precio'])} | {f['anunciante'] or '—'} | "
                      f"{tel} | [{tipo}]({f['enlace']}) | {f['confirmar'].replace('|', '/')} |")
    return "\n".join(lineas) + "\n"


def whatsapp(filas, fecha):
    elegidas = [f for f in filas if f["telefono"] or f["whatsapp"] or f["es_ficha"]][:12]
    partes = [f"*Mejores locales para el supermercado ({fecha})*", ""]
    for f in elegidas:
        contacto = " · ".join(t for t in (f["anunciante"].split(" (")[0], f["telefono"].split(" (")[0],
                                           f"WhatsApp {f['whatsapp']}" if f["whatsapp"] else "") if t)
        partes.append(f"{f['n']}. *{f['zona']}*: {numero(f['area'])} m² · US${numero(f['precio'])}/mes"
                      + (f"\n   {contacto}" if contacto else "") + f"\n   {f['enlace']}")
    partes += ["", "_Contactos tomados de páginas públicas: confirmar área, planta, precio y vigencia al llamar._"]
    return "https://wa.me/?text=" + urllib.parse.quote("\n".join(partes), safe="")


def main():
    hoy = dt.datetime.now(PANAMA)
    fecha = f"{hoy.day} {MESES[hoy.month - 1]} {hoy.year}"
    filas = opciones()
    destino = AQUI / "reportes"
    excel(filas, destino / f"Mejores opciones {hoy:%Y-%m-%d}.xlsx", fecha)
    (destino / f"Mejores opciones {hoy:%Y-%m-%d}.md").write_text(markdown(filas, fecha), encoding="utf-8")
    (destino / f"Enlace WhatsApp mejores {hoy:%Y-%m-%d}.txt").write_text(whatsapp(filas, fecha) + "\n", encoding="utf-8")
    con = sum(1 for f in filas if f["telefono"] or f["whatsapp"])
    print(f"{len(filas)} opciones A; {con} con teléfono; {sum(f['es_ficha'] for f in filas)} con ficha directa")


if __name__ == "__main__":
    main()
