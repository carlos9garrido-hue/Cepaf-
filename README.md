# CePaF – Evangelio de San Juan y Lectio Divina (Android)

Prototipo en Kotlin + Jetpack Compose.

## Cómo abrirlo
1. Abrir la carpeta `CePaF` con Android Studio (Hedgehog o más reciente).
2. Dejar que sincronice Gradle (genera el wrapper automáticamente).
3. Ejecutar en un emulador o dispositivo con Android 7.0 o superior.

> Importante: este prototipo no se compiló en el entorno donde se creó. Es posible que Android Studio pida ajustes menores de versiones.

## Estructura
- **Evangelio**: 21 capítulos, versículos numerados, tamaño de letra A- / A+.
- **Lectio**: guía de los 5 pasos de la Lectio Divina.
- **Ciudades**: glosario con historia y gobernantes.
- **Personajes**: biografías de los protagonistas de los signos.
- **Folleto**: espacio reservado para el folleto digital.

## Contenido editable (`app/src/main/assets/`)
- `juan.json`: texto del Evangelio (Biblia de Jerusalén, 1976), 21 capítulos y 879 versículos, convertido desde el PDF del Instituto de Pastoral Bíblica.
- `glosario.json`, `personajes.json`, `lectio.json`: contenidos en español, editables.
- `imagenes/`: poner aquí las imágenes y escribir su nombre de archivo en el campo `"imagen"` del JSON correspondiente.

## Volver a cargar o cambiar el texto
Desde un PDF:
1. `pdftotext -enc UTF-8 evangelio-de-juan.pdf juan_raw.txt`
2. `python3 tools/pdf_a_texto.py juan_raw.txt juan.txt`
3. `python3 tools/importar_texto.py importar juan.txt --version "Nombre de la versión" -o app/src/main/assets/juan.json`

Desde un texto propio: un versículo por línea (`1:1 Texto...`) y solo el paso 3. El script avisa de qué versículos faltan (el Evangelio tiene 21 capítulos y 879 versículos).

## Sobre el texto
La Biblia de Jerusalén está protegida por derechos de autor: para publicar la app (por ejemplo en Google Play) hace falta autorización de la editorial (Desclée de Brouwer). Para uso interno de formación, conviene confirmar los permisos con quien proporcionó el PDF. Si no se consigue, se puede cambiar a una versión de dominio público con el mismo procedimiento.
