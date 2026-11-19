# IA, analítica geoespacial y datos para abrir tiendas de ~250 m² en Panamá: métodos, fuentes, herramientas, casos y modelo comercial para "Lativium para supermercados"

> Notas de investigación (fecha de corte: 19-nov-2026). Advertencia metodológica: en esta sesión **WebFetch no pudo abrir páginas externas** (DNS bloqueado para expansion.mx, colombiaretail.com, inkl.com y book.st-hakky.com). Por eso todo lo que sigue sale de resúmenes de resultados de búsqueda y no de la lectura del texto completo. Las cifras deben verificarse en la fuente antes de citarlas a un cliente. Etiquetas usadas: **[Vendor]** = afirmación de un proveedor sin auditoría independiente; **[Académico]** = estudio publicado; **[Prensa]** = medio de comunicación; **[Oficial]** = fuente gubernamental o de la empresa.

## 1. Métodos de selección de sitios y áreas de influencia, y cómo los usan OXXO, Walmart, D1, Mass, Dollar General, 7-Eleven, Lawson y Starbucks

### Takeaway
Los grandes operadores de proximidad no publican sus algoritmos. Lo documentado es que combinan mapeo territorial periódico, modelos de potencial y canibalización, y cada vez más IA. Desde 2024-2026 el foco se movió de "abrir rápido" a "productividad por tienda" (OXXO cierra tiendas que "probablemente no deberían existir"). Los resultados verificables de precisión vienen sobre todo de la academia (modelos de tiendas de conveniencia con un 70-76 % de acierto al clasificar éxito o fracaso) y de proveedores (Buxton, CARTO), no de auditorías independientes.

### Cited Findings
**Métodos (base técnica)**
- Modelo de Huff: en el modelo de ArcGIS Business Analyst los exponentes por defecto son arbitrarios y pueden no servir para un área concreta, así que hay que **calibrarlo**. La calibración también debe considerar la "fuga" del gasto de abarrotes hacia tiendas de conveniencia, mercados y delivery [Oficial/Vendor, documentación Esri] — [Esri: How Huff Model works](https://pro.arcgis.com/en/pro-app/2.7/tool-reference/business-analyst/understanding-huff-model.htm); [Esri whitepaper Calibrating Huff Model](https://esri.com/library/whitepapers/pdfs/calibrating-huff-model.pdf)
- Huff dinámico (T-Huff) calibrado con datos de visitas de teléfonos móviles para tres cadenas en 10 ciudades de EE. UU. Para Whole Foods, la correlación de Pearson con las visitas observadas fue 0,864 (α=0,717; β=0,805), y la versión temporal superó al Huff estático. La cifra mide probabilidad de visita, no ventas [Académico, 2020] — [Liang et al., arXiv 2003.10857](https://arxiv.org/pdf/2003.10857); [versión TGIS 2020](https://geography.wisc.edu/geods/wp-content/uploads/sites/28/2022/05/2020_TGIS_DynamicHuffModel.pdf)
- Un estudio de 2020 se presenta como la primera validación del modelo de Huff contra transacciones reales y reporta buen ajuste para supermercados, ropa, gasolineras y restaurantes. El texto completo está tras paywall y sus métricas de error no se verificaron [Académico, 2020] — [Big Data journal, doi 10.1089/big.2020.0161](https://journals.sagepub.com/doi/10.1089/big.2020.0161)
- Optimización de red: el problema de cobertura máxima (MCLP) maximiza la demanda cubierta con presupuesto o número de tiendas fijo, y el p-median minimiza la distancia ponderada. El MCLP es NP-hard y se resuelve con heurísticas o solvers [Académico] — [Operational Research: Methods and Applications, arXiv 2303.14217](https://arxiv.org/pdf/2303.14217); [Budget Constrained Generalized MCLP](https://www.researchgate.net/publication/271921265_An_Iterated_Local_Search_for_the_Budget_Constrained_Generalized_Maximal_Covering_Location_Problem). No encontré un caso publicado de MCLP o p-median aplicado a una red real de conveniencia o supermercado.
- Machine learning para tiendas de conveniencia:
  - Estudio de 2025 (Scientific Reports) con 96 tiendas de una cadena: precisión de 61,83-68,75 % con todas las variables y de **70,00-76,25 % con MTS-XGBoost** tras filtrar variables [Académico, 2025] — [Nature Sci Rep s41598-025-30650-w](https://www.nature.com/articles/s41598-025-30650-w)
  - Estudio de 2022 (Applied Sciences, ANN + text mining). Define "éxito" como ventas reales >90 % de las proyectadas. La línea base de acierto era 55 % y el modelo la subió en 18,2 % [Académico, 2022] — [Applied Sciences 12(6):3036](https://doi.org/10.3390/app12063036)
  - Un ensamble GBDT/XGBoost/LightGBM para predecir "hot-spots" comerciales reporta precisión de 0,91 [Académico, 2025] — [ScienceDirect S2666764925000098](https://www.sciencedirect.com/science/article/pii/S2666764925000098)
  - En pronóstico de ventas no hay un ganador universal: un estudio con random forest ajustado (R² 0,942) superó a gradient boosting por 0,3-0,6 %, y en otro CatBoost y LightGBM se alternan según el período [Académico, 2024] — [arXiv 2410.13773](https://arxiv.org/pdf/2410.13773); [ENIAC – Comparing Gradient Boosting Algorithms](https://sol.sbc.org.br/index.php/eniac/article/download/25731/25547)
- Canibalización: una regla práctica de proveedores es suponer que 50-70 % de los clientes en el área de influencia superpuesta es demanda **transferida**, no incremental [Vendor] — [geod: Cannibalization analysis](https://www.geod.app/blog/cannibalization-analysis-site-selection); [GrowthFactor: Market saturation](https://www.growthfactor.ai/resources/blog/market-saturation-analysis-trade-area)

**Cómo lo usan los retailers (documentado)**
- **OXXO/FEMSA:** Expansión (03-ene-2024) afirma que OXXO usa IA para identificar ubicaciones estratégicas, sin detalle técnico [Prensa] — [Expansión](https://expansion.mx/empresas/2024/01/03/un-oxxo-en-cada-esquina-no-basta-nueva-estrategia-femsa). Según Colombia Retail, el DG de OXXO, Carlos Arenas, dijo que cada 4 años la embotelladora de Coca-Cola hace un mapeo del territorio para fijar cuánto puede expandirse OXXO (fecha no visible) [Prensa] — [Colombia Retail: Método Oxxo](https://colombiaretail.com/metodo-oxxo-asi-es-como-femsa-instala-nuevas-tiendas-en-el-mundo/)
- **OXXO, giro 2026:** prioriza rentabilidad por tienda sobre velocidad de apertura y en el 1T-2026 empezó a depurar tiendas de bajo desempeño [Prensa, 2026] — [Xataka MX](https://www.xataka.com.mx/empresas-y-economia/oxxo-cambia-su-estrategia-2026-abrir-tiendas-mexico-para-enfocarse-ventas-aumentar-rentabilidad); [Merca2.0](https://www.merca20.com/femsa-cambia-la-estrategia-de-oxxo-con-cierre-de-tiendas-que-probablemente-no-deberian-existir/)
  - Formato **"OXXO Nicho"** para oficinas, fábricas, complejos residenciales y parques industriales: ~25 % de las aperturas nuevas [Prensa, 17-may-2026] — [El Imparcial](https://www.elimparcial.com/mexico/2026/05/17/femsa-anuncio-el-cierre-de-tiendas-oxxo-que-no-son-rentables-tras-detectar-cambios-en-los-habitos-de-consumo-y-la-empresa-planea-abrir-mil-nuevas-sucursales-bajo-el-formato-de-nicho-para-priorizar-la-productividad-sobre-el-crecimiento-acelerado-de-unidades-en-todo-mexico/)
  - Todavía hay espacio para 900-1.100 tiendas nuevas al año en México (conferencia 1T-2026). La red tenía 24.455 unidades a marzo de 2026 [Prensa, 2026] — [Merca2.0](https://www.merca20.com/femsa-cambia-la-estrategia-de-oxxo-con-cierre-de-tiendas-que-probablemente-no-deberian-existir/); [Xataka MX](https://www.xataka.com.mx/empresas-y-economia/oxxo-cambia-su-estrategia-2026-abrir-tiendas-mexico-para-enfocarse-ventas-aumentar-rentabilidad)
  - Una fuente más débil dice que FEMSA proyecta el tráfico y la evolución de cada zona a 5 y 10 años y que las tiendas nuevas serán "digitales por diseño" (sin confirmar en otras fuentes) [Prensa] — [AmericaMalls & Retail](https://americaretail-malls.com/paises/mexico/oxxo-2026-cierre-de-tiendas-y-apertura-de-1100-unidades/)
  - Un artículo vinculado a FEMSA indica que las decisiones de apertura, cierre e inventario se basan en datos (sin metodología) — [Peter Fisk: OXXO Future Makers](https://www.peterfisk.com/event/oxxo-future-makers-moonshots-dual-thinking-and-courage/)
- **Walmart de México:** al 3T-2026 Bodega Aurrera tenía 2.768 tiendas, de ellas **1.609 Bodega Aurrera Express**, y 36 de las 39 aperturas del trimestre fueron Bodega Aurrera [Prensa, 2026] — [Merca2.0](https://www.merca20.com/walmart-prepara-mas-aperturas-de-tiendas-para-el-cierre-de-2026-el-cuarto-trimestre-concentraria-su-mayor-expansion/). Ampliará la plataforma de "tienda conectada" de Vusion a todas las Walmart Express antes de terminar 2026 [Prensa] — [Xataka MX](https://www.xataka.com.mx/empresas-y-economia/walmart-quiere-tiendas-que-piensen-solas-asi-su-nueva-estrategia-ia-mexico). No encontré una metodología pública de selección de sitios.
- **D1 (Colombia):** unas 2.576 tiendas en más de 500 municipios (2026); otras notas dan hasta 2.745 en unos 550 municipios. Sus criterios públicos son alto tráfico y fácil acceso en barrios residenciales. Empezó en barrios de clase media-alta y después bajó al sur de Bogotá y a Soacha. Su modelo de scoring no es público [Prensa, 2024-2026] — [El Cronista](https://www.cronista.com/colombia/curiosidades/confirmado-d1-revela-la-cifra-exacta-de-tiendas-abiertas-en-mas-de-500-municipios-de-colombia-en-todo-el-pais-consulta-el-listado-completo-y-verifica-si-su-municipio-esta-incluido/); [Cambio](https://cambiocolombia.com/empresas/articulo/2024/11/d1-las-tiendas-de-bajo-costo-que-en-15-anos-dominaron-el-negocio-de-los-supermercados-en); [Colombia Retail](https://colombiaretail.com/tiendas-d1-domina-el-retail-colombiano-con-cifras-record-americamalls-retail/)
- **Mass (InRetail, Perú):** tiendas de unos **150-200 m²** cerca de los hogares. El CEO Juan Carlos Vallejo dijo en 2024 que entrar a una ciudad nueva exige **al menos 60 tiendas** (densidad mínima por ciudad) [Prensa] — [Perú Retail](https://www.peru-retail.com/como-logro-mass-superar-las-1-500-tiendas-en-peru-las-claves-de-su-rapido-crecimiento/). Tenía 1.582 tiendas al 1T-2026, planeaba ~200 aperturas en 2026 y había abierto más de 600 en los dos años anteriores [Prensa, 2026] — [Perú Retail](https://www.peru-retail.com/mass-supera-las-1580-tiendas-en-peru-que-explica-su-expansion/). En el 2T-2026 llegó a 1.602, con 26 aperturas y 166 remodelaciones [Prensa] — [Perú Retail](https://www.peru-retail.com/inretail-refuerza-sus-principales-negocios-pharma-apunta-a-100-aperturas-y-mass-sigue-creciendo/)
- **Dollar General:** no revela sus modelos internos. Ha seguido una estrategia de **canibalización intencional** para capturar inmuebles atractivos. Cada tienda cuesta ~US$500 mil y el retorno de caja ronda los 2 años [Análisis] — [Quartr](https://quartr.com/insights/edge/dollar-general-the-rural-retailer-playbook). Un modelo dinámico de entrada encuentra evidencia clara de canibalización en tiendas de formato pequeño. Entre los motivos de entrada están evitar la canibalización, la exclusión competitiva y la **apropiación preventiva** (preemption) [Académico, 2024] — [Chenarides et al., AJAE 2024](https://onlinelibrary.wiley.com/doi/10.1111/ajae.12404)
- **Starbucks:** usa **Atlas**, una aplicación de planificación de mercado y desarrollo de tiendas construida sobre Esri que incluye un componente de desempeño de tienda [Oficial/Caso] — [Esri Newsroom](https://esri.com/about/newsroom/?p=191052); [Harvard D3](https://d3.harvard.edu/platform-digit/submission/starbucks-brewing-up-a-data-storm/). La cifra que circula de "tiendas nuevas 12 % por encima de lo proyectado" **no tiene fuente** [no verificado] — [blog Knowledge Realm](https://knowledgerealm.beehiiv.com/p/how-starbucks-optimizes-store-locations)
- **7-Eleven y Lawson:** lo documentado es IA de pedidos y operación (ver sección 4), no selección de sitios.
- **Resultados de proveedores:**
  - Buxton: según un agregador, las ubicaciones que recomendó rindieron 12,4 % más que las no recomendadas, y un cliente de rent-to-own bajó de 18 a 6 meses el tiempo hasta la rentabilidad [Vendor/agregador] — [Cuspera: Buxton](https://www.cuspera.com/products/buxton-analytics-platform-x-6496)
  - CARTO + ASDA: elección de sitios para lockers "toyou" (639 ubicaciones, meta de 5.000) con población alcanzable, distancia y cercanía a tiendas propias para evitar canibalización. Los resultados reportados son cualitativos [Vendor] — [CARTO: ASDA](https://carto.com/customer-stories/site-selection-asda/)
  - CARTO también tiene un escenario ilustrativo de dark stores en Seattle con 82 % de cobertura de registros de la app (no es un despliegue real) [Vendor] — [CARTO: dark store site selection](https://carto.com/blog/geospatial-data-for-dark-store-site-selection/)
- **Panamá:** PREDIK Data-Driven calculó que el Super 99 de Vía Porras tiene **571 mil personas a 15 minutos en auto, con un gasto conjunto de ~US$82 millones al mes**. El método son isócronas más datos demográficos, de ingreso y de gasto. El análisis es de alrededor de 2021 [Vendor] — [PREDIK: Supermercados, ¿cómo medir el potencial de sus ubicaciones?](https://predikdata.com/es/supermercados-como-medir-el-potencial-de-sus-ubicaciones/)
- **Caso de fracaso, Justo & Bueno (Colombia, con operación en Panamá):**
  - Abrió más de 500 tiendas en cuatro años y llegó a superar las 1.300, aunque las ventas no alcanzaban para financiar esa expansión.
  - En 2021 tuvo ingresos de COP 1,5 billones y pérdidas de COP 434.961 millones.
  - Entró en liquidación en 2022 con deudas de COP 1,4-1,7 billones (las fuentes difieren). D1 y Ara le quitaron clientes en zonas estratégicas.
  - En Panamá el rescate fracasó y la operación se canceló en noviembre de 2022.
  - [Prensa, 2022] — [Bloomberg Línea (Panamá)](https://www.bloomberglinea.com/2022/11/26/una-reorganizacion-inviable-justo-y-bueno-en-panama-cancela-operaciones/); [La República](https://www.larepublica.co/empresas/la-historia-detras-de-la-quiebra-de-justo-bueno-y-el-perfil-del-nuevo-inversionista-3382224); [Panamá América](https://www.panamaamerica.com.pa/economia/auge-y-caida-de-justo-bueno-por-que-paso-del-exito-la-quiebra-1214883); [Portafolio](https://www.portafolio.co/negocios/empresas/justo-bueno-ha-entregado-casi-1-000-locales-durante-su-liquidacion-571238)

### Inferences
- La práctica de referencia es un **sistema en capas**:
  1. Potencial de demanda por celda (población, ingreso, gasto y flujos).
  2. Huff calibrado o isócronas a pie (5-10 min) para el área de influencia de un formato de 250 m².
  3. Un modelo ML (GBM o random forest) entrenado con tiendas "análogas" para estimar ventas.
  4. Canibalización y optimización de red (MCLP o p-median) para elegir N sitios a la vez.
- Para un formato de proximidad de 250 m² lo decisivo es la **isócrona a pie** y la densidad de hogares, más que el radio en auto. El ejemplo de PREDIK (15 min en auto) corresponde a un supermercado grande, no a una tienda de barrio.
- Los benchmarks académicos (≈70-76 % de acierto al clasificar éxito o fracaso en conveniencia) indican qué precisión es realista prometer. Una oferta creíble debería **comprometer validación retrospectiva** (backtesting con las tiendas existentes del cliente) en lugar de prometer porcentajes de acierto de entrada.
- La señal estratégica 2024-2026 (OXXO Nicho, cierre de tiendas improductivas, el umbral de 60 tiendas por ciudad de Mass, la canibalización intencional de Dollar General, el colapso de Justo & Bueno) justifica vender en Panamá un servicio de **"densidad rentable"**: cuántas tiendas caben por corregimiento sin canibalizar en exceso y en qué orden abrirlas. Justo & Bueno, que también operó en Panamá, sirve de caso local para explicar el riesgo de expandirse sin disciplina analítica.

### Gaps
- No hay documentación pública del algoritmo de sitios de OXXO, Walmex, D1, Mass, 7-Eleven ni Lawson. Las afirmaciones sobre IA de OXXO son de prensa y sin detalle técnico.
- No encontré auditorías independientes de "reducción de tasa de fracaso" de tiendas nuevas atribuibles a IA. Las cifras de Buxton vienen de un agregador o del propio proveedor.
- No pude leer el texto completo de Expansión ni de Colombia Retail (dominios bloqueados en esta sesión).
- No encontré un caso publicado de MCLP o p-median aplicado a supermercados o conveniencia en LatAm.
- Un estudio mencionado en los resultados (random forest con 90-92 % de acierto en ubicaciones de Luckin y Starbucks) no se pudo vincular a una URL verificable y se dejó fuera.

## 2. Fuentes de datos disponibles en Panamá: públicas vs. comerciales y costos aproximados

### Takeaway
Panamá tiene una base pública utilizable y gratuita:
- Censo 2023 por corregimiento y **lugar poblado**, vía REDATAM.
- Capas oficiales de límites.
- Datos abiertos del Metro.
- Overture y OSM.
- La API de Google Places, con cuota gratuita por SKU desde mar-2025.

Lo que falta es geometría pública fina (manzanas, parcelas catastrales). Para movilidad hay al menos un proveedor comercial que declara cobertura de Panamá (PREDIK). No encontré evidencia de que las telcos panameñas ni Yappy vendan datos de movilidad o de transacciones.

### Cited Findings
**Públicas / gratuitas**
- **Censo 2023 (INEC):**
  - Población total de 4.202.572 habitantes [Prensa/Oficial] — [TVN](https://www.tvn-2.com/nacionales/resultado-censo-hay-4-millones-panama_1_2065050.html)
  - INEC publica cuadros del Censo 2023 por provincia, distrito, corregimiento y **lugar poblado** en PDF y Excel (datos tabulares, no espaciales) [Oficial] — [INEC publicaciones](https://www.inec.gob.pa/publicaciones/Default3.aspx?ID_PUBLICACION=1231&ID_CATEGORIA=19&ID_SUBCATEGORIA=71); ejemplo: [Panamá Oeste por lugar poblado (PDF)](https://www.inec.gob.pa/archivos/P0705547520240202082406Panam%C3%A1%20Oeste.pdf)
- **REDATAM / CensosWeb 2023 (INEC):**
  - Consulta y procesamiento en línea de los censos, **gratis**, con filtros por corregimiento y lugar poblado [Oficial] — [Manual CensosWeb 2023](https://www.inec.gob.pa/redpan/RpHelp/Manual_CensosWeb_2023.pdf); [redatam.org: Panamá](https://redatam.org/en/online-process/latam/pan)
  - CEPAL usó esa herramienta para generar tablas del censo de Panamá 2023 [Oficial] — [CEPAL MATERNILAC](https://www.cepal.org/es/notas/actualizacion-maternilac-censo-panama-2023)
  - Hay discrepancias entre totales publicados y REDATAM (1.805.287 vs. 1.795.012 en un agregado analizado) [Académico] — [Universidad de Panamá, Cuadernos de Coyuntura](https://revistas.up.ac.pa/index.php/cuadernos_coyuntura/article/download/5282/4140/8141)
- **Cartografía censal:**
  - El informe metodológico del CNPV 2023 tiene una sección sobre el formato shapefile de la cartografía, pero la mayoría de los mapas se produjeron en papel y la versión digital se usó sobre todo en áreas de difícil acceso [Oficial] — [Informe Metodológico CNPV23](https://www.inec.gob.pa/archivos/Informe%20Metodologico%20CNPV23.pdf)
  - El departamento de cartografía y SIG del INEC mantiene una base de datos cartográfica con viviendas, poblados y barrios [Prensa] — [La Prensa](https://www.prensa.com/economia/el-inec-actualiza-la-informacion-cartografica-para-los-censos-nacionales/)
  - **No encontré descarga pública a nivel de manzana.**
- **Capa Censo 2023 por corregimiento (Esri Panamá / Living Atlas):** polígonos con población total, sexo, edades, educación y otros atributos, consumibles como servicio REST [Vendor/Público] — [MapServer PanamaLivingAtlas](https://ags.esri.co/arcgis/rest/services/PanamaLivingAtlas/Censo_Poblacion_Corregimiento_Panama_2023/MapServer); [ArcGIS item](https://www.arcgis.com/home/item.html?id=0f23a1341c7b4d8699b1e536e7432137)
- **ANATI:**
  - Su servidor ArcGIS publica límites político-administrativos y cabeceras de distritos y corregimientos actualizados a 2024. No encontré una capa pública de parcelas [Oficial] — [sigigntg.anati.gob.pa](https://sigigntg.anati.gob.pa/arcgisserver/rest/services/Mapa_Web_de_Poblados_MIL1/MapServer/layers)
  - Hay un préstamo del Banco Mundial de US$60 millones para modernizar el catastro hacia uno multifinalitario [Prensa] — [La Estrella](https://www.laestrella.com.pa/economia/panama-modernizara-su-sistema-de-catastro-con-prestamo-de-60-millones-del-bm-AP27282893)
  - Se prevé una plataforma única con datos catastrales, registrales y geoespaciales (en desarrollo, 2026) [Prensa] — [La Estrella](https://www.laestrella.com.pa/economia/la-falta-de-datos-sobre-la-tierra-frenan-el-desarrollo-y-encarecen-las-obras-en-la-region-HA27362656)
  - En 2024 hubo una falla en los servidores de ANATI [Oficial] — [ANATI nota de prensa](https://anati.gob.pa/images/noticias/2024/Nota_prensa_servidores.pdf)
  - La IPDE (infraestructura panameña de datos espaciales) fue creada por el Decreto Ejecutivo 51 de 2013 [Oficial] — [CEPAL: IPDE Panamá](https://cepal.org/sites/default/files/presentations/panama-infraestructura-datos-geoespaciales.pdf)
- **Metro de Panamá:**
  - Datos abiertos de demanda de las Líneas 1 y 2 por días laborables, sábados y feriados, de 2018 a 2024 (actualización del 17-may-2024), con una versión más reciente hasta 2026. Son **por línea y mes, no por estación** [Oficial] — [datosabiertos.gob.pa: Metro de Panamá](https://www.datosabiertos.gob.pa/dataset/?organization=metro-de-panama)
  - Para estaciones solo hay una fuente secundaria (Wikipedia, basada en la Memoria Anual): Albrook concentró 10,97 % de las transacciones de la Línea 1, y Cerro Viento, 24 de Diciembre y Nuevo Tocumen estuvieron entre las 5 más usadas en 2024 — [Wikipedia L1](https://es.wikipedia.org/wiki/L%C3%ADnea_1_(Metro_de_Panam%C3%A1)); [Wikipedia L2](https://es.wikipedia.org/wiki/L%C3%ADnea_2_(Metro_de_Panam%C3%A1))
- **Overture Maps (Places):** puntos de negocios y servicios con licencia CDLA Permissive 2.0 (ODbL para lo derivado de OSM), gratuito [Público] — [Overture Places guide](https://docs.overturemaps.org/guides/places); [Atlas: Overture](https://atlas.co/data-sources/overture-maps/). Un proveedor lista **34.245 places en Panamá**, cifra no verificada y contradictoria con otra página del mismo proveedor [Vendor] — [openplacesapi coverage](https://openplacesapi.com/coverage.md)
- **Google Maps Platform:** desde el **1-mar-2025** el crédito mensual de US$200 se reemplazó por cuotas gratuitas por SKU: 10.000 llamadas/mes en Essentials, 5.000 en Pro y 1.000 en Enterprise. Places API, Directions y Distance Matrix pasaron a "Legacy" y sus sucesores son Places API (New) y Routes API [Oficial] — [Google FAQ de cambios](https://developers.google.com/maps/billing-and-pricing/faq); [Google pricing overview](https://developers.google.com/maps/billing-and-pricing/overview)
- **Luces nocturnas / satélite como proxy de ingreso:**
  - Hay aplicaciones en LatAm: Brasil, con deep learning sobre imágenes diurnas y nocturnas, a nivel de ciudad [Académico] — [USP](https://repositorio.usp.br/bitstreams/c6e049cc-be66-4fcd-a862-5e58edd74bdb); Medellín, intraurbano, combinando luces, encuestas y estimación de áreas pequeñas [Académico] — [U. del Rosario](https://repository.urosario.edu.co/bitstreams/13005dab-c753-45de-93bf-0368b802d700/download)
  - Literatura del Banco Mundial advierte que la relación entre luces e ingreso o salario a escala fina es débil [Académico] — [World Bank OKR](https://openknowledge.worldbank.org/bitstreams/ec4a4124-9063-4329-9da8-5b2afcf18467/download)

**Comerciales**
- **PREDIK Data-Driven** (antes CentralAmericaData; cambio de marca en ene-2022):
  - Su dataset de ubicación móvil lista cobertura de **EE. UU., México, Costa Rica, El Salvador, Guatemala, Honduras, Nicaragua y Panamá** [Vendor] — [Datarade: PREDIK data products](https://datarade.ai/data-providers/centralamericadata/data-products); [CentralAmericaData → PREDIK](https://centralamericadata.com/es/article/home/CentralAmericaData_ahora_es_PREDIK_DataDriven)
  - Ofrece footfall, tasa de visitas, dwell time e isócronas con población, ingreso, gasto mensual e intereses [Vendor] — [PREDIK Retail Footfall](https://predikdata.com/retail-footfall-analytics/); [PREDIK Retail BI](https://predikdata.com/es/inteligencia-de-negocios-industria-retail/)
  - Una reseña de un cliente (sobre Australia, no Panamá) advierte los sesgos y vacíos habituales de los datos de dispositivos — [Datarade profile](https://datarade.ai/data-providers/centralamericadata/profile)
  - Precio no publicado.
- **Kido Dynamics:** trabaja con datos de señalización de operadores móviles, anonimizados y agregados. Dice operar en más de 15 países de Europa, LatAm, Medio Oriente y Asia, sin listarlos; **no confirmé Panamá** [Vendor] — [Venturelab](https://www.venturelab.swiss/kido-dynamics); [kidodynamics.com](https://www.kidodynamics.com/). Un estudio en México usó sus datos de telefonía de agosto de 2023 [Caso] — [Cal y Mayor 2024 (PDF)](https://www.calymayor.com.mx/mx/assets/perspectivas/Grupo%20Cal%20y%20Mayor%20-%20Implementaci%C3%B3n%20de%20Big%20Data%202024.pdf)
- **Grandata:** desarrolló con el PNUD (2020) una herramienta de movilidad por país, estado y municipio, y aportó datos para un estudio de 314 ciudades latinoamericanas. No encontré datos específicos de Panamá [Oficial/Académico] — [PNUD + Grandata](https://www.undp.org/latin-america/press-releases/undp-and-grandata-join-forces-tool-addressing-public-policy-decision-supported-data); [Salud Digital: 314 ciudades](https://saluddigital.com/plataformas-digitales/estudio-analizo-la-movilidad-de-314-ciudades-de-latinoamerica-durante-la-pandemia-con-datos-de-telefonos-moviles/)
- **Placer.ai:** su plataforma está centrada en EE. UU. y su utilidad fuera de ese país es limitada; no tiene cobertura confirmada en LatAm [Vendor/Reseña] — [placer.ai](https://www.placer.ai/); [BestCRE review](https://bestcre.com/placer-ai-review-cre-ai/)
- **Telcos (Más Móvil, Tigo, Claro, Digicel):** no encontré productos de datos de movilidad para empresas. Los informes de IPANDETEC (2020, 2022, 2024) evalúan como débiles las políticas de privacidad y transparencia de los ISP panameños [ONG] — [EFF/IPANDETEC 2024](https://www.eff.org/deeplinks/2024/10/new-ipandetec-report-shows-panamas-isps-still-lag-protecting-user-data); [EFF/IPANDETEC 2022](https://www.eff.org/deeplinks/2022/06/new-ipandetecs-report-features-isps-privacy-best-practices-and-flaws-panama?language=en)
- **Yappy (Banco General):**
  - Más de 1,8 millones de clientes y unos 34 mil comercios [Prensa] — [La Prensa](https://www.prensa.com/economia/yappy-amplia-su-alcance-en-el-sistema-bancario-panameno/); [Banco General](https://www.bgeneral.com/yappy/)
  - 40 millones de transacciones al mes (may-2025) [Prensa] — [MetroLibre](https://www.metrolibre.com/economia/yappy-registra-40-millones-de-transacciones-al-mes-JN12680180)
  - Los pagos de personas a comercios promediaron ~US$101 millones al mes en 2024 [Prensa] — [EcoTV](https://www.ecotvpanama.com/economia-inteligente/programas/yappy-aspira-que-panamasea-un-referente-pagos-digitales-la-region-n6092177)
  - **No encontré un producto de datos agregados de transacciones a la venta.**
- **Delivery:** PedidosYa declara a Panamá mercado estratégico de quick commerce (abr-2026) [Prensa] — [DPL News](https://dplnews.com/panama-pedidosya-apuesta-por-el-quick-commerce-para-consolidar-su-crecimiento/). Más de 14 millones de personas usaron apps para compras de supermercado en LatAm en 2025 (cifra regional de PedidosYa) [Prensa] — [El Dinero](https://eldinero.com.do/345188/compras-ultrarrapidas-transforman-habitos-de-consumo-en-rd-y-la-region/). No encontré venta de datos de pedidos por zona.
- **Marco legal:** la Ley 81 de 2019 y su reglamento (Decreto Ejecutivo 285 de 2021) exigen consentimiento previo e informado y principios de finalidad y proporcionalidad, y ANTAI supervisa su cumplimiento [Oficial/Legal] — [Kraemer Law](https://kraemerlaw.com/en/articles/law-81-of-2019-about-protection-of-personal-data-in-panama/); [Órgano Judicial (2026)](https://www.organojudicial.gob.pa/uploads/blogs.dir/28/2026/06/913/la-proteccion-de-datos-personales-en-la-republica-de-panama.pdf); [ANTAI comunicado](https://www.antai.gob.pa/wp-content/uploads/2023/02/COMUNICADO-2-2-2023-1.pdf)

### Inferences
- La **columna vertebral gratuita** para Panamá sería:
  - Censo 2023 por lugar poblado (REDATAM), unido a la geometría de corregimientos (ANATI y Esri Living Atlas) y repartido a una grilla H3 con proxies de densidad: huellas de edificios de Overture u OSM, como técnica de *dasymetric mapping*.
  - Puntos de interés de Overture, OSM y Google Places (New) para la competencia: Super 99, Rey/Romero, Xtra, El Machetazo, minisúper y farmacias. La cuota gratuita de Google probablemente basta para un piloto, pero hay que verificar los términos de uso que limitan almacenar datos de Google.
  - Metro (por línea, y por estación si se piden las Memorias Anuales) como proxy de flujo peatonal en los nodos.
- La **capa comercial diferenciadora** sería movilidad de dispositivos (PREDIK es el candidato con cobertura declarada de Panamá) más los **datos propios del cliente**: ventas por tienda y SKU, tarjetas de lealtad con dirección o corregimiento, y pedidos a domicilio geocodificados. Los datos propios suelen ser la fuente de mayor valor para calibrar Huff y ML.
- Como no hay catastro público por parcela, la evaluación de locales concretos (renta, frente, estacionamiento, visibilidad) debe venir de **trabajo de campo y brokers**, idealmente capturado con un formulario móvil georreferenciado.
- Yappy y los bancos son una oportunidad de alianza (insights agregados), no una fuente disponible hoy. Cualquier uso de datos de ubicación o de transacciones debe diseñarse con la Ley 81 (agregación, anonimización, finalidad) desde el inicio.

### Gaps
- No confirmé si INEC publica shapefiles de lugar poblado, segmento o manzana del Censo 2023. Hay que consultar al departamento de cartografía del INEC.
- No encontré afluencia oficial por estación del Metro en datos abiertos (hay que revisar la Memoria Anual o pedirla).
- No obtuve precios de PREDIK, Kido, Grandata ni Unacast/Near-Azira para Panamá. No encontré información de Unacast ni de Near/Azira en esta búsqueda.
- No encontré oferta de datos de movilidad de Más Móvil, Tigo, Claro ni Digicel, ni datos de tarjetas (Banco General, Yappy, otros) a la venta.
- No verifiqué la cobertura real de Overture o Google Places para minisúper y abarroterías informales en Panamá; es probable que esté subrepresentada (inferencia).
- No investigué datasets de MIVIOT (permisos de construcción o proyectos de vivienda) por falta de tiempo; serían útiles para proyectar demanda futura.

## 3. Herramientas y plataformas: CARTO, Esri Business Analyst, Placer.ai, Kepler.gl, H3, stack Python y proveedores de geomarketing en LatAm

### Takeaway
Hay tres niveles:
1. **Suites empresariales con precio de lista o cotización:** Esri Business Analyst desde ~US$700 por usuario al año (Standard) y US$5.200 (Advanced); CARTO por cuota anual de consumo cotizada; Placer.ai centrado en EE. UU.
2. **Stack open source gratuito:** H3, kepler.gl, GeoPandas, OSMnx y scikit-learn o XGBoost.
3. **Proveedores regionales:** PREDIK en Centroamérica y Panamá; Zonia y Mexico GIS Data en México.

Para Lativium, lo realista es un stack open source o en la nube con datos públicos y comerciales selectivos, y Esri o CARTO solo si el cliente ya los tiene.

### Cited Findings
- **ArcGIS Business Analyst Web** [Oficial/Marketplace]:
  - Standard desde **US$700 por usuario al año** y Advanced Bundle a **US$5.200 por usuario al año** — [Microsoft Marketplace](https://marketplace.microsoft.com/en-us/product/esri.arcgis-business-analyst-web?tab=PlansAndPrice); [AWS Marketplace](https://aws.amazon.com/marketplace/pp/prodview-kkpfgbxfp6qde)
  - Business Analyst Pro (escritorio) aparece a US$9.010 al año con paquete de datos estatal de EE. UU. y US$14.365 con paquete regional, según una lista de precios de contrato estatal de 2024 — [WA DES Esri price list 11/24](https://apps.des.wa.gov/contracting/09121_ESRI_Pricelist_11_24.pdf)
  - Incluye herramientas de Huff y calibración del Huff con datos reales — [Esri Huff](https://pro.arcgis.com/en/pro-app/2.7/tool-reference/business-analyst/understanding-huff-model.htm)
- **CARTO:** precios empresariales cotizados, por cuota anual de uso estimada según usuarios y casos de uso, sin precio de lista [Vendor] — [CARTO pricing](https://carto.com/pricing/); [CARTO blog: consumption pricing](https://www.carto.com/blog/the-per-seat-trap-consumption-pricing-spatial-analytics/); [Capterra](https://www.capterra.com/p/140192/CartoDB/pricing/)
- **Placer.ai:** sin precio publicado. Un tercero lo estima en US$5.000-30.000 al año (no verificado) [Estimación de terceros] — [SoftwareFinder](https://softwarefinder.com/analytics-software/placer-ai)
- **SiteZeus** (según un competidor): contratos empresariales de más de US$20 mil al año [Vendor competidor] — [GrowthFactor vs SiteZeus](https://www.growthfactor.ai/compare/growthfactor-vs-sitezeus). **GrowthFactor**: tier de entrada de ~US$200 al mes (la nomenclatura del plan difiere entre fuentes) [Vendor/terceros] — [Toolradar](https://toolradar.com/tools/growthfactor/pricing). Kalibrate: solo precios empresariales, no publicados — [GrowthFactor vs Kalibrate](https://www.growthfactor.ai/compare/growthfactor-vs-kalibrate)
- **H3 (Uber, open source):**
  - Índice hexagonal de 64 bits con 16 resoluciones; cada resolución más fina tiene celdas de 1/7 del área.
  - La función k-ring obtiene los vecinos a distancia k, útil para áreas de influencia.
  - kepler.gl entiende identificadores H3 de forma nativa.
  - [Oficial] — [Uber Engineering: H3](https://www.uber.com/us/en/blog/h3/)
- **Proveedores de LatAm:**
  - PREDIK Data-Driven (Centroamérica, Panamá y México): geomarketing con isócronas, footfall y datos de consumo [Vendor] — [PREDIK](https://predikdata.com/es/inteligencia-de-negocios-industria-retail/)
  - Zonia (México): plan básico de **MXN 2.500 por zona**, estudio a la medida desde **MXN 26.500**; cita MXN 30.000-80.000 como rango típico de una consultora [Vendor] — [zonia.mx](https://zonia.mx/)
  - Mexico GIS Data: bases de geomarketing por zona metropolitana a $5.200 (CDMX a $6.000; moneda presumiblemente MXN) [Vendor] — [mexicogisdata.com](https://mexicogisdata.com/base-de-datos-geomarketing-mexico/)
  - "Asesor en Geomarketing" (independiente, México): paquetes desde $5.400 antes de IVA [Vendor] — [catálogo](https://geoalex1769.github.io/)
  - Servinformación (Perú/Colombia) aparece en prensa peruana promoviendo el geomarketing comercial [Prensa] — [Gestión](https://gestion.pe/tendencias/que-es-el-geomarketing-y-que-beneficios-tiene-en-los-procesos-comerciales-estrategias-marketing-emprendedores-noticia/)
  - Blackprint (México) publica guías de geomarketing y costos de estudios [Vendor] — [Blackprint: geomarketing en México](https://www.blackprint.ai/guias/geomarketing-en-mexico)
- **Forecasting y reabastecimiento en LatAm:** RELEX Solutions es el proveedor elegido por OXXO México, OXXO Internacional (LatAm) y la división Bara de FEMSA Proximity [Vendor/Oficial] — ver sección 4.

### Inferences
- **Stack recomendado para Lativium**, en orden de menor a mayor costo:
  1. Python: GeoPandas, H3, OSMnx o OpenRouteService para isócronas a pie, y scikit-learn, XGBoost o LightGBM para el scoring.
  2. Un data warehouse en la nube (BigQuery, Snowflake o Postgres/PostGIS).
  3. kepler.gl o un dashboard web para el cliente.
  4. CARTO o Esri BA solo si el cliente ya tiene licencias o prefiere software "de marca". Esri BA Web Standard (~US$700/año) es asequible, pero sus paquetes de datos demográficos para Panamá no se verificaron.
- La diferenciación de Lativium no estaría en la herramienta, que es commodity, sino en **ensamblar datos panameños** (REDATAM por lugar poblado, Metro, POIs locales, movilidad de PREDIK, datos propios del cliente) y en la **calibración con tiendas reales**.
- H3 permite presentar al cliente un "mapa de espacio en blanco" por hexágono y generar fichas de sitio comparables.

### Gaps
- No encontré información sobre "Datlas", "Urbanist" ni "Geoinsights" como proveedores de geomarketing en LatAm (posibles nombres incorrectos o de baja visibilidad web).
- No hay precios públicos de CARTO ni de Placer.ai. No verifiqué la disponibilidad ni el costo de los datos demográficos de Esri para Panamá.
- No encontré proveedores de geomarketing con sede en Panamá aparte de PREDIK (regional). Habría que buscar en directorios locales o en LinkedIn.
- No encontré documentación específica de OSMnx ni de OpenRouteService en esta búsqueda (son herramientas conocidas, pero no quedaron citadas aquí).

## 4. Casos de uso de IA más allá de la selección de sitio para que funcione una tienda de 250 m², con cifras de impacto

### Takeaway
En proximidad, el caso de IA mejor documentado es el **pronóstico y pedido automático por tienda**. Ejemplos: OXXO con RELEX (+8 pp de precisión de pronóstico en cerveza), Lawson AI.CO en más de 14 mil tiendas, Ito-Yokado (−30 % de tiempo de pedido y −20 % de quiebres en piloto).

Le siguen:
- Perecederos con pedidos asistidos (Afresh: −25 % de merma promedio [Vendor]; −14,8 % de desperdicio por tienda en pilotos multi-proveedor de una colaboración sectorial).
- Rebajas dinámicas (Wasteless: −30 a −40 % [Vendor]; un modelo de UCSD estima −21 % de desperdicio y +3 % de margen).
- Visión por computadora para disponibilidad en góndola (−20 a −35 % de quiebres [Vendor]).
- Surtido localizado (+2 a +5 % de ventas según McKinsey/QuantumBlack).

Casi todas las cifras son de proveedores.

### Cited Findings
**Pronóstico y reabastecimiento**
- **OXXO + RELEX:**
  - Selección en sep-2023 para ~22.000 tiendas en México; arranque en oct-2023 con piloto de 13 categorías, incluyendo pronóstico por clima y promociones; olas en may-jun 2024.
  - Resultados: **+8 pp de precisión de pronóstico en cerveza** y +4,8 pp en bebidas deportivas, con menos trabajo manual.
  - OXXO adoptó luego también el reabastecimiento de RELEX [Vendor, 2023-2024] — [RELEX: OXXO case](https://www.relexsolutions.com/resources/case-study-oxxo/); [BusinessWire sep-2023](https://www.businesswire.com/news/home/20230907493161/en)
  - OXXO Internacional (LatAm) anunció la expansión en abr-2024; antes su cadena de suministro dependía de procesos manuales [Oficial/Vendor] — [BusinessWire abr-2024](https://www.businesswire.com/news/home/20240415433716/en/OXXO-Internacional-Enhances-Retail-Operations-with-RELEX-Solutions-for-Forecasting-and-Replenishment)
  - La división Bara de FEMSA Proximity también eligió RELEX (jun-2024) — [BusinessWire jun-2024](https://www.businesswire.com/news/home/20240626649625/en)
- **Lawson (Japón):**
  - Sistema "AI.CO" desplegado a nivel nacional en jul-2024 en más de 14.000 tiendas para equilibrar desperdicio por sobrepedido y ventas perdidas por quiebre.
  - Pedido "semi-automático" con IA desde 2015.
  - No hay cifras públicas de impacto [Oficial/secundaria] — [Lawson DX Strategy (IR 2020)](https://www.lawson.jp/en/ir/library/annual_report/2020/pdf/ar2020_P22-23.pdf); [note.com case compilation](https://note.com/masamasa11_12/n/n67fae3ae20c8?hl=en)
  - Lawson prueba IA y robótica en una tienda piloto (nov-2025) [Prensa sectorial] — [NACS](https://www.convenience.org/stay-current/news/2025/november/20/4-japans-lawson-banks-on-ai-and-robotics_tech)
- **Ito-Yokado (Seven & i):**
  - Pedido asistido por IA en unas 130 tiendas. Antes, el personal dedicaba unos 40 min al día a pedir 400 ítems.
  - En la demostración piloto el tiempo bajó ~30 % y la tasa de quiebre ~20 % [Prensa] — [inkl](https://inkl.com/news/ito-yokado-introduces-ai-aided-stocking-system-at-all-stores) (no se pudo abrir la página; cifra tomada del resumen de búsqueda)
  - Seven-Eleven Japan introdujo pedido con IA en toda su red (~21.000 tiendas) desde 2023, sin porcentaje de ahorro publicado [secundaria] — [st-hakky case study](https://book.st-hakky.com/en/industry/ai-ordering-convenience-store-case-study). **No encontré fuente para el "40 % menos de tiempo de pedido" que suele atribuirse a 7-Eleven.**
- **B-Luck (Brycen) en Nodake Shokai (supermercados, Japón):** ~30 % menos tiempo de pedido, equivalente a 900 horas al mes en toda la cadena [Vendor, may-2026] — [washinmura](https://aeo.washinmura.jp/ai/%E6%A0%AA%E5%BC%8F%E4%BC%9A%E7%A4%BE%E3%83%96%E3%83%A9%E3%82%A4%E3%82%BB%E3%83%B3/en/news/2026-05-19-brycens-b-luck-implemented-at-nodake-sho?lang=ja)

**Perecederos: pedidos y merma**
- **Afresh:**
  - Promedios declarados: −25 % de merma, +3 % de ventas, +7 % de rotación [Vendor] — [Yespress](https://yespress.io/afresh); [Afresh IDC Innovator 2026](https://www.afresh.com/resources/afresh-named-a-2026-idc-innovator/case-study)
  - Heinen's: US$1 millón de ahorro anualizado, −70 pb de merma y +1,4 % de ventas [Vendor] — [Afresh: Heinen's](https://www.afresh.com/resources/case-study/how-heinens-transformed-fresh-with-ai-powered-replenishment)
- **Pacific Coast Food Waste Commitment** (colaboración multi-actor, más independiente que un proveedor): pilotos 2020-2022 en más de 1.300 tiendas con Afresh y Shelf Engine, con **−14,8 % de desperdicio promedio por tienda** — [PCFWC Case Study (dic-2022)](https://pacificcoastcollaborative.org/wp-content/uploads/2022/12/PCFWC-Case-Study_AI_Final.pdf)

**Precios dinámicos y rebajas**
- **Wasteless** [Vendor/afiliado]:
  - Minorista español: −32 % de desperdicio — [Wasteless](https://wasteless.com/success/leading-spanish-retailer-cuts-waste-by-32)
  - Hoogvliet (Países Bajos): −30 % de desperdicio y −50 % de costo de rebajas — [Supercool newsletter](https://supercool.beehiiv.com/p/wasteless-turns-expiring-food-into-profit-for-grocers-worldwide)
  - "Hasta −40 %" según la empresa — [NoCamels 2022](https://nocamels.com/2022/09/supermarkets-use-ai-to-cut-prices/)
- **UC San Diego** (modelo, no prueba de campo): los precios dinámicos reducirían el desperdicio un **21 %** en promedio y subirían el margen bruto un **3 %** [Académico] — [UCSD Today](https://today.ucsd.edu/story/dynamic-pricing-could-cut-greenhouse-gas-emissions-from-landfills-far-more-than-organic-waste-bans)

**Visión por computadora y disponibilidad en góndola**
- Simbe (Tally): **−35 % de quiebres controlables** en el piloto de un supermercado nacional de EE. UU. sin nombre [Vendor] — [Simbe](https://www.simberobotics.com/resources/insights/how-a-leading-grocer-improved-on-shelf-availability-and-drove-store-profitability)
- Vinasoy (AWS): −20 % de quiebres en 2 meses [Prensa sectorial] — [AI News](https://www.artificialintelligence-news.com/news/vinasoy-reports-20-out-of-stock-reduction-aws-ai/)
- Nestlé con Shelf Inspector: ~20 % [Vendor] — [Bull/Eviden](https://www.bull.com/en/solutions/ai/shelf-inspector)

**Surtido localizado**
- QuantumBlack (McKinsey), Assortment.AI: +5 % de ventas en un retailer [Vendor] — [QuantumBlack/Medium](https://medium.com/quantumblack/ai-helps-retailers-put-the-right-products-in-the-right-stores-at-scale-f80f6cfb6bd6)
- McKinsey 2022: el surtido por tienda podría dar más de 5 % de ventas en Norteamérica (estimación) y 2-4 % en Europa [Consultora] — [McKinsey State of Grocery NA 2022](https://www.mckinsey.com/~/media/mckinsey/industries/retail/how%20we%20help%20clients/the%20state%20of%20grocery%20retail%202022%20north%20america/mck_state%20of%20grocery%20na_fullreport_v9.pdf); [McKinsey State of Grocery Europe 2022](https://www.mckinsey.com/~/media/mckinsey/industries/retail/our%20insights/state%20of%20grocery%20europe%202022/navigating-the-market-headwinds-the-state-of-grocery-retail-2022-europe.pdf)
- OXXO EE. UU. reemplazó ~400 SKUs tras adquirir DK, usando software propio que analiza ventas, tendencias y precios de la competencia [Prensa sectorial] — [CSP Daily News](https://www.cspdailynews.com/mergers-acquisitions/oxxo-replaces-400-skus-after-acquiring-dk-using-proprietary-software)

**CRM, lealtad, tienda conectada y comercio conversacional**
- OXXO usa analítica avanzada y modelos de IA para predecir el comportamiento de sus clientes en lealtad y CRM [Prensa] — [América Economía](https://www.americaeconomia.com/en/node/288712)
- Walmart Express (México): plataforma de tienda conectada de Vusion en todas las tiendas antes de fin de 2026 [Prensa] — [Xataka MX](https://www.xataka.com.mx/empresas-y-economia/walmart-quiere-tiendas-que-piensen-solas-asi-su-nueva-estrategia-ia-mexico)
- WhatsApp:
  - Cencosud Perú ("Compras JUMBO") permite hacer el pedido con IA que arma la lista y pagar en el mismo flujo (jun-2026, sin cifras) [Prensa] — [Perú Retail](https://www.peru-retail.com/un-supermercado-de-cencosud-estrena-las-compras-por-whatsapp-impulsadas-por-ia/)
  - Coca-Cola con Yalo (B2B a tenderos): ~1 millón de tenderos, ~40 mil pedidos al día, ~80 % de conversión y más de 60 % de pedidos recurrentes [Vendor, oct-2022] — [Mobile Time](https://www.mobiletime.com.br/noticias/24/10/2022/yalo-quer-replicar-em-outras-industrias-sucesso-de-chat-commerce-da-coca-cola-na-america-latina/)
- **Quick commerce en Panamá:** PedidosYa apuesta por el quick commerce como mercado estratégico (abr-2026) [Prensa] — [DPL News](https://dplnews.com/panama-pedidosya-apuesta-por-el-quick-commerce-para-consolidar-su-crecimiento/)

### Inferences
- Una tienda de 250 m² tiene poca bodega, así que el **pedido automático diario por SKU y tienda** (con clima, feriados, quincenas y eventos) es el habilitador operativo número uno. Las referencias más relevantes para el formato son OXXO, Lawson e Ito-Yokado.
- La **merma de perecederos** (frutas, verduras, panadería, lácteos) es la segunda palanca. Combinar pedidos asistidos con rebajas escalonadas por hora o día es replicable con modelos propios, sin licenciar Wasteless.
- El **surtido por micro-zona** (clusters de tiendas por perfil del área de influencia) conecta directamente con el modelo geoespacial de la sección 1: los mismos atributos de área que predicen ventas sirven para definir el surtido.
- **WhatsApp + Yappy** es un canal natural en Panamá: Yappy tiene más de 1,8 millones de usuarios y 34 mil comercios (ver sección 2). La tienda de 250 m² puede funcionar como mini-hub de entrega en un radio corto. Esto es inferencia y requiere validar costos de última milla.
- Para presentar el valor al cliente, conviene usar **rangos conservadores** que distingan:
  - Evidencia más independiente: PCFWC −14,8 % de desperdicio; UCSD −21 % (modelado).
  - Promesas de proveedores: Afresh −25 %; Wasteless −30 a −40 %; Simbe −35 %.

### Gaps
- No encontré cifras auditadas de impacto de la IA de pedidos en 7-Eleven o Lawson (ahorro de tiempo, merma, ventas).
- No encontré casos de visión por computadora en tiendas pequeñas de LatAm ni costos de hardware.
- No encontré cifras de resultados del canal WhatsApp de supermercados en LatAm (ticket, retención). Tampoco datos de quick commerce específicos de Panamá (pedidos, dark stores verificadas).
- No hay datos públicos sobre el uso de IA por cadenas panameñas (Super 99, Rey/Romero, Xtra, Riba Smith, El Machetazo); no se investigó en profundidad.

## 5. Modelos comerciales y precios de servicios de consultoría y analítica de ubicación en LatAm; fases y plazos típicos

### Takeaway
Hay poca transparencia de precios. Las referencias encontradas son:
- **Estudio de sitio único:** US$5-25 mil y 4-8 semanas (referencia de un proveedor estadounidense).
- **Estudio de mercado por consultora en México:** MXN 230-600 mil + IVA (2026).
- **Plataformas por zona en México:** desde MXN 2.500 por zona.
- **SaaS:** desde ~US$200 al mes (GrowthFactor) hasta más de US$20 mil al año (SiteZeus), y Esri BA a US$700-5.200 por usuario al año.

No encontré evidencia pública de **success fees** en site selection.

### Cited Findings
- Consultoría de sitio único: típicamente **US$5.000-25.000** y **4-8 semanas** [Vendor, EE. UU.] — [GrowthFactor: Site selection services guide](https://growthfactor.ai/blog-posts/site-selection-services-complete-guide). La misma fuente advierte que quien espera un pronóstico de ventas a veces solo recibe un resumen demográfico, por lo que el pronóstico debe quedar explícito en el alcance — misma fuente.
- Estudio de mercado por consultora en México: **MXN 230.000-600.000 + IVA** (2026), según alcance, ciudad y trabajo de campo [Vendor] — [Blackprint](https://www.blackprint.ai/guias/cuanto-cuesta-un-estudio-de-mercado)
- Modelo por crédito o zona: Zonia cobra MXN 2.500 por zona en su plan básico y desde MXN 26.500 por un estudio a la medida, y cita MXN 30.000-80.000 para consultoras [Vendor] — [Zonia](https://zonia.mx/)
- Datos por zona metropolitana (México): $5.200-6.000 por base [Vendor] — [Mexico GIS Data](https://mexicogisdata.com/base-de-datos-geomarketing-mexico/)
- SaaS de site selection:
  - GrowthFactor: ~US$200 al mes en el tier de entrada; Enterprise y "Labs" (equipo de data science embebido) a medida [Vendor] — [Toolradar](https://toolradar.com/tools/growthfactor/pricing)
  - SiteZeus: más de US$20 mil al año [competidor] — [GrowthFactor vs SiteZeus](https://www.growthfactor.ai/compare/growthfactor-vs-sitezeus)
  - Placer.ai: US$5-30 mil al año (estimación de terceros) — [SoftwareFinder](https://softwarefinder.com/analytics-software/placer-ai)
  - Esri BA Web: US$700-5.200 por usuario al año — [AWS Marketplace](https://aws.amazon.com/marketplace/pp/prodview-kkpfgbxfp6qde)
  - CARTO: cuota anual cotizada — [CARTO pricing](https://carto.com/pricing/)
- Fases típicas de site selection: Research → Evaluate → Decide → Validate, con análisis separados de demanda, competencia y canibalización. Ningún marco da semanas por fase para un plan de red [Vendor] — [GrowthFactor: Site selection process](https://www.growthfactor.ai/resources/blog/site-selection-process-complete-guide); [SafeGraph checklist](https://www.safegraph.com/?p=1429)
- Ciclo de vida de una tienda: selección de sitio → diseño → construcción → gestión continua [Prensa sectorial] — [Total Retail](https://www.mytotalretail.com/article/the-retail-store-lifecycle-from-plan-to-performance/)
- Valor económico de evitar un mal sitio: Dollar General invierte ~US$500 mil por tienda con retorno de ~2 años [Análisis] — [Quartr](https://quartr.com/insights/edge/dollar-general-the-rural-retailer-playbook). Buxton dice haber reducido el tiempo a rentabilidad de 18 a 6 meses en un caso [Vendor/agregador] — [Cuspera](https://www.cuspera.com/products/buxton-analytics-platform-x-6496)
- Proyectos de forecasting en proximidad: el piloto de OXXO con RELEX empezó en oct-2023 con 13 categorías y se extendió en olas hasta may-jun 2024, unos 7-9 meses hasta escalar categorías [Vendor] — [RELEX OXXO](https://www.relexsolutions.com/resources/case-study-oxxo/)

### Inferences
- Una **estructura comercial creíble** para Lativium en Panamá (los montos son **inferencias** a partir de los benchmarks anteriores; la conversión MXN→USD es aproximada y no tiene fuente):
  1. **Diagnóstico y mapa de oportunidades (white space)** para Ciudad de Panamá, Panamá Oeste y San Miguelito: proyecto de precio fijo de 6-10 semanas. Rango de referencia: similar o algo inferior a un estudio de consultora mexicano (MXN 230-600 mil ≈ US$12-33 mil). Entregables: grilla H3 con potencial, competencia, flujos, ranking de los 30-50 micro-mercados y un tablero.
  2. **Scoring por sitio** ("ficha de local" para cada local que traiga el broker): tarifa por sitio, muy por debajo de los US$5-25 mil de un estudio de sitio único de EE. UU., porque el modelo ya está construido. Precio sugerido: unos pocos cientos a ~US$1-2 mil por sitio, a validar con el cliente.
  3. **Suscripción (SaaS o servicio administrado)** con tablero de red, monitoreo de canibalización, re-entrenamiento trimestral del modelo y alertas de tiendas en riesgo. Mensualidad comparable al rango de GrowthFactor a SiteZeus.
  4. **Operación con IA tras la apertura** (pedido automático, merma, surtido por cluster, WhatsApp + Yappy): piloto de 3-6 meses en 5-10 tiendas y luego cobro por tienda al mes.
  5. **Success fee** opcional: bono si las tiendas recomendadas alcanzan el X % de las ventas pronosticadas al mes 12. No hay benchmark público; es una propuesta de diferenciación.
- Riesgo comercial: el cliente puede comparar con licencias de software (Esri BA a US$700 por usuario al año). La propuesta de valor debe ser "decisiones y modelo calibrado con datos panameños", no "acceso a una herramienta".

### Gaps
- No encontré tarifas publicadas de consultoras de geomarketing en Panamá, Colombia o Perú, ni tarifas por sitio de proveedores establecidos (Kalibrate, Buxton, SiteZeus).
- No encontré evidencia pública de contratos con success fee en site selection retail.
- No encontré plazos publicados para un plan de red completo (multi-sitio) con modelo de pronóstico.

## 6. ¿Qué podría ofrecer de forma realista Lativium a cadenas de supermercados en Panamá? (síntesis para diseñar la oferta)

### Takeaway
No hay información pública sobre Lativium, así que la oferta debe apoyarse en credenciales de método y en un piloto. Lo realista es un servicio en 3 capas:
1. **Dónde abrir:** modelo geoespacial con datos panameños.
2. **Cuántas y en qué orden:** canibalización y densidad.
3. **Cómo hacer que la tienda de 250 m² funcione:** pedido automático, merma, surtido local y WhatsApp.

Todo validado con backtesting sobre las tiendas existentes del cliente y con expectativas de precisión tomadas de la literatura.

### Cited Findings
- La búsqueda web no arrojó resultados sobre "Lativium"; no pude verificar su oferta ni sus credenciales — (búsqueda "Lativium Panamá inteligencia artificial transformación digital consultora", 19-nov-2026, sin coincidencias)
- Contexto del ecosistema: Panamá tiene una Estrategia Nacional de IA a 2030 liderada por Senacyt, con la visión de ser "hub" de innovación en IA [Oficial/Prensa] — [News in America (2026)](https://newsinamerica.com/pdcc/boletin/2026/panama-busca-convertirse-en-el-canal-digital-de-la-inteligencia-artificial-en-america-latina/); [Panacámara: Estrategia Nacional de IA (ago-2026)](https://www.panacamara.com/wp-content/uploads/2026/08/ES-2-Estrategia-Nacional-de-IA.pdf). La Prensa reporta que Panamá está rezagado en la creación de empresas de IA [Prensa] — [La Prensa](https://www.prensa.com/economia/panama-rezagada-en-el-desarrollo-de-empresas-de-inteligencia-artificial/)
- Densidad mínima y formato como referencias: Mass necesita al menos 60 tiendas por ciudad con locales de 150-200 m² — [Perú Retail](https://www.peru-retail.com/como-logro-mass-superar-las-1-500-tiendas-en-peru-las-claves-de-su-rapido-crecimiento/). OXXO Nicho ya es ~25 % de sus aperturas — [El Imparcial](https://www.elimparcial.com/mexico/2026/05/17/femsa-anuncio-el-cierre-de-tiendas-oxxo-que-no-son-rentables-tras-detectar-cambios-en-los-habitos-de-consumo-y-la-empresa-planea-abrir-mil-nuevas-sucursales-bajo-el-formato-de-nicho-para-priorizar-la-productividad-sobre-el-crecimiento-acelerado-de-unidades-en-todo-mexico/)
- Precisión realista de modelos para conveniencia: 70-76 % (MTS-XGBoost) frente a una línea base de ~55 % — [Nature Sci Rep 2025](https://www.nature.com/articles/s41598-025-30650-w); [Applied Sciences 2022](https://doi.org/10.3390/app12063036)
- Datos panameños disponibles: REDATAM 2023 por lugar poblado (gratis) — [Manual CensosWeb 2023](https://www.inec.gob.pa/redpan/RpHelp/Manual_CensosWeb_2023.pdf); movilidad de PREDIK con cobertura declarada de Panamá — [Datarade PREDIK](https://datarade.ai/data-providers/centralamericadata/data-products); Metro en datos abiertos — [datosabiertos.gob.pa](https://www.datosabiertos.gob.pa/dataset/?organization=metro-de-panama)
- Ejemplo de potencial de una ubicación en Panamá (Super 99 Vía Porras: 571 mil personas y ~US$82 millones al mes de gasto a 15 min en auto) — [PREDIK](https://predikdata.com/es/supermercados-como-medir-el-potencial-de-sus-ubicaciones/)
- Cumplimiento: Ley 81 de 2019 y Decreto 285 de 2021 (consentimiento, finalidad, ANTAI) — [Kraemer Law](https://kraemerlaw.com/en/articles/law-81-of-2019-about-protection-of-personal-data-in-panama/)

### Inferences
**Propuesta "Lativium para supermercados", módulos sugeridos:**
- **M0. Data foundation (2-4 semanas):**
  - Integrar ventas por tienda, SKU y día, lealtad y delivery geocodificado del cliente.
  - Integrar el Censo 2023 por lugar poblado (REDATAM) y la geometría de corregimientos.
  - Integrar POIs de Overture, OSM y Google Places (New): competencia, generadores de tráfico como escuelas, clínicas, oficinas y paradas.
  - Integrar Metro y, de forma opcional, movilidad de PREDIK.
  - Todo en una grilla H3 con gobierno de datos según la Ley 81.
- **M1. Mapa de espacio en blanco y potencial (4-6 semanas):**
  - Isócronas a pie de 5 y 10 minutos y en auto de 5 minutos.
  - Huff calibrado con la participación de mercado observada en las tiendas propias.
  - Índice de "zonas de alta influencia": densidad de hogares, ingreso proxy, flujos, nodos de transporte y brechas de oferta.
- **M2. Modelo de ventas por sitio (ML) y backtesting:**
  - GBM o random forest entrenado con tiendas existentes y análogas.
  - Validación fuera de muestra con métricas reportadas al cliente (MAPE y acierto éxito/fracaso), con expectativa inicial del 70-75 % de acierto, en línea con la literatura.
- **M3. Canibalización y plan de red:**
  - Matriz de transferencia entre tiendas propias, como regla inicial 50-70 % de demanda transferida en zonas superpuestas, ajustable con datos.
  - Optimización MCLP o p-median para elegir N tiendas y secuencia de aperturas.
  - Densidad mínima por zona, con la referencia de las 60 tiendas por ciudad de Mass.
- **M4. Scoring de locales en campo:** app o formulario georreferenciado para brokers, con ficha automática por local (renta/m², frente, visibilidad, estacionamiento, acera, cruce peatonal) y su score.
- **M5. Operación con IA de la tienda de 250 m²:**
  - Pedido automático diario (clima, quincenas, feriados).
  - Merma y rebajas de perecederos.
  - Surtido por cluster de micro-zona.
  - WhatsApp + Yappy para pedidos de entrega cercana.
  - Monitoreo de disponibilidad, con visión por computadora solo como fase 2 por el costo de hardware.
- **M6. Monitoreo continuo (suscripción):** tablero de red, alertas de tiendas por debajo del pronóstico, re-entrenamiento trimestral y evaluación de cierres o reubicaciones (el enfoque de OXXO 2026).

**Pilotos sugeridos para generar credibilidad rápida:** backtesting gratuito o de bajo costo con las tiendas actuales del cliente ("¿el modelo habría predicho sus mejores y peores tiendas?"), más un mapa de oportunidades para un distrito (por ejemplo, San Miguelito o Panamá Oeste).

### Gaps
- No pude verificar la existencia ni las capacidades de Lativium. El diseño de la oferta asume capacidades de ciencia de datos y de ingeniería geoespacial.
- No hay datos públicos sobre la disposición a pagar de las cadenas panameñas ni sobre su madurez analítica; requiere entrevistas.
- No hay benchmarks públicos de ventas por m² de tiendas de proximidad en Panamá que permitan calibrar el modelo sin datos del cliente; esto podría estar cubierto por otro investigador.
