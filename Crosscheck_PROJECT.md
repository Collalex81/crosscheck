# Crosscheck — Brief del proyecto (visión genérica)

> Documento de arranque para el conocimiento del proyecto. Define **qué es**, **hacia dónde va**, y **cómo trabajar**. Es texto ligero: no incluye el código (el `index.html` con las librerías incrustadas es pesado).

## 1. Visión
Una herramienta web de un solo archivo, 100% offline, que hace **cross-reference entre dos spreadsheets cualesquiera** (CSV o XLSX), sin importar su estructura. No es específica de inventario: la reconciliación de inventario es solo *un caso de uso*. El objetivo es que sirva para cruzar cualquier par de tablas (clientes vs CRM, facturas vs pagos, activos vs registro, empleados vs nómina, etc.).

## 2. Principios de diseño
1. **Genérica primero.** Nada cableado a un dominio. Nombres, llaves y estados los define el usuario.
2. **Absorbe la variabilidad** con una capa de mapeo entre lectura y cruce (detección de encabezados + diccionario de sinónimos + confirmación manual).
3. **Configurable, no programable.** El usuario adapta la herramienta con clics y campos de texto, sin tocar código.
4. **Offline y portable.** Un archivo, sin depender de internet (para uso local); desplegable en GitHub Pages para uso por URL.
5. **Salida profesional.** Reporte en pantalla + export a Excel corporativo.

## 3. Arquitectura (genérica)
1. **Lectura** XLSX/CSV con detección automática de la fila de encabezado (tolerante a filas basura/doble encabezado).
2. **Mapeo de llaves de match** — hasta N prioridades, **renombrables** por el usuario (hoy 7: Serial, EO, Part, MFG, ID/Asset Tag, SKU/Code, Barcode/UPC — pero son solo defaults editables). El cruce usa la primera llave disponible por prioridad.
3. **Selección de columnas del reporte** — checkboxes de todas las columnas en ambos lados; orden configurable arrastrando.
4. **Motor de cruce** → matched / ambiguous / no-match / only-in-anchor, con expansión de ambiguos en filas separadas.
5. **Columna de estado derivada (Stage logic) — CONFIGURABLE** (ver §4).
6. **Filtros** sincronizados (KPIs + barra) y **export a Excel** con formato corporativo.

## 4. Stage logic configurable (el gran salto genérico)
Hoy la lógica de estado está cableada a inventario (Sent to site / Assigned to BOM / Not assigned to BOM → Installed/Assigned/Available). **Objetivo:** convertirla en un motor de reglas definible por el usuario:

- El usuario elige una **columna fuente** (cualquiera del anchor o del cruce).
- Define un conjunto de **reglas** ordenadas: `si el valor contiene / es igual / coincide con <patrón> → etiqueta "<texto>" + color`.
- Regla **por defecto** (fallback) para valores no reconocidos.
- Opción de **anexar** el valor de otra columna a la etiqueta (como hoy se anexa el Build Plan).
- Estas reglas se guardan en los **presets** (junto con mapeo, columnas y opciones), para reutilizarlas por tipo de reporte.

Resultado: la misma "columna de estado" sirve para inventario, para "estado de pago" (Pagado/Pendiente/Vencido), para "estado de ticket", etc. — todo definido por el usuario.

## 5. Estado actual vs. objetivo
Hecho (genérico ya): lectura flexible, auto-mapeo por sinónimos, 7 llaves editables, columnas por checkboxes en ambos lados, orden configurable, filtros sincronizados, export Excel corporativo (centrado, autoajuste tope 50 + wrap, freeze B6, autofilter), encabezado + instrucciones fijos, presets en el navegador.

Pendiente para la visión genérica:
- **Stage logic configurable** (§4) — hoy cableada a inventario; convertir en motor de reglas.
- Terminología de UI más neutral (menos "FC/inventario", más "Anchor / File B" configurable).
- Guardar/exportar e importar presets como archivo (portar configuraciones entre equipos).
- (Opcional) match difuso por nombre/descripción; normalización por regex definible.

## 6. Distribución
- **Local:** un `index.html` autocontenido (SheetJS + ExcelJS incrustados), abrir con doble clic, offline.
- **Web:** repo en GitHub `Collalex81/crosscheck`, servido por GitHub Pages en `https://collalex81.github.io/crosscheck/`. Estructura plana en la raíz: `index.html` + `xlsx.min.js` + `exceljs.min.js`.
- En Google Sites: botón/enlace a la URL de Pages (abre en pestaña nueva; no incrustar en iframe).

## 7. Cómo trabajar (para cada chat del proyecto)
- El código vive en `index.html` (carpeta Crosscheck en Drive / repo en GitHub). **Nunca pegar el archivo completo en el chat** si tiene las librerías incrustadas (pesa mucho). Con la versión separada (libs aparte) el `index.html` es chico y se edita completo.
- Editar por secciones con reemplazo exacto; leer este brief antes de trabajar.
- Al hacer cambios grandes, actualizar este documento.
- Respuestas concisas y directas.

## 8. Repos y rutas
- GitHub: `https://github.com/Collalex81/crosscheck`
- Pages: `https://collalex81.github.io/crosscheck/`
- Local: `H:\My Drive\Claude code\Crosscheck\` (index.html + xlsx.min.js + exceljs.min.js)
