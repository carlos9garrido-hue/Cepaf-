#!/usr/bin/env python3
"""
Herramienta para cargar el texto del Evangelio de San Juan en CePaF.

Uso:
  # Genera juan.json con marcadores de posición (estructura de 21 capítulos / 879 versículos)
  python3 importar_texto.py plantilla --version "Texto pendiente" -o ../app/src/main/assets/juan.json

  # Convierte un archivo de texto a juan.json y lo valida
  python3 importar_texto.py importar juan.txt --version "Biblia de Jerusalén" -o ../app/src/main/assets/juan.json

Formato del archivo de texto: un versículo por línea, así:
  1:1 Texto del versículo...
  1:2 Texto del versículo...
Las líneas que no empiezan con "capítulo:versículo" se unen al versículo anterior.
"""
import argparse
import json
import re
import sys

# Número de versículos de cada capítulo de Juan (21 capítulos, 879 versículos).
VERSICULOS = [51, 25, 36, 54, 47, 71, 53, 59, 41, 42, 57, 50, 38, 31, 27, 33, 26, 40, 42, 31, 25]


def plantilla(version):
    return {
        "version": version,
        "capitulos": [
            {
                "numero": c,
                "versiculos": [
                    {"n": v, "t": "[Texto del versículo pendiente de cargar]"}
                    for v in range(1, total + 1)
                ],
            }
            for c, total in enumerate(VERSICULOS, start=1)
        ],
    }


def importar(ruta, version):
    datos = {}
    ultimo = None
    patron = re.compile(r"^\s*(\d+)\s*[:.,]\s*(\d+)\s+(.*\S)\s*$")
    with open(ruta, encoding="utf-8") as f:
        for linea in f:
            if not linea.strip():
                continue
            m = patron.match(linea)
            if m:
                c, v, texto = int(m.group(1)), int(m.group(2)), m.group(3)
                datos[(c, v)] = texto
                ultimo = (c, v)
            elif ultimo:
                datos[ultimo] += " " + linea.strip()
            else:
                print(f"Línea ignorada (sin versículo previo): {linea.strip()[:60]}", file=sys.stderr)

    problemas = []
    capitulos = []
    for c, total in enumerate(VERSICULOS, start=1):
        versiculos = []
        for v in range(1, total + 1):
            if (c, v) in datos:
                versiculos.append({"n": v, "t": datos[(c, v)]})
            else:
                problemas.append(f"Falta {c}:{v}")
        capitulos.append({"numero": c, "versiculos": versiculos})
    extras = [k for k in datos if k[0] > len(VERSICULOS) or k[1] > VERSICULOS[k[0] - 1] or k[0] < 1]
    problemas += [f"Versículo fuera de rango: {c}:{v}" for c, v in extras]
    return {"version": version, "capitulos": capitulos}, problemas


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p1 = sub.add_parser("plantilla")
    p1.add_argument("--version", default="Texto pendiente")
    p1.add_argument("-o", "--salida", required=True)
    p2 = sub.add_parser("importar")
    p2.add_argument("entrada")
    p2.add_argument("--version", required=True)
    p2.add_argument("-o", "--salida", required=True)
    a = ap.parse_args()

    if a.cmd == "plantilla":
        resultado, problemas = plantilla(a.version), []
    else:
        resultado, problemas = importar(a.entrada, a.version)

    with open(a.salida, "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=1)
    total = sum(len(c["versiculos"]) for c in resultado["capitulos"])
    print(f"Escrito {a.salida}: {len(resultado['capitulos'])} capítulos, {total} versículos")
    if problemas:
        print(f"ATENCIÓN: {len(problemas)} problemas", file=sys.stderr)
        for p in problemas[:30]:
            print("  -", p, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
