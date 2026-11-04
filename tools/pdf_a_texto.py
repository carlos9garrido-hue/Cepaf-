#!/usr/bin/env python3
"""
Convierte el texto extraído de un PDF de San Juan (con pdftotext) al formato
"capítulo:versículo texto" que lee importar_texto.py.

Uso:
  pdftotext -enc UTF-8 evangelio-de-juan.pdf juan_raw.txt
  python3 pdf_a_texto.py juan_raw.txt juan.txt

Casos que maneja:
  - Encabezados y pies de página repetidos.
  - Números de versículo solos en su línea (el texto sigue en la línea siguiente).
  - Números de versículo en medio de una línea (pdftotext a veces junta dos versículos).
Un número solo se toma como inicio de versículo cuando es el siguiente esperado.
"""
import re
import sys

ENCABEZADOS = (
    "JUAN",
    "BIBLIA DE JERUSALÉN, 1976",
    "INSTITUTO DE PASTORAL BÍBLICA",
)

# Correcciones puntuales: pdftotext perdió un guion que sí aparece en el PDF
# (Juan 4,1: "...bautizaba más que Juan -" y luego "aunque no era Jesús...").
CORRECCIONES = {
    (4, 1): lambda t: t + " -" if t.endswith("que Juan") else t,
}


def convertir(entrada, salida):
    capitulo = 0
    versiculo = 0
    versos = []  # [cap, ver, texto]

    def empezar(texto):
        """Abre el versículo siguiente con 'texto' y separa los que vengan pegados."""
        nonlocal versiculo
        versiculo += 1
        versos.append([capitulo, versiculo, ""])
        agregar(texto)

    def agregar(texto):
        """Añade texto al último versículo; si trae el número del siguiente, lo separa."""
        texto = texto.strip()
        if not texto:
            return
        m = re.search(r"(?:^|\s)(%d)\s+(\S.*)$" % (versiculo + 1), texto)
        if m:
            antes = texto[: m.start()].strip()
            if antes:
                versos[-1][2] += (" " if versos[-1][2] else "") + antes
            empezar(m.group(2))
        else:
            versos[-1][2] += (" " if versos[-1][2] else "") + texto

    with open(entrada, encoding="utf-8") as f:
        lineas = f.read().replace("\f", "\n").splitlines()

    for crudo in lineas:
        linea = crudo.strip()
        if not linea or linea in ENCABEZADOS:
            continue

        m_cap = re.fullmatch(r"Juan\s+(\d+)", linea)
        if m_cap and int(m_cap.group(1)) == capitulo + 1:
            capitulo += 1
            versiculo = 0
            continue

        m_ver = re.match(r"^(\d+)(?:\s+(.*))?$", linea)
        if m_ver and capitulo and int(m_ver.group(1)) == versiculo + 1:
            empezar(m_ver.group(2) or "")
            continue

        if linea.isdigit():
            continue  # número de página suelto

        if versos:
            agregar(linea)
        else:
            print(f"Línea ignorada: {linea[:60]}", file=sys.stderr)

    with open(salida, "w", encoding="utf-8") as f:
        for c, v, t in versos:
            t = re.sub(r"\s+", " ", t).strip()
            if (c, v) in CORRECCIONES:
                t = CORRECCIONES[(c, v)](t)
            f.write(f"{c}:{v} {t}\n")
    print(f"{len(versos)} versículos escritos en {salida}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    convertir(sys.argv[1], sys.argv[2])
