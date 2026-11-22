#!/usr/bin/env python3
"""Arma el portal privado de proyectos (proyectos.pacificainmobiliaria.com).

Uso: python3 sitio/construir.py

Escribe sitio/salida/proyectos/ y el paquete sitio/salida/proyectos.zip, listo para
subir al subdominio y proteger con clave desde el panel del hosting. Cada proyecto
lleva su mapa interactivo y sus documentos más recientes, convertidos a páginas.
Requiere: pip install markdown
"""
import collections
import datetime as dt
import html
import json
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

import markdown

AQUI = Path(__file__).resolve().parent
REPO = AQUI.parent
SALIDA = AQUI / "salida"
PORTAL = SALIDA / "proyectos"
PANAMA = dt.timezone(dt.timedelta(hours=-5))
MESES = "enero febrero marzo abril mayo junio julio agosto septiembre octubre noviembre diciembre".split()


def fecha_larga(d):
    return f"{d.day} de {MESES[d.month - 1]} de {d.year}"


def ultimo(carpeta, patron):
    archivos = sorted(carpeta.glob(patron))
    return archivos[-1] if archivos else None


def md_a_html(texto):
    cuerpo = markdown.markdown(texto, extensions=["tables", "sane_lists"])
    cuerpo = cuerpo.replace("<table>", '<div class="tabla"><table>').replace("</table>", "</table></div>")
    # Enlaces externos en pestaña nueva
    return re.sub(r'<a href="(https?://[^"]+)"', r'<a href="\1" target="_blank" rel="noopener"', cuerpo)


def pagina(titulo, cuerpo, fecha):
    plantilla = (AQUI / "plantillas" / "documento.html").read_text(encoding="utf-8")
    return (plantilla.replace("{{TITULO}}", html.escape(titulo))
            .replace("{{CUERPO}}", cuerpo).replace("{{FECHA}}", fecha))


def vista_mapa(metro, locales):
    """Miniatura del mapa: líneas de Metro y locales de prioridad A, proyectados a la caja."""
    puntos = [(s["lon"], s["lat"]) for s in metro] + [(l["lon"], l["lat"]) for l in locales if l.get("lat")]
    lon0, lon1 = min(p[0] for p in puntos) - 0.02, max(p[0] for p in puntos) + 0.02
    lat0, lat1 = min(p[1] for p in puntos) - 0.02, max(p[1] for p in puntos) + 0.02
    W, H = 600, 300

    def xy(lon, lat):
        return (lon - lon0) / (lon1 - lon0) * W, (lat1 - lat) / (lat1 - lat0) * H

    lineas = ""
    for linea in ("L1", "L2"):
        pts = " ".join("%.1f,%.1f" % xy(s["lon"], s["lat"]) for s in metro if s["linea"] == linea)
        lineas += f'<polyline points="{pts}" fill="none" stroke="#fff" stroke-opacity=".75" stroke-width="3" stroke-linejoin="round"/>'
    estaciones = "".join('<circle cx="%.1f" cy="%.1f" r="2.6" fill="#fff"/>' % xy(s["lon"], s["lat"]) for s in metro)
    color = {"A": "#f08a3c", "B": "#ffd27a"}
    marcas = "".join(
        '<circle cx="%.1f" cy="%.1f" r="%s" fill="%s" stroke="#122766" stroke-width="1.5"/>'
        % (*xy(l["lon"], l["lat"]), 6 if l["prioridad"] == "A" else 3.5, color[l["prioridad"]])
        for l in sorted(locales, key=lambda l: l["prioridad"], reverse=True)
        if l.get("lat") and l["prioridad"] in color)
    return (f'<svg viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice" aria-hidden="true">'
            f"{lineas}{estaciones}{marcas}</svg>")


def proyecto_supermercados(fecha):
    """Proyecto Lativium: locales de ~250 m² para supermercados de proximidad."""
    carpeta = PORTAL / "supermercados"
    subprocess.run([sys.executable, str(REPO / "locales" / "mapa" / "construir.py")], check=True)
    shutil.copytree(REPO / "locales" / "mapa" / "publicar", carpeta / "mapa", dirs_exist_ok=True)

    datos = carpeta / "mapa" / "datos"
    locales = json.loads((datos / "locales.json").read_text(encoding="utf-8"))
    metro = json.loads((datos / "metro.json").read_text(encoding="utf-8"))
    cuenta = collections.Counter(l["prioridad"] for l in locales)

    docs = []
    lista = ultimo(REPO / "locales", "Locales para llamar *.md")
    if lista:
        (carpeta / "llamadas.html").write_text(
            pagina("Locales para llamar", md_a_html(lista.read_text(encoding="utf-8")), fecha), encoding="utf-8")
        cifras = "".join(f"<i>{p}: {cuenta.get(p, 0)}</i>" for p in "ABCD")
        docs.append(("llamadas.html", "Locales para llamar",
                     "Todos los anuncios por prioridad, con las preguntas para cada llamada.", cifras))
    reporte = ultimo(REPO / "locales" / "reportes", "Reporte *.txt")
    if reporte:
        cuerpo = f'<h1>Reporte del día</h1><pre class="reporte">{html.escape(reporte.read_text(encoding="utf-8"))}</pre>'
        (carpeta / "reporte.html").write_text(pagina("Reporte del día", cuerpo, fecha), encoding="utf-8")
        docs.append(("reporte.html", "Reporte del día", "El resumen que se envía cada mañana al grupo.", ""))
    pistas = REPO / "locales" / "pistas.md"
    if pistas.exists():
        (carpeta / "pistas.html").write_text(
            pagina("Pistas de campo", md_a_html(pistas.read_text(encoding="utf-8")), fecha), encoding="utf-8")
        docs.append(("pistas.html", "Pistas de campo",
                     "Antiguos Justo & Bueno, plazas nuevas y oportunidades para visitar.", ""))
    informe = REPO / "reports" / "Penetración supermercados 250 m2 Panamá.md"
    if informe.exists():
        (carpeta / "informe.html").write_text(
            pagina("Informe de mercado", md_a_html(informe.read_text(encoding="utf-8")), fecha), encoding="utf-8")
        docs.append(("informe.html", "Informe de mercado",
                     "Penetración de supermercados de 250 m²: formato, zonas y ubicación.", ""))

    tarjetas = "".join(
        f'<a class="doc" href="supermercados/{href}"><b>{titulo}</b><span>{desc}</span>'
        f'{f"<div class=cifras>{cifras}</div>" if cifras else ""}</a>'
        for href, titulo, desc, cifras in docs)
    return f"""<section class="proyecto">
  <h1>Locales para supermercados de proximidad (250 m²)</h1>
  <p class="meta">Proyecto Lativium · {len(locales)} anuncios revisados · {cuenta.get('A', 0)} de prioridad A</p>
  <a class="mapa" href="supermercados/mapa/">
    <div class="vista">{vista_mapa(metro, locales)}</div>
    <div class="txt">
      <h2>Mapa interactivo</h2>
      <p>Población por corregimiento, Metro, locales por prioridad, recorrido sugerido y plan de llamadas.</p>
      <span class="boton">Abrir el mapa</span>
    </div>
  </a>
  <div class="docs">{tarjetas}</div>
</section>"""


def main():
    if PORTAL.exists():
        shutil.rmtree(PORTAL)
    (PORTAL / "marca").mkdir(parents=True)
    for nombre in ("pacifica-horizontal-20-anos-blanco.svg", "pacifica-marca.svg"):
        shutil.copy(AQUI / "marca" / "logos" / nombre, PORTAL / "marca" / nombre)

    ahora = dt.datetime.now(PANAMA)
    fecha = fecha_larga(ahora)
    proyectos = [proyecto_supermercados(fecha)]

    portada = (AQUI / "plantillas" / "portal.html").read_text(encoding="utf-8")
    (PORTAL / "index.html").write_text(
        portada.replace("{{PROYECTOS}}", "\n".join(proyectos)).replace("{{FECHA}}", fecha), encoding="utf-8")
    (PORTAL / "robots.txt").write_text("User-agent: *\nDisallow: /\n", encoding="utf-8")

    paquete = SALIDA / "proyectos.zip"
    with zipfile.ZipFile(paquete, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(PORTAL.rglob("*")):
            if f.is_file():
                z.write(f, f.relative_to(PORTAL))
    print("Portal listo en", PORTAL.relative_to(REPO), "y", paquete.relative_to(REPO),
          f"({paquete.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
