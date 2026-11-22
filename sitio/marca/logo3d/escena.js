// Escena 3D del logo de Pacífica: edificio extruido en metal, ventanas de vidrio azul
// y textos con volumen. Expone window.preparar(variante, ancho, alto) y window.cuadro(t).
import * as THREE from "three";
import { SVGLoader } from "three/examples/jsm/loaders/SVGLoader.js";

const F = window.FORMAS;
const ESC = 0.01; // unidades del trazo -> unidades de la escena

const MAT = {
  plata: new THREE.MeshPhysicalMaterial({ color: 0xe9ecf2, metalness: 1, roughness: 0.24, clearcoat: 0.8, clearcoatRoughness: 0.18 }),
  cromo: new THREE.MeshPhysicalMaterial({ color: 0xf6f8fb, metalness: 1, roughness: 0.07, clearcoat: 1, clearcoatRoughness: 0.04 }),
  vidrio: new THREE.MeshPhysicalMaterial({ color: 0x0c2a8f, metalness: 0, roughness: 0.18, clearcoat: 0.45, clearcoatRoughness: 0.08, emissive: 0x081f78, emissiveIntensity: 0.5 }),
  blanco: new THREE.MeshPhysicalMaterial({ color: 0xffffff, metalness: 0, roughness: 0.32, clearcoat: 0.7, clearcoatRoughness: 0.2 }),
};

function formas(d) {
  const svg = `<svg xmlns="http://www.w3.org/2000/svg"><path d="${d}" fill-rule="evenodd"/></svg>`;
  const res = [];
  for (const p of new SVGLoader().parse(svg).paths) {
    p.userData.style.fillRule = "evenodd";
    for (const s of SVGLoader.createShapes(p)) res.push(s);
  }
  return res;
}

// El SVG crece hacia abajo; la escena hacia arriba: se voltea cada punto antes de extruir.
const v2 = (v) => new THREE.Vector2(v.x * ESC, -v.y * ESC);
function voltear(shape) {
  const ex = shape.extractPoints(28);
  const s = new THREE.Shape(ex.shape.map(v2));
  s.holes = ex.holes.map((h) => new THREE.Path(h.map(v2)));
  return { s, huecos: ex.holes.map((h) => new THREE.Shape(h.map(v2))) };
}

function extruir(shape, prof, bisel, mat) {
  const g = new THREE.ExtrudeGeometry(shape, {
    depth: prof, curveSegments: 28, bevelEnabled: bisel > 0,
    bevelThickness: bisel, bevelSize: bisel * 0.7, bevelSegments: 5,
  });
  const m = new THREE.Mesh(g, mat);
  m.castShadow = true;
  return m;
}

function centroY(shape) {
  const b = new THREE.Box2().setFromPoints(shape.getPoints());
  return { y: (b.min.y + b.max.y) / 2, alto: b.max.y - b.min.y };
}

function edificio() {
  const g = new THREE.Group();
  const piezas = formas(F.marca.d).map(voltear);
  const bandas = piezas.filter((p) => p.huecos.length).sort((a, b) => centroY(b.s).y - centroY(a.s).y);
  const otras = piezas.filter((p) => !p.huecos.length);
  // Escalonado: la banda de arriba atrás y la de abajo adelante; el arco detrás de todo.
  bandas.forEach((p, i) => {
    const z = i * 0.32;
    const banda = extruir(p.s, 0.9, 0.07, MAT.plata);
    banda.position.z = z;
    g.add(banda);
    for (const h of p.huecos) {
      const vidrio = extruir(h, 0.5, 0, MAT.vidrio);
      vidrio.position.z = z + 0.2;
      g.add(vidrio);
    }
  });
  for (const p of otras) {
    const arco = extruir(p.s, 0.45, 0.05, MAT.cromo);
    arco.position.z = -0.35;
    g.add(arco);
  }
  return g;
}

function texto(clave, prof, bisel, mat) {
  const g = new THREE.Group();
  for (const p of formas(F.textos[clave]).map(voltear)) g.add(extruir(p.s, prof, bisel, mat));
  return g;
}

// Estudio fotográfico: cuarto azul oscuro con tiras de luz que se reflejan en el metal.
function estudio() {
  const s = new THREE.Scene();
  s.add(new THREE.Mesh(new THREE.SphereGeometry(20, 48, 24), new THREE.MeshBasicMaterial({ color: 0x14266b, side: THREE.BackSide })));
  const panel = (w, h, x, y, z, fuerza, color = 0xffffff) => {
    const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h),
      new THREE.MeshBasicMaterial({ color: new THREE.Color(color).multiplyScalar(fuerza), side: THREE.DoubleSide }));
    m.position.set(x, y, z);
    m.lookAt(0, 0, 0);
    s.add(m);
  };
  panel(34, 3.5, 0, 13, 3, 3.2);
  panel(3.5, 18, -12, 2, 7, 2.6);
  panel(3.5, 18, 13, 1, -3, 1.6, 0x9fbaff);
  panel(24, 2.5, 0, -7, 12, 1.4);
  panel(40, 16, 0, 0, 18, 1.15);
  panel(40, 1.8, 0, 6.5, 17.5, 3.6);
  return s;
}

function centrar(obj, x = 0, y = 0, z = 0) {
  const b = new THREE.Box3().setFromObject(obj);
  const c = b.getCenter(new THREE.Vector3());
  obj.position.sub(c).add(new THREE.Vector3(x, y, z));
  return b.getSize(new THREE.Vector3());
}

let renderer, scene, camera, raiz, luzClave, sombra, variante;

window.preparar = (nombre, ancho, alto) => {
  variante = nombre;
  renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, preserveDrawingBuffer: true });
  renderer.setPixelRatio(1);
  renderer.setSize(ancho, alto);
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.05;
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  document.body.appendChild(renderer.domElement);

  scene = new THREE.Scene();
  const pmrem = new THREE.PMREMGenerator(renderer);
  scene.environment = pmrem.fromScene(estudio(), 0.02).texture;

  raiz = new THREE.Group();
  scene.add(raiz);
  const ed = edificio();
  raiz.add(ed);
  const tam = centrar(ed);

  if (nombre === "logo") {
    const pac = texto("PACIFICA", 0.32, 0.04, MAT.plata);
    const inm = texto("INMOBILIARIA", 0.22, 0.03, MAT.blanco);
    raiz.add(pac, inm);
    const tp = centrar(pac, 0, -tam.y / 2 - 1.55, 0.3);
    centrar(inm, 0, -tam.y / 2 - 1.55 - tp.y / 2 - 0.95, 0.3);
  } else if (nombre === "veinte") {
    ed.position.x -= 5.4;
    const veinte = texto("20", 0.9, 0.08, MAT.plata);
    const anos = texto("AÑOS", 0.25, 0.03, MAT.blanco);
    raiz.add(veinte, anos);
    const t20 = centrar(veinte, 5.6, 0.75, 0.1);
    centrar(anos, 5.6, 0.75 - t20.y / 2 - 0.85, 0.2);
  }
  centrar(raiz);

  // Luz principal desde arriba a la izquierda, contraluz azul y piso que solo recibe sombra
  luzClave = new THREE.DirectionalLight(0xffffff, 2.2);
  luzClave.position.set(-3, 14, 4);
  luzClave.castShadow = true;
  luzClave.shadow.mapSize.set(2048, 2048);
  Object.assign(luzClave.shadow.camera, { left: -14, right: 14, top: 14, bottom: -14, near: 1, far: 50 });
  luzClave.shadow.radius = 6;
  scene.add(luzClave);
  const contra = new THREE.DirectionalLight(0x8fb0ff, 1.6);
  contra.position.set(8, 4, -8);
  scene.add(contra);
  scene.add(new THREE.AmbientLight(0x4466cc, 0.35));

  const caja = new THREE.Box3().setFromObject(raiz);
  sombra = new THREE.Mesh(new THREE.PlaneGeometry(80, 80), new THREE.ShadowMaterial({ opacity: 0.38 }));
  sombra.rotation.x = -Math.PI / 2;
  sombra.position.y = caja.min.y - 0.02;
  sombra.receiveShadow = true;
  scene.add(sombra);

  const radio = caja.getBoundingSphere(new THREE.Sphere()).radius;
  camera = new THREE.PerspectiveCamera(28, ancho / alto, 0.1, 200);
  const dist = (radio * 1.08) / Math.sin(THREE.MathUtils.degToRad(28 / 2)) / Math.min(1, ancho / alto);
  camera.position.set(0, radio * 0.32, dist);
  camera.lookAt(0, -radio * 0.05, 0);
  window.cuadro(0.12);
  window.listo = true;
};

// t en [0,1): el logo gira suave de un lado a otro y la luz barre el metal; el ciclo empalma.
window.cuadro = (t) => {
  const a = Math.sin(t * Math.PI * 2);
  raiz.rotation.y = 0.42 * a;
  raiz.rotation.x = 0.06 + 0.03 * Math.cos(t * Math.PI * 2);
  luzClave.position.x = -3 + 6 * Math.cos(t * Math.PI * 2);
  renderer.render(scene, camera);
};
