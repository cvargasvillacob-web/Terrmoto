# Lentes disruptivos: el terremoto de Azuero (9 oct 2026) visto al revés

**Fecha de corte:** 19 de noviembre de 2026 (día 41 después del sismo).
**Complementa a:** [`terremoto-panama-2026-10-09-datos-tecnicos.md`](terremoto-panama-2026-10-09-datos-tecnicos.md), escrito el mismo día del evento.

Un *lente disruptivo* es otra forma de leer los mismos datos, una que rompe la narrativa por defecto. Cada lente de este documento tiene la misma estructura:

- **Narrativa dominante:** lo que se dijo o se asumió.
- **Lo que muestran los datos:** cifras con fuente y fecha.
- **Pregunta incómoda:** la que la narrativa evita.
- **Qué haríamos distinto:** propuesta concreta.

Cada lente lleva además un nivel de **confianza** (alta, media o baja) según la solidez de la evidencia disponible al día 41.

---

## 0. Punto de partida: el día 0 frente al día 41

Antes de los lentes, conviene comparar lo que decía el informe técnico del 9 de octubre con lo que se sabe seis semanas después.

| Dato | Informe del día 0 (9 oct) | Estado al día 41 (19 nov) | Fuente |
|---|---|---|---|
| Fallecidos | Ninguno confirmado | **2** (Sinaproc, corte 28–30 oct). Un medio reporta una tercera víctima; sin confirmar | Sinaproc #25 y #26; Minuto60 |
| Heridos | "Varios heridos leves", "sin heridos de gravedad" | **27**. Al menos una persona gravemente herida (mujer de 68 años) murió días después en el hospital | Sinaproc; EFE vía Diario del Sur |
| Viviendas | Daños puntuales en Penonomé, Playa Venao y Pedasí | **2,318 con daño total, 5,546 con daño moderado o parcial y 1,260 con daño leve** (19 oct). 17,058 evaluadas al 30 oct | Sinaproc #16 y #26 |
| Puentes y vías | "Sinaproc no reportó daños en puentes" | **Al menos 14 puentes dañados** en los primeros reportes. El MOP llevó otros 14 al Consejo de Gabinete y mantenía 16–17 en inspección. Hubo comunidades aisladas alrededor de Tonosí | Rio Times; AFP vía Excelsior y CRHoy |
| Escuelas, salud y edificios públicos | Clases vespertinas suspendidas | **619 centros educativos, 120 instalaciones de salud y 127 edificios gubernamentales afectados**. USD 61 M para reparar 67 instalaciones hospitalarias | Sinaproc #25; EFE vía Infobae |
| Iglesias | Daños en la catedral de Penonomé | **44 iglesias afectadas** (informe oficial vía EFE). El primer conteo de la Conferencia Episcopal era de 13 | Revista Summa; La Estrella |
| Réplicas | 46 | **1,452** (6 nov) | IGC-UP vía La Estrella y Prensa Latina |
| Magnitud del IGC-UP | 7.2 | **7.5** (revisada); es la cifra que usa Sinaproc | TVN; Telemetro; Sinaproc |
| Personas | n/d | **55,245 registradas** (30 oct). Unas 3,700 personas en 46 albergues (17 oct) | Sinaproc #26; EFE vía Primicias |
| Pérdidas económicas | PAGER: cientos de millones de USD (modelo) | **De USD 200–300 M** (Felipe Argote) **a hasta USD 2,000 M** (modelo de la Universidad de Panamá) | Infobae; CR Prensa |
| Seguros | — | **6,865 siniestros** reportados por 17 aseguradoras | SSRP vía La Estrella |
| Respuesta fiscal | — | Estado de emergencia; fondo de **hasta USD 100 M** canalizado por fideicomisos | AP vía ADN; Bloomberg Línea |

**Ninguna cifra de daño mejoró. Todas empeoraron.** De ahí parte el primer lente.

---

## Lente 1. Lente temporal: "El día 0 miente, y siempre en la misma dirección"

**Confianza: alta**

- **Narrativa dominante:** "Fuerte sismo, pero sin destrucción mayor". Así lo resumió un titular de agencia replicado en medios de todo el mundo ("Strong Panama quake shakes nation, but avoids major destruction"), y es lo que decía nuestro propio informe técnico.
- **Lo que muestran los datos:**
  - Las cifras del día 0 resultaron ser un **piso, no una estimación**. Los muertos pasaron de 0 a 2, los heridos de "varios" a 27, las réplicas de 46 a 1,452 y los puentes de "sin daños" a decenas en evaluación.
  - La frase "Sinaproc no reportó daños en puentes" era cierta, pero no significaba que no los hubiera. Los lugares más dañados (alrededor de Tonosí) eran justo los que no podían reportar: tenían la telefonía caída y los caminos cortados.
  - El modelo PAGER del USGS acertó en el orden de magnitud económico (alerta roja, cientos de millones de USD) y se equivocó en vidas (pronosticaba decenas a centenas de muertos). Los reportes de campo del día 0 fueron optimistas en ambas cosas.
  - Hasta el identificador del evento cambia según la fuente. Nuestro informe citó `pt26282000` (solución del PTWC), pero el producto PAGER del USGS usa `us6000u18k`.
- **Pregunta incómoda:** si todos los sesgos del día 0 apuntan en la misma dirección, ¿por qué seguimos comunicando esas cifras como si fueran un balance?
- **Qué haríamos distinto:**
  1. **Regla del silencio.** Cuando una zona cercana al epicentro no reporta, se trata como zona con daño probable alto, no como zona sin daño.
  2. **Cifras con fecha de vencimiento.** Cada número publicado el día 0 se etiqueta como "piso preliminar".
  3. **Usar el modelo para el orden de magnitud y el campo para el piso.** El rango real suele quedar entre los dos.

---

## Lente 2. Lente métrico: "La magnitud es una decisión, no solo una medición"

**Confianza: alta**

- **Narrativa dominante:** "La magnitud es un dato objetivo; las diferencias son técnicas".
- **Lo que muestran los datos:**
  - Seis semanas después conviven **tres cifras oficiales**: 7.7 Mww (USGS), 7.5 (IGC-UP revisada, la que usa el Gobierno) y 7.2 (primer reporte del IGC-UP, que según un sitio de seguimiento aún figura en su catálogo).
  - Las diferencias no son menores. Cada décima de magnitud multiplica la energía por 10^0.15 (≈ 1.4). Entre 7.5 y 7.7 hay **≈ 2 veces** más energía; entre 7.2 y 7.7, **≈ 5.6 veces**.
  - La primera cifra automática del USGS, **8.0**, activó una amenaza de tsunami para cinco países con olas pronosticadas de 1 a 3 m. Era un sismo de rumbo, que mueve poca agua. La alerta reaccionó al número, no al mecanismo, porque el mecanismo todavía no se conocía.
- **Pregunta incómoda:** si un contrato, un seguro paramétrico o un comunicado oficial depende de la magnitud, ¿cuál de las tres cifras vale? ¿Y quién decide?
- **Qué haríamos distinto:**
  1. Fijar un **protocolo de magnitud de referencia**: la red nacional publica su magnitud local y adopta explícitamente una Mw de referencia (propia, del USGS o del GCMT), con una explicación pública de la diferencia.
  2. En cualquier instrumento financiero o legal, **especificar la agencia y el tipo de magnitud** que se usarán como disparador.
  3. En las alertas de tsunami, comunicar en un segundo mensaje **por qué se levantan** (mecanismo de rumbo), no solo que se levantan. Eso protege la credibilidad de la próxima alerta.

---

## Lente 3. Lente contrafactual: "Dos muertos no es un éxito; es un cuasi-accidente"

**Confianza: media** (el contrafactual es razonado, no modelado)

- **Narrativa dominante:** "Panamá resistió un 7.7 con muy pocas víctimas".
- **Lo que muestran los datos:**
  - Hubo 2,318 viviendas con daño total, colapsos de un hotel en Playa Venao y de parte de la Gobernación de Penonomé, y 619 escuelas afectadas. El potencial de víctimas existía.
  - Varios factores que redujeron las víctimas fueron **suerte, no diseño**:
    - **La hora:** 12:56 p. m. de un día laborable, con la gente despierta y muchas personas fuera de casa.
    - **La temporada:** octubre es temporada baja en la costa de Azuero. Las edificaciones turísticas dañadas en Pedasí estaban desocupadas.
    - **La densidad:** el epicentro está en una zona rural poco poblada, a unos 200 km de la capital.
- **Pregunta incómoda:** ¿cuántas víctimas habría dejado la misma ruptura a las 3 a. m.? ¿Y durante el Carnaval de Las Tablas, a unos 60 km del epicentro y con las calles llenas de visitantes?
- **Qué haríamos distinto:**
  1. Hacer una **revisión formal de cuasi-accidente**, al estilo de la aviación. Por cada estructura colapsada o con daño total se estima su ocupación probable a otras horas y en otras fechas.
  2. Medir la respuesta por la **exposición evitada por diseño**, no por el conteo de muertos.
  3. Revisar la evaluación estructural de las escuelas afectadas como si hubieran estado llenas.

---

## Lente 4. Lente de memoria: "La falla no estaba dormida; nosotros sí"

**Confianza: alta**

- **Narrativa dominante:** "Una esquina sísmicamente tranquila de Panamá produjo un 7.7". Así lo enmarcaron varios medios internacionales, que hablaron de la "falla silenciosa".
- **Lo que muestran los datos:**
  - En **1913** hubo un sismo destructivo en Azuero, de Mw 6.6–6.9 según la fuente (Víquez y Camacho, 1990, citado por la Universidad de Panamá). Un geólogo citado tras el evento lo ubicó en un rango de energía similar para el mismo sistema de fallas.
  - El **sistema de fallas Azuero-Soná** (rumbo NO-SE, sinistral) está descrito en la literatura académica panameña. El director del IGC-UP lo señaló como la fuente probable desde el primer día.
  - Un artículo del Banco Mundial ya advertía que la percepción generalizada era que "solo Chiriquí" tiene problemas sísmicos.
  - Entre 1913 y 2026 pasaron **113 años**, unas cuatro generaciones. Ninguna persona viva recordaba el anterior.
- **Pregunta incómoda:** si la amenaza estaba en los papers, ¿por qué no estaba en la cabeza de la gente ni, quizá, en las casas?
- **Qué haríamos distinto:**
  1. Incluir la **historia sísmica local** (1621, 1882, 1913, 1934, 2026) en el currículo escolar de cada región.
  2. Instalar **marcadores físicos de memoria** en Tonosí, Los Pozos y La Villa con la fecha y la intensidad de 1913 y de 2026.
  3. Verificar que el mapa de amenaza del REP represente las **fuentes corticales de rumbo**, no solo la subducción. La UTP ya anunció que usará el sismo como caso de estudio.

---

## Lente 5. Lente territorial: "La capital fue espectadora, no examinada"

**Confianza: alta**

- **Narrativa dominante:** "El Canal opera con normalidad, el Metro se reanudó y la ciudad fue evacuada sin daños mayores".
- **Lo que muestran los datos:**
  - Mientras los titulares internacionales hablaban del tráfico del Canal, en Azuero había **comunidades aisladas** por caminos y puentes destruidos (AFP) y familias viviendo "entre galeras, cartones y carpas" en Isla Cañas, Búcaro y Tonosí (La Prensa).
  - Solo en **Los Pozos** (Herrera) se contaban unas 2,000 viviendas afectadas y unos 30 albergues.
  - La capital estaba a unos 200 km del epicentro. **No pasó el examen: no lo presentó.** Su riesgo propio es otro y es real. Estudios paleosísmicos (Rockwell et al., 2010) identifican como activa la falla de Pedro Miguel, junto al Canal, y la ciudad sufrió sismos destructivos en 1621 y 1882.
- **Pregunta incómoda:** si los indicadores de "resiliencia" se miden en la capital, ¿quién mide la recuperación de Tonosí?
- **Qué haríamos distinto:**
  1. Publicar un **tablero de recuperación por corregimiento**: días sin acceso vial, viviendas reparadas y personas en albergue.
  2. No usar el funcionamiento del Canal como indicador de impacto de un sismo lejano; es un dato logístico, no de daño.
  3. Usar el evento como simulacro de mesa: **la misma ruptura bajo la ciudad de Panamá**.

---

## Lente 6. Lente constructivo: "El código no llega a donde se cayeron las casas"

**Confianza: media**

- **Narrativa dominante:** "Hay que revisar y actualizar el Reglamento Estructural Panameño (REP)".
- **Lo que muestran los datos:**
  - El REP existe desde 1984 y se ha actualizado cinco veces, pero según expertos de la UTP **su aplicación sigue siendo limitada**.
  - El REP-84 no exigía un diseño sísmico formal para viviendas unifamiliares.
  - Muchas viviendas del interior se levantan **sin planos aprobados ni supervisión profesional** (UTP), y el daño se concentró en ese tipo de vivienda rural.
  - El Gobierno anunció que **prestará fondos del fideicomiso a contratistas** para construir viviendas.
- **Pregunta incómoda:** un código más exigente, ¿qué cambia en una casa que nunca pasó por un ingeniero?
- **Qué haríamos distinto:**
  1. Llevar la palanca al **albañil, la ferretería y el material**, no solo al reglamento. Eso significa planos tipo gratuitos con detalles sísmicos (vigas de amarre, columnas y conexiones) y certificación de maestros de obra en Azuero.
  2. Considerar la **reconstrucción dirigida por el propietario con asistencia técnica**, documentada por el Banco Mundial en *Safer Homes, Stronger Communities* (2010), junto al modelo por contratista. Los pagos se entregarían por tramos, condicionados a inspecciones de los detalles clave.
  3. Auditar los edificios públicos construidos antes de 1984, como piden expertos citados por La Prensa.

---

## Lente 7. Lente del desastre lento: "Las réplicas no son el epílogo; son el desastre"

**Confianza: alta** en los conteos, **media** en la extrapolación

- **Narrativa dominante:** "El sismo fue el 9 de octubre".
- **Lo que muestran los datos:**

| Fecha | Días después | Réplicas acumuladas (IGC-UP) |
|---|---|---|
| 9 oct (tarde) | ~0.2 | 46 |
| 16 oct, 7:40 a. m. | 6.8 | 746 |
| 19 oct | ~9.8 | 917 |
| 6 nov | ~27.8 | 1,452 |

- **Verificación rápida con leyes empíricas** (cálculo propio, orden de magnitud):
  - **Ley de Båth.** La réplica mayor suele ser unas 1.2 unidades menor que el sismo principal: 7.7 − 1.2 ≈ **6.5**. Coincide con la réplica de 6.4–6.6 de la 1:37 p. m. La secuencia es "normal".
  - **Ley de Omori** (tasa ∝ 1/t). Con los conteos del 16 y el 19 de octubre se ajusta K ≈ 460–500 réplicas por unidad logarítmica de tiempo. Esa ley predice ≈ 485 réplicas entre el 19 de octubre y el 6 de noviembre; se observaron **535**, un 10 % de diferencia.
  - El mismo ajuste exige una constante c ≈ 1.4–2 días, muy grande. Es la firma de la **incompletitud temprana**: en las primeras horas la red no alcanzó a contar muchas réplicas, porque sus señales se superponen. Esto refuerza el Lente 1: el "46" del día 0 era un piso.
  - **Extrapolación**, suponiendo un umbral de detección constante: unas **1,600–1,700 réplicas acumuladas hacia el 19 de noviembre** y unas **2,000 a fin de año**, a un ritmo que baja de ~12 a ~6 por día. El director del IGC-UP ya advirtió que la secuencia podría extenderse hasta diciembre.
- **Pregunta incómoda:** si la secuencia dura meses y coincide con el pico de la temporada lluviosa (deslizamientos y caminos cortados), ¿por qué los albergues y la ayuda se planifican en días?
- **Qué haríamos distinto:**
  1. Planificar la **vivienda temporal para meses**.
  2. Comunicar **pronósticos probabilísticos de réplicas**, al estilo de los que publica el USGS, en lugar de "pueden seguir ocurriendo".
  3. Tratar la salud mental como parte de la respuesta. Hay familias que temen volver a casas que siguen en pie.

---

## Lente 8. Lente fiscal: "Un terremoto pagado a crédito y con fideicomisos"

**Confianza: media** (las estimaciones de pérdidas varían diez veces)

- **Narrativa dominante:** "El Estado cuenta con los recursos necesarios". Sinaproc descartó pedir ayuda internacional el día 0.
- **Lo que muestran los datos:**
  - **Tamaño del fondo frente al daño.** El fondo de emergencia es de hasta USD 100 M, y las pérdidas estimadas van de USD 200–300 M a USD 2,000 M. El fondo cubre **entre el 5 % y el 50 %** del daño estimado.
  - **Ejecución.** Según el ministro Chapman, los desembolsos **no superaban los USD 20 M**, menos del 10 % de la estimación más baja. Las solicitudes de Azuero ya rondaban los USD 80 M.
  - **Ingeniería fiscal.** Los dos fideicomisos permiten **no pedir a la Asamblea una dispensa de la Ley de Responsabilidad Fiscal** y mantener la meta de déficit del 3.5 % del PIB (Bloomberg Línea). El MEF descartó "por ahora" usar el Fondo de Ahorro de Panamá.
  - **Financiamiento externo.** El Gobierno gestionó fondos con el BID, la CAF, el BCIE, el Banco Mundial y el FMI. Las donaciones suman poco más de USD 5 M; las líneas de la CAF y el BID son **préstamos**.
  - **Seguros.** Hay 6,865 siniestros reportados por 17 aseguradoras. Una aseguradora advirtió que muchas viviendas afectadas del interior **no tenían ningún seguro**.
- **Pregunta incómoda:** el terremoto se paga en tres monedas: deuda pública, contabilidad creativa y los ahorros de familias sin seguro. La tercera no aparece en ninguna estadística. ¿Cuánto pone cada una?
- **Qué haríamos distinto:**
  1. Armar una **estrategia de financiamiento ex ante por capas**: un fondo de reserva para eventos frecuentes, un crédito contingente para eventos medianos y transferencia de riesgo para los extremos. Chile, Colombia, México y Perú colocaron en 2018, con el Banco Mundial, bonos catastróficos conjuntos contra terremotos; Panamá no participó.
  2. Definir **reglas de activación públicas** para el Fondo de Ahorro. Si un estado de emergencia nacional no lo activa, ¿qué lo haría?
  3. Pedir a la SSRP los **siniestros por provincia** para medir la brecha de protección. Hipótesis por verificar: los reclamos se concentran donde hay hipotecas (ciudades), y el daño, donde no las hay.

---

## Lente 9. Lente patrimonial: "Restaurar como estaba es restaurar la vulnerabilidad"

**Confianza: media**

- **Narrativa dominante:** "Las iglesias dañadas recibirán intervención estatal" (ministra de Cultura).
- **Lo que muestran los datos:**
  - El conteo de **iglesias afectadas pasó de 13 a 44**.
  - En **Natá**, la Basílica Santiago Apóstol y la Capilla San Juan de Dios presentan grietas y desprendimientos.
  - En **La Villa de Los Santos**, cuna del Primer Grito de Independencia (1821), se retiraron piezas en riesgo de la iglesia de San Atanasio.
  - Ese patrimonio es parte de la economía de Azuero: turismo cultural y fiestas patronales y patrias.
- **Pregunta incómoda:** si el templo resistió así un sismo de 1913 y otro de 2026, ¿restaurarlo idéntico no es programar el próximo daño?
- **Qué haríamos distinto:**
  1. Hacer **refuerzo compatible y reversible** (tirantes, anclajes y refuerzos ocultos), discutido de forma explícita con criterios de conservación, en lugar de una reposición idéntica.
  2. Hacer ahora el **levantamiento digital (escaneo 3D)** de los templos dañados, antes de que una réplica cambie su estado.
  3. Elaborar un **inventario de vulnerabilidad sísmica** de todos los templos coloniales del Arco Seco antes del próximo evento.

---

## Lente 10. Lente de datos: "La red sísmica es infraestructura crítica, aunque viva en una universidad"

**Confianza: media**

- **Narrativa dominante:** "Geociencias informa".
- **Lo que muestran los datos:**
  - La referencia nacional para magnitudes, réplicas y localización es el **Instituto de Geociencias de la Universidad de Panamá**. Su magnitud cambió de 7.2 a 7.5 en una noche, y su conteo de réplicas pasó de 46 a 1,452.
  - El IGC-UP anunció un informe consolidado para el 9 de noviembre. Al cierre de este documento no se encontró publicado.
  - **La falla que rompió aún no está confirmada en campo.** El IGC-UP habló de una ruptura de unos 90 km. Análisis secundarios del modelo de falla finita del USGS sugieren **dos parches de deslizamiento separados**, posiblemente por un escalón de falla, y otras fuentes citan ~150 km y hasta 7.8 m de deslizamiento. Nada de esto está verificado contra la fuente primaria.
  - El REP de 2004 exige **instrumentación sísmica en todo edificio nuevo de más de 15 pisos o 5,000 m²**. Las torres de la capital deberían haber registrado este sismo.
- **Pregunta incómoda:** ¿dónde están esos registros acelerográficos? ¿Quién los recoge, y por qué no son públicos?
- **Qué haríamos distinto:**
  1. Crear un **portal de datos abiertos con historial de versiones**: cada revisión de magnitud y de profundidad, con fecha y hora.
  2. Hacer una **recolección obligatoria y publicación de los registros acelerográficos** exigidos por el REP 2004. Son datos para calibrar el riesgo de la capital con un sismo real.
  3. Darle a la red sísmica un **presupuesto y redundancia de infraestructura crítica**, no de proyecto académico.

---

## Matriz resumen

| # | Lente | Tesis | Evidencia clave | Confianza | Acción prioritaria |
|---|---|---|---|---|---|
| 1 | Temporal | El día 0 subestima siempre | 0 → 2 muertos; 46 → 1,452 réplicas; puentes "sin daño" → decenas | Alta | Regla del silencio y cifras con vencimiento |
| 2 | Métrico | La magnitud es una decisión | 7.2 / 7.5 / 7.7; alerta de tsunami por un 8.0 automático | Alta | Protocolo de magnitud de referencia |
| 3 | Contrafactual | Pocas víctimas = suerte | Mediodía, temporada baja, zona rural | Media | Revisión de cuasi-accidente |
| 4 | Memoria | La falla no estaba dormida | Sismo de 1913, falla Azuero-Soná documentada | Alta | Historia sísmica local en escuelas |
| 5 | Territorial | La capital no fue examinada | Comunidades aisladas frente a "Canal normal" | Alta | Tablero por corregimiento |
| 6 | Constructivo | El código no llega a la casa autoconstruida | REP con aplicación limitada; viviendas sin planos | Media | Planos tipo y maestros de obra certificados |
| 7 | Desastre lento | Las réplicas son el desastre | Omori ajusta al 10 %; secuencia hasta diciembre | Alta / media | Vivienda temporal por meses |
| 8 | Fiscal | Pagado a crédito | Fondo de USD 100 M frente a pérdidas de 200 M–2,000 M; < 20 M desembolsados | Media | Financiamiento ex ante por capas |
| 9 | Patrimonial | Restaurar igual = mismo riesgo | 13 → 44 iglesias afectadas | Media | Refuerzo compatible y escaneo 3D |
| 10 | Datos | La red es infraestructura crítica | Magnitud versionada; acelerogramas no públicos | Media | Datos abiertos con historial |

---

## Preguntas abiertas para seguir investigando

1. ¿Qué falla rompió, con qué longitud y con cuánto deslizamiento en superficie? Faltan el trabajo de campo, el InSAR y el informe consolidado del IGC-UP.
2. ¿Cuál fue la intensidad máxima real (¿IX en Tonosí?) y dónde están los registros de aceleración?
3. ¿Cuántas de las 2,318 viviendas con daño total tenían seguro? ¿Cómo se reparten los 6,865 siniestros por provincia?
4. ¿Cuál es el balance final de Sinaproc? El último encontrado es el Comunicado #26, del 30 de octubre.
5. ¿Se confirmará una tercera víctima mortal?

---

## Método y limitaciones

- Compilado el 19 de noviembre de 2026 a partir de resultados de búsqueda web. Desde este entorno no fue posible abrir directamente las páginas de Sinaproc, Wikipedia ni Substack, así que las cifras de los comunicados de Sinaproc se tomaron de los extractos que devolvió el buscador. Conviene verificarlas contra los comunicados originales.
- Los cálculos de energía, de la ley de Båth y del ajuste de Omori son **propios y de orden de magnitud**. Suponen un umbral de detección constante y no sustituyen un pronóstico oficial.
- Las cifras de falla finita (90 km, 150 km, 7.8 m, dos parches) provienen de fuentes secundarias y **no están verificadas** contra el USGS.
- Este documento no reemplaza al informe técnico del día 0. Lo usa como objeto de análisis. Donde ambos difieren, prevalecen las cifras con fecha más reciente.

---

## Fuentes

### Oficiales
- Sinaproc, Comunicado Oficial #16 (19 oct): https://www.sinaproc.gob.pa/comunicado-oficial-16/
- Sinaproc, Comunicado Oficial #18 (21 oct): https://www.sinaproc.gob.pa/comunicado-oficial-18/
- Sinaproc, Comunicado Oficial #23 (26 oct): https://www.sinaproc.gob.pa/comunicado-oficial-23/
- Sinaproc, Comunicado Oficial #25 (28 oct): https://www.sinaproc.gob.pa/comunicado-oficial-25/
- Sinaproc, Comunicado Oficial #26 (30 oct): https://www.sinaproc.gob.pa/comunicado-oficial-26/
- USGS, PAGER (evento `us6000u18k`): https://earthquake.usgs.gov/pdl/products/urn%3Ausgs-product%3Aus%3Alosspager%3Aus6000u18k%3A1791573634239/contents/onepager.pdf

### Réplicas, magnitud y falla
- La Estrella de Panamá, 1,452 réplicas en la falla Azuero-Soná: https://www.laestrella.com.pa/panama/nacional/falla-azuero-sona-alcanza-1452-replicas-tras-el-terremoto-de-magnitud-75-AH27134774
- Prensa Latina, más de 1,400 réplicas (6 nov): https://www.prensa-latina.cu/2026/11/06/panama-contabiliza-mas-de-mil-400-replicas-tras-fuerte-terremoto/
- Panamá América, 746 réplicas: https://www.panamaamerica.com.pa/sociedad/instituto-de-geociencias-contabiliza-746-replicas-hasta-este-viernes-1267579
- La Prensa, 917 réplicas: https://www.prensa.com/sociedad/panama-registra-917-replicas-tras-el-terremoto-de-azuero-tambien-sismos-en-chiriqui-y-bocas-del-toro/
- TVN, 170 réplicas y magnitud 7.5: https://www.tvn-2.com/nacionales/temblor-panama-instituto-geociencias-reporta_1_2265386.html
- Telemetro, réplicas disminuyen (7.5): https://www.telemetro.com/nacionales/tras-el-terremoto-magnitud-75-las-replicas-disminuyen-que-significa-n6094886
- Minuto60, qué es la falla Azuero-Soná: https://www.minuto60.com/mundo/que-es-falla-azuero-sona-su-relacion-sismo-panama/16906
- Earthquake Insights, análisis del modelo de falla finita: https://earthquakeinsights.substack.com/p/another-quick-update-on-the-mw77
- Focus.it, la "falla silenciosa": https://www.focus.it/scienza/scienze/terremoto-di-magnitudo-7-7-a-panama-perche-si-e-scatenata-la-scossa-piu-forte-mai-registrata-sulla-terraferma

### Historia sísmica y amenaza
- Universidad de Panamá, Tecnociencia (sismo de 1913, falla Azuero-Soná): https://revistas.up.ac.pa/index.php/tecnociencia/article/download/6649/5138/10975
- El Nuevo Día, energía acumulada durante un siglo: https://www.elnuevodia.com/noticias/mundo/notas/terremoto-en-panama-libero-energia-acumulada-durante-un-siglo-afirma-geologo/
- La Prensa, la energía acumulada en un siglo: https://www.prensa.com/sociedad/la-energia-acumulada-en-un-siglo-que-se-libero-en-el-terremoto-en-panama/
- La Estrella de Panamá, el sismo de 1882: https://www.laestrella.com.pa/panama/publicando-historia/tragedia-en-1882-asi-fue-el-sismo-mas-devastador-de-panama-NG23610058
- La Estrella de Panamá, riesgo sísmico de la ciudad de Panamá: https://www.laestrella.com.pa/panama/nacional/entendiendo-el-riesgo-sismico-de-la-ciudad-de-panama-GI23814460
- Rockwell et al. (2010), paleosismología de la falla de Pedro Miguel: https://www.earthconsultants.com/pdf/Rockwell_etal_2010_Panama.pdf
- Panamá América, edificios altos y la falla de Pedro Miguel: https://www.panamaamerica.com.pa/sociedad/edificios-mas-altos-de-panama-estan-cimentados-sobre-roca-pero-la-falla-de-pedro-miguel
- Banco Mundial, percepción del riesgo sísmico en Panamá: https://blogs.worldbank.org/es/latinamerica/panam-planificar-preparar-mitigar-acciones-clave-en-la-prevenci-n-de-desastres

### Daños, víctimas y respuesta
- Diario del Sur (EFE), primera víctima mortal: https://www.diariodelsur.com.co/noticias/terremoto-de-panama-deja-su-primera-victima-mortal-dias-despues-del-sismo
- Minuto60, víctimas mortales: https://www.minuto60.com/mundo/terremoto-panama-cuantos-muertos-deja-quienes-son-las-victimas/18133
- La Prensa, balance en vivo del Gobierno: https://www.prensa.com/politica/en-vivo-gobierno-actualiza-informe-sobre-el-terremoto-en-panama/
- Primicias (EFE), damnificados y albergues: https://www.primicias.ec/internacional/terremoto-panama-damnificados-piden-agilizar-ayuda-134657/
- Excelsior (AFP), comunidades aisladas: https://www.excelsior.com.mx/internacional/terremoto-panama-comunidades-aisladas
- CRHoy, comunidades aún aisladas: https://crhoy.com/mundo/pequenas-comunidades-golpeadas-por-terremoto-en-panama-aun-siguen-aisladas/
- La Prensa, Isla Cañas, Búcaro y Tonosí: https://www.prensa.com/politica/entre-galeras-cartones-y-carpas-la-tragedia-se-prolonga-en-isla-canas-bucaro-y-tonosi/
- Panamá América, la emergencia continúa (Los Pozos): https://www.panamaamerica.com.pa/nacion/el-sismo-paso-pero-la-emergencia-continua-1281777
- Rio Times, reparación de puentes: https://www.riotimesonline.com/panama-quake-bridge-repairs-14-more-public-works-2026/
- AP vía ADN, estado de emergencia: https://www.adn.com/nation-world/2026/10/10/panama-declares-a-state-of-emergency-as-powerful-quake-aftershocks-rattle-communities/
- Star-Advertiser (AP), más de 200 réplicas: https://www.staradvertiser.com/2026/10/11/breaking-news/panama-suffers-over-200-aftershocks-from-fridays-7-7-magnitude-earthquake/
- Infobae (EFE), USD 61 M para hospitales: https://www.infobae.com/panama/2026/10/13/panama-destinara-61-millones-a-reparar-hospitales-danados-por-terremoto/

### Construcción y normas
- Panamá América, propuesta de revisión del REP: https://www.panamaamerica.com.pa/nacion/proponen-revision-del-rep-sismo-sera-caso-de-estudio-1267560
- Panamá América, viviendas unifamiliares y normas: https://www.panamaamerica.com.pa/sociedad/viviendas-unifamiliares-expertos-insisten-en-cumplir-las-normas-de-construccion-1267638
- La Prensa, auditar edificaciones anteriores a 1984: https://www.prensa.com/economia/urge-auditar-edificaciones-construidas-antes-de-1984-ante-riesgo-sismico-en-panama-exigen-expertos/

### Economía, finanzas y seguros
- Infobae, déficit de hasta USD 2,000 M: https://www.infobae.com/panama/2026/11/12/terremoto-en-panama-puede-generar-un-deficit-de-hasta-usd-2000-millones-estiman-economistas/
- CR Prensa, la misma estimación: https://crprensa.com/2026/11/12/terremoto-en-panama-podria-generar-un-deficit-de-hasta-usd-2-000-millones-segun-economistas/
- La Estrella de Panamá, fideicomisos y política fiscal: https://www.laestrella.com.pa/economia/terremoto-en-panama-pueden-los-fideicomisos-blindar-la-politica-fiscal-OD26614965
- La Estrella de Panamá, Azuero pide USD 80 M: https://www.laestrella.com.pa/economia/azuero-pide-80-millones-para-reconstruccion-tras-el-sismo-JD27249426
- Bloomberg Línea, dos fideicomisos: https://www.bloomberglinea.com/latinoamerica/panama/panama-pone-en-marcha-dos-fideicomisos-para-la-ayuda-humanitaria-y-la-reconstruccion-tras-el-sismo/
- Telemetro, el MEF descarta por ahora el Fondo de Ahorro: https://www.telemetro.com/nacionales/terremoto-panama-mef-descarta-ahora-utilizar-el-fondo-ahorro-y-anuncia-fideicomiso-n6095116
- La Prensa, préstamos a contratistas: https://www.prensa.com/economia/gobierno-prestara-dinero-a-contratistas-para-construir-viviendas-y-otras-obras-por-el-terremoto-con-fondos-del-fideicomiso/
- Bruno Masi, gestiones con multilaterales: https://www.brunomasi.com.py/noticias/terremoto-en-panama-el-gobierno-pide-auxilio-financiero-r8fidy
- La Estrella de Panamá, 6,865 siniestros: https://www.laestrella.com.pa/economia/aseguradoras-reportan-mas-de-6-mil-reclamos-tras-el-sismo-del-9-de-octubre-HG27213510
- La Estrella de Panamá, seguros contra terremotos: https://www.laestrella.com.pa/economia/seguros-contra-terremotos-en-panama-la-proteccion-que-muchos-desconocian-DB27158193

### Patrimonio
- La Estrella de Panamá, iglesias afectadas y MiCultura: https://www.laestrella.com.pa/vida-y-cultura/que-iglesias-resultaron-afectadas-por-el-sismo-micultura-coordina-su-recuperacion-MM26914282
- Revista Summa, daños en bienes patrimoniales: https://revistasumma.com/panama-evalua-el-alcance-de-los-danos-que-causo-el-terremoto-en-los-bienes-patrimoniales/
- La Prensa, iglesia de San Atanasio: https://www.prensa.com/sociedad/iglesia-de-san-atanasio-en-la-villa-retiran-piezas-en-riesgo-tras-el-terremoto/
