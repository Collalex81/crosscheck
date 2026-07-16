# Crosscheck — Spec del proyecto

> Documento de diseño y estado. Guárdalo como **conocimiento del proyecto** para que cualquier chat nuevo entienda la herramienta sin arrastrar el hilo completo. Es texto ligero: describe el diseño, no pega el código pesado (el `index.html` mide ~1.6 MB por las librerías incrustadas).

---

## 1. Qué es
Herramienta de **cross-reference / reconciliación** en un solo archivo HTML, 100% offline (doble clic en cualquier navegador; ningún archivo sale del equipo). Compara dos spreadsheets. Originalmente FC Inventory (ancla, estructura fija) vs. archivo de cliente (CSV/XLSX, estructura variable); en v2 se generaliza para **cualquier** par de spreadsheets.

## 2. Flujo
1. **Lectura** de XLSX o CSV con detección automática de la fila de encabezados (tolerante a filas basura y doble encabezado; prefiere la fila que más se parece a nombres de campo conocidos).
2. **Auto-mapeo** por diccionario de sinónimos + confianza; corregible con dropdown (queda "manual").
3. **Cruce por cascada de prioridad** de match keys; informa en *Match by* con qué llave hizo match.
4. **Salida**: matched / ambiguo / sin match / solo-en-ancla, con conteo por llave, filtros, búsqueda y export a Excel corporativo.

## 3. Match keys (prioridades)
Editables (se pueden renombrar en la UI). Defaults:
`Serial / SN → EO → Part Number → MFG Product # → ID / Asset Tag → SKU / Code → Barcode / UPC`.
El cruce toma, por cada fila, la primera llave mapeada y no vacía en ese orden.

## 4. Columnas del reporte
Elegibles con checkboxes en **ambos** lados (ancla y cliente): se marca cualquier columna del archivo. El orden se define arrastrando chips en el panel de orden. Meta-columnas opcionales: Result, Key, Match group, Equipment Status.

## 5. Normalización (toggles)
Mayúsculas, espacios, guiones internos y **ceros a la izquierda** (Excel se come los ceros de los seriales — este es el que más esconde matches válidos).

## 6. Columna de estado derivada — **motor de reglas configurable** (v2)
Antes estaba cableada a inventario; ahora es un motor de reglas definible por el usuario (`stageCfg` + `evalStage()` en el código):

- **Nombre de la columna** editable (por defecto "Equipment Status"; renombrable p. ej. a "Estado de pago").
- **Columna fuente** — cualquier columna del ancla (A). `state.A.stageIdx`.
- **Columna a anexar (opcional)** — se agrega como ` · <valor>` a la etiqueta (generaliza el antiguo Build Plan). `state.A.buildPlanIdx`.
- **Reglas ordenadas** (gana la primera que coincide): `[contiene | es igual | regex] patrón → etiqueta + color`. Reordenables (▲▼) y borrables (✕); "＋ Agregar regla".
- **Regla por defecto (fallback)**: etiqueta + color; si la etiqueta está vacía, muestra el **valor original** (comportamiento previo para valores no reconocidos).
- **Paleta fija** (7): azul, ámbar, verde, rojo, gris, morado, teal — se aplica igual en pantalla (`.eqp-<color>`) y en el Excel (`STAGE_COLORS[color].xlFill/xlFont`).
- Todo se guarda en los **presets** (`cfg.stageCfg`); los presets viejos (con `stage`/`buildPlan` pero sin reglas) **migran** automáticamente a las reglas de inventario por defecto.

Reglas de inventario **precargadas por defecto** (equivalen a la lógica anterior):

| Regla (contiene) | Etiqueta | Color |
|---|---|---|
| not assigned | Available to reassign | Verde |
| sent to site / installed | Installed at site | Azul |
| assigned to bom / assigned | Assigned to Build Plan | Ámbar |

> El orden importa: "not assigned" va antes que "assigned" (primera coincidencia gana).

## 7. Export a Excel (.xlsx real vía ExcelJS)
Encabezado corporativo (título, subtítulo con fecha y nombres de archivos, KPIs, leyenda), **autofilter** en la fila de encabezados, **freeze en B6** (`xSplit:1, ySplit:5`), color-coding por fila y por Equipment Status, texto **centrado**, ancho **autoajustado con tope 50** y `wrapText` para textos que exceden 50, bordes y expansión de ambiguos en filas separadas (`1 de N`).

## 8. Stack técnico
Un solo HTML autocontenido, sin internet. **SheetJS** (~670 KB) y **ExcelJS** (~950 KB) incrustados. Peso ~1.6 MB. **No pegar el archivo completo en el chat.** Editar por secciones (reemplazo por contenido exacto); la numeración de líneas es poco fiable por los blobs minificados.

## 9. Distribución / Google Sites
Abierto directo o en pestaña nueva (URL de GitHub Pages) → todo funciona. Embebido como iframe en Google Sites → Google bloquea descargas y prompts. Solución: botón/enlace a la URL completa de GitHub (abre en pestaña nueva). No incrustar como iframe.

## 10. Estado — pendientes 1–6 (primera tanda) TODOS ✅
1. ✅ Botón de reset. 2. ✅ Hasta 6 columnas del cliente. 3. ✅ Orden de columnas + freeze B6. 4. ✅ FC: EO = Shipment Package por defecto. 5. ✅ Filtros sincronizados (KPIs + barra). 6. ✅ Excel pulido (centrado, autoajuste tope 50 + wrap).

## 11. Upgrade de generalización (v2) — hecho en esta tanda
1. ✅ **Match keys editables** — input para renombrar cada prioridad; se guarda en `keyLabels`, se refleja en mapeo/reporte/tiers/Excel y persiste en presets.
2. ✅ **3 prioridades nuevas** (7 total): ID / Asset Tag, SKU / Code, Barcode / UPC, con sinónimos genéricos.
3. ✅ **Columnas del cliente por checkboxes** de todas las columnas (igual que el ancla), en vez de 6 dropdowns.
4. ✅ **Encabezado + instrucciones fijos** (`.stickytop`): encabezado y barra de 4 pasos quedan sticky arriba al hacer scroll.

Pendiente: continuar con más mejoras (el usuario dijo "haz esto y luego seguimos").
Nota técnica: el `th` de la tabla es `sticky top:0` y queda por debajo del bloque fijo; si molesta, ajustar su `top` a la altura del `.stickytop` en otra iteración.

## 12. Pruebas
- Motor de reglas (`evalStage`): probado con Node (replica exacta del comportamiento de inventario, orden "not assigned" antes que "assigned", `regex`/`es igual`, regex inválido → fallback sin romper).
- UI: **probado en vivo headless** (Playwright/Chromium) cargando el `index.html` con datos de ejemplo — sin errores de consola; el editor dibuja reglas, colores, ▲▼✕, "＋ Agregar regla", fallback y nombre editable; el rename se refleja en el reporte.
- **Rutas de librerías:** los `<script src>` se alinearon a `lib/xlsx.min.js` y `lib/exceljs.min.js` (coincide con `split_libs.py` y con la carpeta local). Si GitHub Pages usa estructura plana en la raíz, revertir a `xlsx.min.js` / `exceljs.min.js`.
- La prueba definitiva sigue siendo abrir el `index.html` con **archivos reales** de inventario + cliente.

## 13. Bilingüe EN/ES + rediseño estilo JCE (v3)
- **Bilingüe (inglés por defecto, persistente):** motor i18n propio embebido (`I18N={en,es}`, `t()`, `tf()` con placeholders, `applyLang()`). Soporta `data-i18n` (textContent), `data-i18n-html`, `data-i18n-ph` (placeholder), `data-i18n-title`, `data-i18n-aria`. Toggle **EN/ES** en el encabezado (clase `.lang`, igual que el portal JCE); guarda la preferencia en `localStorage` bajo la **misma llave `jce_lang`** que el portal, así se sincroniza. Las cadenas generadas por JS (KPIs, tabla, tiers, mapeo, estado configurable, hints, alertas, export a Excel) usan `t()`; `relocalizeDynamic()` re-renderiza todo al cambiar de idioma. La ayuda y la nota "cómo leer el match" son bilingües vía `<template id="tpl-help-en/es">` y `tpl-note-en/es`.
- **Contenido vs. chrome:** las etiquetas de las *reglas* de estado (p. ej. "Installed at site") y el nombre de la columna de estado (`stageCfg.colLabel`, por defecto "Equipment Status") son **datos editables**, no se traducen automáticamente.
- **Rediseño estilo JCE (JCE Page):** paleta de marca (`--brand:#e4231c`, `--brand-2`, navys `#0a1122/#0e1730/#16224a`), fuentes **Inter** (cuerpo) y **Sora** (títulos) vía Google Fonts (con fallback a system-ui si no hay internet), header tipo `site-header` con logo en badge + toggle de idioma, **hero** navy con acento rojo y chips, tarjetas con gloss/sombras en capas, botón primario rojo en gradiente, KPIs tipo stat-tile, chips/pills redondeados y footer navy con borde rojo. Se conservaron **todas las clases** existentes (el JS no cambió de nombres); solo se reskinaron.
- **Pruebas (headless Playwright):** carga con CSV de ejemplo, corrida completa de crosscheck, y **toggle EN↔ES** verificando que botones, KPIs, badges de la tabla, pasos, panel de orden, opciones y ayuda cambian de idioma; sin errores de consola (salvo el fetch de Google Fonts, que falla solo sin internet y cae a fuentes del sistema).

## 14. Cómo trabajar sin llenar el contexto
No volver a pegar el HTML completo en el chat. Editar por secciones. Al agregar textos nuevos, añadir su llave en `I18N.en` **y** `I18N.es`. Este spec (no el código) es lo que va al conocimiento del proyecto.
