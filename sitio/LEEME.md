# Sitio de Pacífica Inmobiliaria

Dos partes:

- **pacificainmobiliaria.com**: la web pública. Se armará en WordPress con la plantilla Houzez
  (publicación de propiedades por propietarios y asociados, con aprobación previa, y Google Maps),
  más nuestro mapa «Panamá en datos». El prototipo de diseño va en `plantillas/`.
- **proyectos.pacificainmobiliaria.com**: portal privado con clave. Cada proyecto tiene su
  mapa interactivo y sus documentos (lista de llamadas, reporte del día, pistas e informe).

## Armar el portal de proyectos

```bash
pip install markdown
python3 sitio/construir.py
```

Deja la carpeta `sitio/salida/proyectos/` y el paquete `sitio/salida/proyectos.zip`
(ambos fuera de Git). Antes rearma el mapa con lo último de `locales/datos/anuncios.json`.

## Subirlo a Hostinger con clave

1. **Hosting activo.** El dominio está en Hostinger. Si el plan de hosting venció, renuévalo
   o compra uno (Premium o Business sirven también para WordPress) y asígnale
   pacificainmobiliaria.com.
2. **Subdominio.** hPanel → Dominios → Subdominios → crear `proyectos`. Anota su carpeta
   (por ejemplo `public_html/proyectos`).
3. **Archivos.** hPanel → Administrador de archivos → entra a esa carpeta → sube
   `proyectos.zip` → clic derecho → Extraer. `index.html` debe quedar directo en la carpeta,
   no dentro de otra subcarpeta.
4. **Clave.** hPanel → Avanzado → «Proteger directorios con contraseña» → elige la carpeta
   del subdominio → usuario `julio` y una clave segura → Proteger. Puedes crear un usuario
   por persona y borrarlo cuando deje el proyecto.
5. **Entregar el acceso.** Manda a Julio el enlace por un lado y la clave por otro (no los dos
   en el grupo).
6. **Actualizar.** Repite el paso 3 con el zip nuevo; la clave se mantiene.

El portal tiene `robots.txt` y la etiqueta `noindex` para que Google no lo indexe, pero lo
que lo protege es la clave.

## Logos

`marca/generar_logos.py` arma las versiones «20 años» a partir del logo original
(`marca/logo-pacifica-original.jpg`), cuyo edificio está trazado en vector en
`marca/marca_edificio.json`. Los PNG se regeneran con el script; en Git quedan los SVG.
