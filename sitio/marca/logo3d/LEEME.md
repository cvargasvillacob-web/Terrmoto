# Logo en 3D (guardado para más adelante)

Por ahora se usa el logo original. Esta carpeta arma una versión 3D del edificio (bandas de metal,
ventanas de vidrio azul) y un video corto con movimiento, por si se decide usarlo después.

```bash
python3 exportar_formas.py      # formas.json a partir del logo trazado
npm install                     # three y esbuild
node renderizar.js fotos        # salida/logo-3d-*.png
node renderizar.js video 6      # salida/logo-3d-20-anos.mp4
```
