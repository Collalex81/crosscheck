#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Separa el index.html autocontenido de Crosscheck en:
    index.html          (solo la app, ~50 KB)
    lib/xlsx.min.js     (SheetJS)
    lib/exceljs.min.js  (ExcelJS)

Guarda una copia de seguridad del original en index.full.backup.html.

USO: pon este archivo en la carpeta que contiene index.html y ejecuta:
    python split_libs.py
"""
import os, sys, shutil

SRC = 'index.html'

def carve(html, marker, out_rel):
    """Extrae el bloque <script>...</script> que contiene 'marker' a out_rel
    y lo reemplaza en el HTML por <script src="out_rel"></script>."""
    i = html.find(marker)
    if i == -1:
        print('  ! No encontre el marcador:', marker)
        return html, False
    start = html.rfind('<script>', 0, i)
    end = html.find('</script>', i) + len('</script>')
    inner = html[start + len('<script>'):end - len('</script>')]
    d = os.path.dirname(out_rel)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(out_rel, 'w', encoding='utf-8') as f:
        f.write(inner)
    tag = '<script src="%s"></script>' % out_rel
    print('  - %s  (%d KB)' % (out_rel, round(len(inner) / 1024)))
    return html[:start] + tag + html[end:], True

def main():
    if not os.path.exists(SRC):
        sys.exit('No hay index.html en esta carpeta. Corre el script dentro de la carpeta Crosscheck.')

    with open(SRC, encoding='utf-8') as f:
        html = f.read()
    print('index.html original: %d KB' % round(len(html) / 1024))

    # copia de seguridad (una sola vez)
    if not os.path.exists('index.full.backup.html'):
        shutil.copy(SRC, 'index.full.backup.html')
        print('Backup -> index.full.backup.html')

    print('Extrayendo librerias:')
    html, ok1 = carve(html, 'SheetJS 0.18.5', 'lib/xlsx.min.js')
    html, ok2 = carve(html, 'ExcelJS 4.4.0', 'lib/exceljs.min.js')

    with open(SRC, 'w', encoding='utf-8') as f:
        f.write(html)

    print('Nuevo index.html: %d KB' % round(len(html) / 1024))
    print('SheetJS:', 'OK' if ok1 else 'FALLO', '| ExcelJS:', 'OK' if ok2 else 'FALLO')
    print('Listo. Sube index.html y la carpeta lib/ a GitHub.')

if __name__ == '__main__':
    main()
