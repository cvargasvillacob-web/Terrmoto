"""Genera las propuestas de logo «20 años» de Pacífica Inmobiliaria.

Parte del edificio plateado del logo original, ya trazado como vector
(marca_edificio.json, ver trazar_marca.py), y compone tres versiones:

  1. clasico-20  : el logo de siempre con volumen y un medallón de 20 años
  2. sello-20    : sello circular de aniversario
  3. horizontal-20 (claro y oscuro): para la cabecera de la web y firmas

Todo el texto se convierte a trazos, así que los SVG se ven igual en
cualquier computadora sin instalar fuentes. Los PNG salen al doble de tamaño.

Uso: python3 sitio/marca/generar_logos.py   (requiere fonttools y node con playwright)
"""
import json
import math
import subprocess
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

AQUI = Path(__file__).resolve().parent
SALIDA = AQUI / "logos"
FUENTES = Path("/usr/share/fonts/truetype/liberation")

AZUL = "#203e98"      # fondo del logo original
AZUL_OSC = "#122766"
AZUL_CLARO = "#3460d0"
VENTANA = "#0d4598"

MARCA = json.loads((AQUI / "marca_edificio.json").read_text())


class Fuente:
    def __init__(self, archivo):
        self.f = TTFont(FUENTES / archivo)
        self.glifos = self.f.getGlyphSet()
        self.cmap = self.f.getBestCmap()
        self.upm = self.f["head"].unitsPerEm

    def _g(self, ch):
        return self.cmap[ord(ch)]

    def ancho(self, texto, tam, tracking=0.0):
        nat = sum(self.glifos[self._g(c)].width for c in texto) * tam / self.upm
        return nat + tracking * tam * (len(texto) - 1)

    def tracking_para(self, texto, tam, ancho_meta):
        nat = self.ancho(texto, tam)
        return (ancho_meta - nat) / (tam * (len(texto) - 1))

    def texto(self, texto, tam, x, y, tracking=0.0, anclaje="start"):
        w = self.ancho(texto, tam, tracking)
        x -= {"start": 0, "middle": w / 2, "end": w}[anclaje]
        esc = tam / self.upm
        pen = SVGPathPen(self.glifos)
        for c in texto:
            g = self._g(c)
            self.glifos[g].draw(TransformPen(pen, (esc, 0, 0, -esc, x, y)))
            x += self.glifos[g].width * esc + tracking * tam
        return pen.getCommands()

    def arco(self, texto, tam, cx, cy, r, tracking=0.0, abajo=False):
        """Texto sobre un círculo: arriba se lee en sentido horario, abajo al derecho."""
        esc = tam / self.upm
        total = self.ancho(texto, tam, tracking) / r
        pen = SVGPathPen(self.glifos)
        s = 0.0
        for c in texto:
            g = self._g(c)
            adv = self.glifos[g].width * esc
            medio = (s + adv / 2) / r
            if abajo:
                phi = math.pi / 2 + total / 2 - medio
                th = phi - math.pi / 2
            else:
                phi = -math.pi / 2 - total / 2 + medio
                th = phi + math.pi / 2
            px, py = cx + r * math.cos(phi), cy + r * math.sin(phi)
            co, si = math.cos(th), math.sin(th)
            m = (co * esc, si * esc, si * esc, -co * esc, px - co * adv / 2, py - si * adv / 2)
            self.glifos[g].draw(TransformPen(pen, m))
            s += adv + tracking * tam
        return pen.getCommands()


SANS = Fuente("LiberationSans-Bold.ttf")
SERIF = Fuente("LiberationSerif-Bold.ttf")


DEFS = f"""<defs>
  <linearGradient id="plata" x1="0" x2="1" y1="0" y2="0">
    <stop offset="0" stop-color="#4c4d51"/><stop offset=".2" stop-color="#8e9095"/>
    <stop offset=".42" stop-color="#d3d5d9"/><stop offset=".6" stop-color="#f7f8f9"/>
    <stop offset=".82" stop-color="#c8cace"/><stop offset="1" stop-color="#696a6e"/>
  </linearGradient>
  <linearGradient id="brillo" x1="0" x2="0" y1="0" y2="1">
    <stop offset="0" stop-color="#fff" stop-opacity=".55"/><stop offset=".45" stop-color="#fff" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="cromo" x1="0" x2="0" y1="0" y2="1">
    <stop offset="0" stop-color="#ffffff"/><stop offset=".46" stop-color="#e3e6eb"/>
    <stop offset=".5" stop-color="#9ea3ad"/><stop offset=".62" stop-color="#cfd3d9"/>
    <stop offset="1" stop-color="#f4f5f7"/>
  </linearGradient>
  <linearGradient id="cromo-azul" x1="0" x2="0" y1="0" y2="1">
    <stop offset="0" stop-color="{AZUL_CLARO}"/><stop offset=".48" stop-color="{AZUL}"/>
    <stop offset=".52" stop-color="{AZUL_OSC}"/><stop offset="1" stop-color="{AZUL}"/>
  </linearGradient>
  <linearGradient id="aro" x1="0" x2="1" y1="0" y2="1">
    <stop offset="0" stop-color="#f7f8f9"/><stop offset=".3" stop-color="#8e9095"/>
    <stop offset=".55" stop-color="#e9eaec"/><stop offset=".8" stop-color="#6d6e72"/>
    <stop offset="1" stop-color="#d3d5d9"/>
  </linearGradient>
  <radialGradient id="fondo" cx=".42" cy=".34" r=".85">
    <stop offset="0" stop-color="{AZUL_CLARO}"/><stop offset=".5" stop-color="{AZUL}"/>
    <stop offset="1" stop-color="{AZUL_OSC}"/>
  </radialGradient>
  <linearGradient id="barra" x1="0" x2="0" y1="0" y2="1">
    <stop offset="0" stop-color="#e3e5e8"/><stop offset=".5" stop-color="#8e9095"/><stop offset="1" stop-color="#5c5d61"/>
  </linearGradient>
  <filter id="sombra" x="-20%" y="-20%" width="140%" height="150%">
    <feDropShadow dx="0" dy="14" stdDeviation="14" flood-color="#06103a" flood-opacity=".6"/>
  </filter>
  <filter id="sombra-suave" x="-10%" y="-10%" width="120%" height="140%">
    <feDropShadow dx="0" dy="4" stdDeviation="5" flood-color="#06103a" flood-opacity=".45"/>
  </filter>
</defs>"""


def marca(x, y, ancho, ventanas=True, sombra="sombra"):
    """El edificio plateado con sombra y un reflejo arriba, escalado a `ancho`."""
    esc = ancho / MARCA["w"]
    d = MARCA["d"]
    return f"""<g transform="translate({x:.1f},{y:.1f}) scale({esc:.4f})">
  <path d="{d}" fill="url(#plata)" fill-rule="evenodd" filter="url(#{sombra})"/>
  <path d="{d}" fill="url(#brillo)" fill-rule="evenodd"/>
</g>"""


def alto_marca(ancho):
    return MARCA["h"] * ancho / MARCA["w"]


def svg(w, h, cuerpo):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">\n'
            f"{DEFS}\n{cuerpo}\n</svg>\n")


def medallon(cx, cy, r):
    """Medallón «20 años»: aro plateado, centro azul, 20 en cromo."""
    veinte = SERIF.texto("20", r * 0.98, cx, cy + r * 0.26, tracking=-0.02, anclaje="middle")
    anos = SANS.texto("AÑOS", r * 0.25, cx, cy + r * 0.62, tracking=0.32, anclaje="middle")
    return f"""<g filter="url(#sombra-suave)">
  <circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#aro)"/>
  <circle cx="{cx}" cy="{cy}" r="{r * 0.87:.1f}" fill="url(#fondo)"/>
  <circle cx="{cx}" cy="{cy}" r="{r * 0.8:.1f}" fill="none" stroke="#fff" stroke-opacity=".35" stroke-width="{r * 0.015:.1f}"/>
</g>
<path d="{veinte}" fill="url(#cromo)"/>
<path d="{anos}" fill="#fff"/>"""


def clasico_20():
    W, H = 1240, 1000
    ancho_m = 690
    xm, ym = (W - ancho_m) / 2 - 20, 70
    pac = SANS.texto("PACIFICA", 128, W / 2, 868, tracking=SANS.tracking_para("PACIFICA", 128, W - 80), anclaje="middle")
    inm = SERIF.texto("INMOBILIARIA", 98, W / 2, 970, tracking=SERIF.tracking_para("INMOBILIARIA", 98, W - 90), anclaje="middle")
    cuerpo = f"""<rect width="{W}" height="760" fill="url(#fondo)"/>
<rect y="0" width="{W}" height="760" fill="url(#brillo)" opacity=".25"/>
{marca(xm, ym, ancho_m)}
{medallon(1075, 165, 125)}
<rect y="760" width="{W}" height="122" fill="#fff"/>
<path d="{pac}" fill="{AZUL}"/>
<rect y="882" width="{W}" height="104" fill="{AZUL}"/>
<path d="{inm}" fill="#fff" filter="url(#sombra-suave)"/>
<rect y="986" width="{W}" height="14" fill="url(#barra)"/>"""
    return W, H, cuerpo


def sello_20():
    W = H = 1000
    c = 500
    arriba = SANS.arco("PACIFICA INMOBILIARIA", 56, c, c, 410, tracking=0.1)
    abajo = SANS.arco("PANAMÁ", 50, c, c, 440, tracking=0.5, abajo=True)
    ancho_m = 430
    veinte = SERIF.texto("20", 250, c, 735, tracking=-0.03, anclaje="middle")
    anos = SANS.texto("AÑOS", 58, c, 815, tracking=0.42, anclaje="middle")
    puntos = "".join(
        f'<circle cx="{c + 440 * math.cos(a):.1f}" cy="{c + 440 * math.sin(a):.1f}" r="7" fill="#fff" fill-opacity=".8"/>'
        for a in (math.radians(90 - 33), math.radians(90 + 33)))
    cuerpo = f"""<g filter="url(#sombra-suave)">
  <circle cx="{c}" cy="{c}" r="490" fill="url(#aro)"/>
  <circle cx="{c}" cy="{c}" r="468" fill="url(#fondo)"/>
</g>
<circle cx="{c}" cy="{c}" r="468" fill="url(#brillo)" opacity=".3"/>
<circle cx="{c}" cy="{c}" r="352" fill="none" stroke="#fff" stroke-opacity=".3" stroke-width="3"/>
<path d="{arriba}" fill="#fff"/>
<path d="{abajo}" fill="#fff" fill-opacity=".85"/>
{puntos}
{marca(c - ancho_m / 2, 205, ancho_m)}
<path d="{veinte}" fill="url(#cromo)" filter="url(#sombra-suave)"/>
<path d="{anos}" fill="#fff"/>"""
    return W, H, cuerpo


def horizontal_20(oscuro=False, con_fondo=True):
    """oscuro: letras blancas para fondos azules; con_fondo=False lo deja transparente."""
    W, H = 1600, 400
    lado = 330
    y0 = (H - lado) / 2
    ancho_m = lado * 0.8
    caja = f"""<g filter="url(#sombra-suave)"><rect x="35" y="{y0}" width="{lado}" height="{lado}" rx="46" fill="url(#fondo)"/></g>
<rect x="35" y="{y0}" width="{lado}" height="{lado}" rx="46" fill="url(#brillo)" opacity=".3"/>
{marca(35 + (lado - ancho_m) / 2, y0 + (lado - alto_marca(ancho_m)) / 2 - 4, ancho_m, sombra="sombra-suave")}"""
    x_txt = 35 + lado + 50
    ancho_txt = 760
    pac = SANS.texto("PACIFICA", 132, x_txt, 205, tracking=SANS.tracking_para("PACIFICA", 132, ancho_txt))
    inm = SERIF.texto("INMOBILIARIA", 76, x_txt, 312, tracking=SERIF.tracking_para("INMOBILIARIA", 76, ancho_txt))
    x_div = x_txt + ancho_txt + 55
    x_20 = x_div + 55
    veinte = SERIF.texto("20", 230, x_20, 262, tracking=-0.03)
    w20 = SERIF.ancho("20", 230, -0.03)
    anos = SANS.texto("AÑOS", 52, x_20 + w20 / 2, 330, tracking=SANS.tracking_para("AÑOS", 52, w20) , anclaje="middle")
    tinta = "#fff" if oscuro else AZUL
    inm_color = "#d9dde6" if oscuro else "#5b5d63"
    fondo = f'<rect width="{W}" height="{H}" fill="url(#fondo)"/>' if oscuro and con_fondo else ""
    cuerpo = f"""{fondo}
{caja}
<path d="{pac}" fill="{tinta}"/>
<path d="{inm}" fill="{inm_color}"/>
<rect x="{x_div}" y="70" width="5" height="260" rx="2" fill="url(#aro)"/>
<path d="{veinte}" fill="url(#{'cromo' if oscuro else 'cromo-azul'})"/>
<path d="{anos}" fill="{tinta}"/>"""
    return W, H, cuerpo


PIN_DEFS = f"""<defs>
  <radialGradient id="pin-cuerpo" cx=".34" cy=".26" r=".9">
    <stop offset="0" stop-color="#6f97f5"/><stop offset=".28" stop-color="{AZUL_CLARO}"/>
    <stop offset=".62" stop-color="{AZUL}"/><stop offset="1" stop-color="#0b1a52"/>
  </radialGradient>
  <linearGradient id="pin-reflejo" x1="0" x2="1" y1="0" y2="1">
    <stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".7" stop-color="#8fb0ff" stop-opacity="0"/>
    <stop offset="1" stop-color="#8fb0ff" stop-opacity=".55"/>
  </linearGradient>
  <linearGradient id="pin-lado" x1="0" x2="1" y1="0" y2="0">
    <stop offset="0" stop-color="#9fbaff" stop-opacity=".35"/><stop offset=".12" stop-color="#9fbaff" stop-opacity="0"/>
    <stop offset=".55" stop-color="#050d30" stop-opacity="0"/><stop offset="1" stop-color="#050d30" stop-opacity=".45"/>
  </linearGradient>
  <radialGradient id="pin-brillo" cx=".5" cy=".5" r=".5">
    <stop offset="0" stop-color="#fff" stop-opacity=".85"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="pin-hueco" cx=".5" cy=".38" r=".7">
    <stop offset="0" stop-color="{AZUL_CLARO}"/><stop offset=".6" stop-color="{AZUL}"/><stop offset="1" stop-color="{AZUL_OSC}"/>
  </radialGradient>
  <radialGradient id="pin-suelo" cx=".5" cy=".5" r=".5">
    <stop offset="0" stop-color="#0b1a52" stop-opacity=".45"/><stop offset="1" stop-color="#0b1a52" stop-opacity="0"/>
  </radialGradient>
  <filter id="pin-interior" x="-10%" y="-10%" width="120%" height="120%">
    <feOffset dy="6"/><feGaussianBlur stdDeviation="7" result="b"/>
    <feComposite in="SourceAlpha" in2="b" operator="arithmetic" k2="-1" k3="1" result="borde"/>
    <feFlood flood-color="#050d30" flood-opacity=".7"/><feComposite in2="borde" operator="in"/>
    <feComposite in2="SourceGraphic" operator="over"/>
  </filter>
</defs>"""


def pin_3d():
    """Pin de ubicación propio: gota azul con volumen, aro plateado y el edificio de Pacífica adentro."""
    W, H = 400, 520
    cx, cy, r = 200, 190, 160
    gota = (f"M{cx},470 C{cx - 52},392 {cx - r},300 {cx - r},{cy} "
            f"A{r},{r} 0 1 1 {cx + r},{cy} C{cx + r},300 {cx + 52},392 {cx},470 Z")
    ancho_m = 166
    cuerpo = f"""<ellipse cx="{cx}" cy="488" rx="96" ry="20" fill="url(#pin-suelo)"/>
<path d="{gota}" fill="url(#pin-cuerpo)"/>
<path d="{gota}" fill="url(#pin-lado)"/>
<path d="{gota}" fill="url(#pin-reflejo)"/>
<ellipse cx="128" cy="98" rx="62" ry="30" transform="rotate(-38 128 98)" fill="url(#pin-brillo)" opacity=".75"/>
<circle cx="{cx}" cy="{cy}" r="104" fill="url(#aro)"/>
<circle cx="{cx}" cy="{cy}" r="92" fill="url(#pin-hueco)" filter="url(#pin-interior)"/>
{marca(cx - ancho_m / 2 - 3, cy - alto_marca(ancho_m) / 2 + 2, ancho_m, sombra="sombra-suave")}
<ellipse cx="{cx - 30}" cy="{cy - 62}" rx="44" ry="14" transform="rotate(-20 {cx - 30} {cy - 62})" fill="#fff" opacity=".18"/>"""
    defs = DEFS.replace("</defs>", PIN_DEFS.replace("<defs>", ""))
    return W, H, f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n{defs}\n{cuerpo}\n</svg>\n'


def renderizar(svg_path, png_path, w, h):
    js = """const { chromium } = require('playwright');
(async () => { const [src, out, w, h] = process.argv.slice(-4);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: +w, height: +h }, deviceScaleFactor: 2 });
  await p.goto('file://' + src); await p.screenshot({ path: out, omitBackground: true }); await b.close(); })();"""
    subprocess.run(["node", "-e", js, "--", str(svg_path), str(png_path), str(w), str(h)], check=True)


def main():
    SALIDA.mkdir(exist_ok=True)
    piezas = {
        "pacifica-clasico-20-anos": clasico_20(),
        "pacifica-sello-20-anos": sello_20(),
        "pacifica-horizontal-20-anos": horizontal_20(),
        "pacifica-horizontal-20-anos-oscuro": horizontal_20(oscuro=True),
        "pacifica-horizontal-20-anos-blanco": horizontal_20(oscuro=True, con_fondo=False),
    }
    for nombre, (w, h, cuerpo) in piezas.items():
        ruta = SALIDA / f"{nombre}.svg"
        ruta.write_text(svg(w, h, cuerpo))
        renderizar(ruta, SALIDA / f"{nombre}.png", w, h)
        print("ok", nombre)
    # La marca sola, para favicon y redes
    lado = 1000
    am = 820
    ruta = SALIDA / "pacifica-marca.svg"
    ruta.write_text(svg(lado, lado, f'<rect width="{lado}" height="{lado}" rx="160" fill="url(#fondo)"/>\n'
                                      f'<rect width="{lado}" height="{lado}" rx="160" fill="url(#brillo)" opacity=".3"/>\n'
                                      f'{marca((lado - am) / 2, (lado - alto_marca(am)) / 2, am)}'))
    renderizar(ruta, SALIDA / "pacifica-marca.png", lado, lado)
    print("ok marca")
    w, h, contenido = pin_3d()
    ruta = SALIDA / "pacifica-pin.svg"
    ruta.write_text(contenido)
    renderizar(ruta, SALIDA / "pacifica-pin.png", w, h)
    print("ok pin")


if __name__ == "__main__":
    main()
