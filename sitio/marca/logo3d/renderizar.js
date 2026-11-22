// Renderiza el logo 3D con Chromium sin pantalla.
// Uso: node renderizar.js fotos           -> salida/logo-3d-*.png
//      node renderizar.js video [segundos] -> salida/logo-3d-20-anos.mp4 (1280x720, 30 fps)
import { buildSync } from "esbuild";
import { chromium } from "playwright";
import { spawn } from "node:child_process";
import { mkdirSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const AQUI = dirname(fileURLToPath(import.meta.url));
const SALIDA = join(AQUI, "salida");
mkdirSync(SALIDA, { recursive: true });
buildSync({ entryPoints: [join(AQUI, "escena.js")], bundle: true, format: "iife", outfile: join(AQUI, "build", "escena.js"), logLevel: "warning" });
const bundle = readFileSync(join(AQUI, "build", "escena.js"), "utf8");
const formas = readFileSync(join(AQUI, "formas.json"), "utf8");

const FONDO = "radial-gradient(120% 120% at 38% 30%, #3a66d8 0%, #203e98 45%, #0b1a52 100%)";
const html = (w, h, fondo = FONDO) => `<!doctype html><html><head><style>
  html,body{margin:0;width:${w}px;height:${h}px;overflow:hidden;background:${fondo}}
  canvas{display:block}
</style></head><body><script>window.FORMAS=${formas};</script><script>${bundle}</script></body></html>`;

async function pagina(navegador, variante, w, h, fondo) {
  const p = await navegador.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
  p.on("pageerror", (e) => console.error("error en página:", e.message));
  await p.setContent(html(w, h, fondo));
  await p.evaluate(([v, a, b]) => window.preparar(v, a, b), [variante, w, h]);
  await p.waitForFunction(() => window.listo === true, null, { timeout: 120000 });
  return p;
}

const navegador = await chromium.launch({ args: ["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"] });
const modo = process.argv[2] || "fotos";

if (modo === "pin") {
  // Fondo transparente: sirve para marcadores del mapa y para el cursor
  const p = await pagina(navegador, "pin", 1000, 1250, "transparent");
  await p.evaluate(() => window.cuadro(0));
  await p.screenshot({ path: join(SALIDA, "pin-3d.png"), omitBackground: true });
  console.log("ok pin");
} else if (modo === "fotos") {
  for (const [variante, w, h, t] of [["marca", 1600, 1200, 0.2], ["logo", 1400, 1400, 0.06], ["veinte", 1800, 1000, 0.1]]) {
    const p = await pagina(navegador, variante, w, h);
    await p.evaluate((x) => window.cuadro(x), t);
    await p.screenshot({ path: join(SALIDA, `logo-3d-${variante}.png`) });
    console.log("ok", variante);
    await p.close();
  }
} else {
  const seg = Number(process.argv[3] || 6), fps = 30, n = seg * fps;
  const [w, h] = [1280, 720];
  const p = await pagina(navegador, "veinte", w, h);
  const ff = spawn("ffmpeg", ["-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", String(fps), "-i", "-",
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-movflags", "+faststart", join(SALIDA, "logo-3d-20-anos.mp4")],
    { stdio: ["pipe", "inherit", "inherit"] });
  for (let i = 0; i < n; i++) {
    await p.evaluate((x) => window.cuadro(x), i / n);
    ff.stdin.write(await p.screenshot({ type: "png" }));
    if (i % 30 === 0) console.log("cuadro", i, "de", n);
  }
  ff.stdin.end();
  await new Promise((r) => ff.on("close", r));
  console.log("ok video");
}
await navegador.close();
