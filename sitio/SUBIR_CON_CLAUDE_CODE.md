# Instrucción para Claude Code: publicar pacificainmobiliaria.com

Copia y pega el bloque en Claude Code, en una computadora con acceso a internet y al hosting.

```text
Tarea: publicar hoy pacificainmobiliaria.com (web de Pacífica Inmobiliaria) y el portal
privado de proyectos de Julio, en el hosting de GoDaddy de la cuenta pacificainversiones.com
(cPanel).

1. Código
- Clona o actualiza https://github.com/cvargasvillacob-web/Terrmoto y usa la rama
  claude/fervent-faraday-l67o51.
- Instala la dependencia y arma los paquetes:
    pip install "markdown>=3.5,<4"
    python3 sitio/construir.py
- Deben quedar sitio/salida/sitio/ (web pública) y sitio/salida/proyectos/ (portal privado).
  Abre sitio/salida/sitio/index.html en el navegador y confirma que carga el mapa.

2. Accesos
- Pídeme el servidor FTP, el usuario y la contraseña (o el usuario y la contraseña de cPanel).
  No los guardes en el repositorio ni en archivos, ni los muestres en el resumen.

3. Carpeta correcta (muy importante)
- public_html es de pacificainversiones.com, que tiene WordPress. No borres, renombres ni
  sobrescribas nada ahí.
- Confirma en cPanel (Dominios) que pacificainmobiliaria.com está agregado y anota su carpeta
  raíz (document root). Si no existe, avísame antes de crearlo.
- Antes de subir, descarga una copia de lo que haya en esa carpeta a
  ./respaldo-pacificainmobiliaria-<fecha>/.

4. Subida
- Sube el contenido de sitio/salida/sitio/ a la carpeta raíz de pacificainmobiliaria.com, de
  modo que index.html quede directo en esa carpeta.
- Sube el contenido de sitio/salida/proyectos/ a <raíz>/proyectos/.
- Usa FTPS si el servidor lo acepta, por ejemplo con lftp:
    lftp -u USUARIO SERVIDOR -e "set ftp:ssl-force true; mirror -R --verbose sitio/salida/sitio/ RAIZ/; mirror -R --verbose sitio/salida/proyectos/ RAIZ/proyectos/; quit"
- No uses opciones que borren archivos del servidor (nada de --delete).

5. Clave del portal
- Protege RAIZ/proyectos con contraseña en cPanel > Privacidad de directorios (Directory
  Privacy), usuario "julio". Pídeme la clave o genera una segura y dímela una sola vez.
- Verifica que https://pacificainmobiliaria.com/proyectos/ pide usuario y clave (responde 401
  sin credenciales).

6. Dominio y certificado
- Revisa con dig que pacificainmobiliaria.com y www.pacificainmobiliaria.com apuntan a la IP
  compartida del hosting (aparece en cPanel). Si no, dime exactamente qué cambiar en Hostinger
  (hPanel > Dominios > DNS): registros A de @ y www a esa IP. No toques los registros MX.
- Cuando el dominio apunte al hosting, corre AutoSSL en cPanel (SSL/TLS Status) para tener https.

7. Comprobación final
- https://pacificainmobiliaria.com carga, se ve el mapa de la portada y el botón de WhatsApp
  abre el chat con +507 6330-4414.
- Dame un resumen: qué subiste, a qué carpeta, la dirección del portal y su usuario.

8. Publicación automática (solo con mi permiso)
- El repositorio tiene .github/workflows/publicar-pacifica.yml, que sube la web sola por FTP en
  cada cambio. Para activarlo, crea los secretos del repositorio con gh y deja que yo escriba la
  contraseña cuando gh la pida:
    gh secret set PACIFICA_FTP_SERVER
    gh secret set PACIFICA_FTP_USERNAME
    gh secret set PACIFICA_FTP_PASSWORD
- Si la carpeta de esa cuenta FTP no es la raíz del dominio, crea también las variables
  PACIFICA_DIR_WEB (ruta de la raíz) y PACIFICA_DIR_PROYECTOS (ruta de la raíz + /proyectos/)
  con gh variable set.
- Lanza el flujo una vez (gh workflow run publicar-pacifica.yml --ref claude/fervent-faraday-l67o51)
  y confirma que terminó bien.
```
