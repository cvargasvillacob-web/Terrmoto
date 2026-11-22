"""Recorta el pin 3D y saca los tamaños para la web (cursor y marcador del mapa).

Uso: node renderizar.js pin && python3 pin_tamanos.py   -> sitio/marca/pin/
Imprime la punta del cursor (hotspot) para el CSS.
"""
from pathlib import Path

from PIL import Image, ImageFilter

AQUI = Path(__file__).resolve().parent
DESTINO = AQUI.parent / "pin"
DESTINO.mkdir(exist_ok=True)

im = Image.open(AQUI / "salida" / "pin-3d.png").convert("RGBA")
im = im.crop(im.getbbox())
im.save(DESTINO / "pacifica-pin-3d.png", optimize=True)


def con_borde(img, grosor):
    """Borde blanco alrededor del pin para que se vea también sobre fondos azules."""
    a = img.getchannel("A").filter(ImageFilter.MaxFilter(grosor * 2 + 1))
    base = Image.new("RGBA", img.size, (255, 255, 255, 0))
    base.putalpha(a.point(lambda v: 235 if v > 40 else 0))
    base.alpha_composite(img)
    return base


def en_cuadro(lado):
    """El pin centrado en un cuadrado transparente, apoyado abajo; devuelve imagen y punta."""
    esc = (lado - 2) / im.height
    p = im.resize((max(1, round(im.width * esc)), lado - 2), Image.LANCZOS)
    c = Image.new("RGBA", (lado, lado), (0, 0, 0, 0))
    x0 = (lado - p.width) // 2
    c.alpha_composite(p, (x0, 1))
    c = con_borde(c, 1 if lado <= 48 else 2)
    a = c.getchannel("A").load()
    for y in range(lado - 1, -1, -1):  # punta: el píxel opaco más bajo
        xs = [x for x in range(lado) if a[x, y] > 200]
        if xs:
            return c, (round(sum(xs) / len(xs)), y)


c1, punta1 = en_cuadro(48)
c2, _ = en_cuadro(96)
c1.save(DESTINO / "pacifica-cursor.png", optimize=True)
c2.save(DESTINO / "pacifica-cursor@2x.png", optimize=True)
for alto in (48, 96):  # marcador del mapa (se muestra a la mitad: 24 px y 48 px en pantallas densas)
    esc = alto / im.height
    m = im.resize((round(im.width * esc), alto - 4), Image.LANCZOS)
    lienzo = Image.new("RGBA", (m.width + 4, alto), (0, 0, 0, 0))
    lienzo.alpha_composite(m, (2, 2))
    con_borde(lienzo, 1 if alto <= 48 else 2).save(DESTINO / f"pacifica-marcador-{alto}.png", optimize=True)
print("punta del cursor (x y):", *punta1)
