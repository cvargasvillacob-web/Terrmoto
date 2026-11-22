"""Traza el edificio plateado del logo original y lo guarda como vector (marca_edificio.json).

Uso: python3 sitio/marca/trazar_marca.py   (requiere: pip install potracer numpy pillow)
"""
import json, time
from pathlib import Path
import numpy as np, potrace
from PIL import Image
AQUI = Path(__file__).resolve().parent
im = Image.open(AQUI / 'logo-pacifica-original.jpg').convert('RGB')
x0, y0, x1, y1 = 600, 60, 3100, 2200
im = im.crop((x0, y0, x1, y1))
ESC = 2
im = im.resize((im.width // ESC, im.height // ESC), Image.LANCZOS)
a = np.asarray(im).astype(int)
r, g, b = a[..., 0], a[..., 1], a[..., 2]
plata = ((b - r) < 60) & (r > 45)
t = time.time()
bm = potrace.Bitmap(~plata)
plist = bm.trace(turdsize=40, turnpolicy=potrace.POTRACE_TURNPOLICY_MINORITY, alphamax=1.0, opticurve=True, opttolerance=0.3)
print('trace s', round(time.time() - t, 1), 'curvas', len(plist))
d = []
for curve in plist:
    sx, sy = curve.start_point.x, curve.start_point.y
    parts = [f"M{sx:.1f},{sy:.1f}"]
    for seg in curve:
        ex, ey = seg.end_point.x, seg.end_point.y
        if seg.is_corner:
            cx, cy = seg.c.x, seg.c.y
            parts.append(f"L{cx:.1f},{cy:.1f}L{ex:.1f},{ey:.1f}")
        else:
            ax, ay, bx, by = seg.c1.x, seg.c1.y, seg.c2.x, seg.c2.y
            parts.append(f"C{ax:.1f},{ay:.1f} {bx:.1f},{by:.1f} {ex:.1f},{ey:.1f}")
    parts.append("Z")
    d.append("".join(parts))
W, H = im.size
(AQUI / 'marca_edificio.json').write_text(json.dumps({'w': W, 'h': H, 'd': ''.join(d)}))
print(W, H, sum(len(x) for x in d), 'chars')
