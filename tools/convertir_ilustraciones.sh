#!/bin/sh
# Convierte las ilustraciones SVG (carpeta ilustraciones/) a PNG para la app.
# Requiere rsvg-convert (librsvg).
cd "$(dirname "$0")/.." || exit 1
mkdir -p app/src/main/assets/imagenes
for f in ilustraciones/*.svg; do
  n=$(basename "$f" .svg)
  rsvg-convert -w 800 -h 450 "$f" -o "app/src/main/assets/imagenes/$n.png" || exit 1
  echo "OK $n.png"
done
