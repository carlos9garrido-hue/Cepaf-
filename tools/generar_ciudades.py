#!/usr/bin/env python3
"""
Genera las ilustraciones SVG originales de las ciudades y lugares del glosario
(carpeta ilustraciones/). Después, tools/convertir_ilustraciones.sh las pasa a PNG.

Uso:  python3 tools/generar_ciudades.py
"""
import os

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SALIDA = os.path.join(RAIZ, "ilustraciones")


# ---------- utilidades ----------

def doc(body, defs=""):
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        'viewBox="0 0 800 450" width="800" height="450">'
        f"<defs>{defs}</defs>{body}</svg>\n"
    )


def cielo(id_, a, b, medio=None, alto=450):
    paradas = f'<stop offset="0" stop-color="{a}"/>'
    if medio:
        paradas += f'<stop offset="0.6" stop-color="{medio}"/>'
    paradas += f'<stop offset="1" stop-color="{b}"/>'
    defs = f'<linearGradient id="{id_}" x1="0" y1="0" x2="0" y2="1">{paradas}</linearGradient>'
    return defs, f'<rect width="800" height="{alto}" fill="url(#{id_})"/>'


def sol(cx, cy, r, color="#FFE9A8", halo="#FFF3C9"):
    return (
        f'<circle cx="{cx}" cy="{cy}" r="{r * 1.6:.0f}" fill="{halo}" opacity="0.55"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}"/>'
    )


def casa(x, y, w, h, muro="#EAD9B8", borde="#CBB48A", puerta="#6B4A2B", luz=False):
    pw = max(8, w * 0.22)
    ph = h * 0.5
    p = puerta if not luz else "#F2C060"
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{muro}"/>'
        f'<rect x="{x - 3}" y="{y - 5}" width="{w + 6}" height="7" fill="{borde}"/>'
        f'<rect x="{x + w / 2 - pw / 2:.1f}" y="{y + h - ph:.1f}" width="{pw:.1f}" height="{ph:.1f}" '
        f'rx="{pw / 2.5:.1f}" fill="{p}"/>'
    )


def casa_teja(x, y, w, h, muro="#F0E2BD", teja="#B5532E"):
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{muro}"/>'
        f'<polygon points="{x - 4},{y} {x + w / 2},{y - h * 0.45:.1f} {x + w + 4},{y}" fill="{teja}"/>'
        f'<rect x="{x + w / 2 - 5:.1f}" y="{y + h - h * 0.45:.1f}" width="10" height="{h * 0.45:.1f}" rx="4" fill="#6B4A2B"/>'
    )


def olivo(x, y, s=1.0):
    return (
        f'<g transform="translate({x} {y}) scale({s})">'
        '<path d="M0 0 C-4 -20 4 -34 0 -50" stroke="#6B5A3E" stroke-width="7" fill="none" stroke-linecap="round"/>'
        '<circle cx="-14" cy="-58" r="18" fill="#7E8F5E"/><circle cx="12" cy="-62" r="20" fill="#94A26E"/>'
        '<circle cx="0" cy="-74" r="17" fill="#7E8F5E"/></g>'
    )


def palma(x, y, alto=150, s=1.0):
    t = alto
    return (
        f'<g transform="translate({x} {y}) scale({s})">'
        f'<path d="M0 0 C6 {-t * 0.4:.0f} -4 {-t * 0.7:.0f} 4 {-t}" stroke="#5C4328" stroke-width="10" fill="none" stroke-linecap="round"/>'
        '<g stroke="#4E7A4A" stroke-width="7" fill="none" stroke-linecap="round">'
        f'<path d="M4 {-t} C-24 {-t - 14} -52 {-t + 4} -70 {-t + 30}"/>'
        f'<path d="M4 {-t} C-14 {-t - 40} -44 {-t - 48} -68 {-t - 36}"/>'
        f'<path d="M4 {-t} C24 {-t - 40} 54 {-t - 46} 74 {-t - 30}"/>'
        f'<path d="M4 {-t} C32 {-t - 10} 58 {-t + 6} 74 {-t + 30}"/>'
        f'<path d="M4 {-t} C2 {-t - 34} 8 {-t - 56} 24 {-t - 72}"/>'
        "</g></g>"
    )


def barca(x, y, s=1.0, vela=True, casco="#6B4223"):
    v = (
        '<line x1="0" y1="-84" x2="0" y2="0" stroke="#4A3A2A" stroke-width="4"/>'
        '<path d="M4 -80 L4 -6 L64 -6 Z" fill="#F1E6CC"/>'
        if vela
        else ""
    )
    return (
        f'<g transform="translate({x} {y}) scale({s})">{v}'
        f'<path d="M-70 0 L90 0 Q76 36 40 40 L-30 40 Q-62 36 -70 0 Z" fill="{casco}"/>'
        '<rect x="-72" y="-4" width="164" height="7" rx="3" fill="#8A5E2E"/></g>'
    )


def oveja(x, y):
    return (
        f'<g transform="translate({x} {y})"><ellipse rx="20" ry="13" fill="#F4F0E6"/>'
        '<circle cx="-19" cy="-3" r="7" fill="#4A3A2A"/>'
        '<rect x="-12" y="9" width="3" height="11" fill="#4A3A2A"/><rect x="8" y="9" width="3" height="11" fill="#4A3A2A"/></g>'
    )


def tinaja(x, y, s=0.5):
    return (
        f'<g transform="translate({x} {y}) scale({s})">'
        '<path d="M-34 -150 L34 -150 L30 -132 C62 -112 66 -50 42 -6 C30 4 -30 4 -42 -6 C-66 -50 -62 -112 -30 -132 Z" fill="#B88A5A"/>'
        '<path d="M-58 -96 C-20 -84 20 -84 58 -96" stroke="#8A6038" stroke-width="6" fill="none"/>'
        '<ellipse cx="0" cy="-150" rx="34" ry="9" fill="#8A6038"/></g>'
    )


def almenas(x, y, ancho, color, paso=22, alto=10, w=12):
    n = int(ancho // paso)
    return "".join(
        f'<rect x="{x + i * paso}" y="{y - alto}" width="{w}" height="{alto}" fill="{color}"/>' for i in range(n + 1)
    )


def columnas(x, y, n, sep, alto, ancho=14, color="#F4EBD6", sombra="#D8CBAA"):
    out = ""
    for i in range(n):
        cx = x + i * sep
        out += f'<rect x="{cx}" y="{y}" width="{ancho}" height="{alto}" fill="{color}"/>'
        out += f'<rect x="{cx + ancho * 0.65:.1f}" y="{y}" width="{ancho * 0.35:.1f}" height="{alto}" fill="{sombra}"/>'
    return out


def lago(y, c1="#7FA6BF", c2="#2F5D7A", id_="lago"):
    defs = f'<linearGradient id="{id_}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient>'
    return defs, f'<rect y="{y}" width="800" height="{450 - y}" fill="url(#{id_})"/>'


def ondas(y, color="#FFFFFF", op=0.35):
    return "".join(
        f'<ellipse cx="{cx}" cy="{yy}" rx="{rx}" ry="3" fill="{color}" opacity="{op}"/>'
        for cx, yy, rx in [(120, y + 20, 50), (330, y + 44, 70), (560, y + 26, 60), (700, y + 60, 44), (210, y + 70, 56)]
    )


# ---------- escenas ----------

def jerusalen():
    d, s = cielo("c", "#E9A56A", "#FBE3B4")
    b = s + sol(620, 130, 34)
    b += '<path d="M0 270 C140 230 320 250 460 232 C600 214 720 240 800 226 V450 H0 Z" fill="#C9A06A"/>'
    # muralla y torres
    b += '<rect x="90" y="262" width="640" height="78" fill="#E4CFA2"/>' + almenas(90, 262, 640, "#E4CFA2")
    b += '<rect x="150" y="190" width="40" height="150" fill="#DCC48F"/>' + almenas(150, 190, 40, "#DCC48F", 18, 10, 10)
    b += '<rect x="650" y="196" width="40" height="144" fill="#DCC48F"/>' + almenas(650, 196, 40, "#DCC48F", 18, 10, 10)
    # explanada y Templo
    b += '<rect x="290" y="226" width="270" height="40" fill="#F0E2BD"/><rect x="290" y="262" width="270" height="6" fill="#CBB48A"/>'
    b += '<rect x="360" y="146" width="130" height="82" fill="#F7EBCB"/>'
    b += '<polygon points="350,146 425,112 500,146" fill="#D7A93B"/>'
    b += '<rect x="350" y="144" width="150" height="8" fill="#C79A2B"/>'
    b += columnas(372, 156, 6, 22, 70, 9, "#EFE0B8", "#D8C697")
    b += '<rect x="408" y="196" width="34" height="32" rx="14" fill="#7A5B3A"/>'
    # casas
    for x, y, w, h in [(110, 300, 50, 36), (170, 292, 44, 44), (230, 304, 56, 32), (570, 296, 50, 40), (640, 300, 48, 36)]:
        b += casa(x, y, w, h, "#EFDDB8")
    # suelo y olivos
    b += '<path d="M0 372 C200 350 420 384 800 360 V450 H0 Z" fill="#9C7A4A"/>'
    b += olivo(80, 410, 1.1) + olivo(700, 416, 1.2) + olivo(560, 400, 0.8)
    return doc(b, d)


def betesda():
    d, s = cielo("c", "#CFE6F2", "#F6EFD4")
    b = s
    b += '<rect y="110" width="800" height="200" fill="#D9C49A"/><rect y="100" width="800" height="14" fill="#B39A68"/>'
    b += almenas(0, 100, 800, "#B39A68", 24, 10, 14)
    # puerta de las ovejas
    b += '<path d="M120 310 V190 A70 70 0 0 1 260 190 V310 Z" fill="#3A2A1C"/>'
    b += '<path d="M138 310 V192 A52 52 0 0 1 242 192 V310 Z" fill="#7A5B3A"/>'
    b += oveja(300, 336) + oveja(344, 348) + oveja(90, 346)
    # cinco pórticos y estanque
    for i in range(5):
        x = 330 + i * 86
        b += f'<path d="M{x} 304 V250 A40 40 0 0 1 {x + 80} 250 V304 Z" fill="#BFA878"/>'
    b += columnas(322, 240, 6, 86, 70, 14)
    b += '<rect x="300" y="304" width="470" height="20" fill="#CBB68A"/>'
    d2, a = lago(324, "#8CC0DA", "#4E8DB0", "agua")
    d += d2
    b += '<rect x="310" y="324" width="450" height="106" rx="12" fill="url(#agua)"/>'
    b += '<g fill="none" stroke="#FFFFFF" stroke-opacity="0.5" stroke-width="3"><ellipse cx="480" cy="374" rx="70" ry="12"/><ellipse cx="640" cy="396" rx="60" ry="10"/></g>'
    b += '<rect y="430" width="800" height="20" fill="#A98F5F"/>'
    return doc(b, d)


def siloe():
    d, s = cielo("c", "#BFE0F0", "#F7F1D8")
    b = s + sol(150, 90, 30, "#FFF3C9", "#FFFFFF")
    b += '<path d="M0 300 C120 230 220 240 330 262 L330 450 H0 Z" fill="#B39A68"/>'
    b += '<path d="M60 300 A40 40 0 0 1 140 300 V330 H60 Z" fill="#2B1F18"/>'  # boca del túnel
    b += '<path d="M100 330 C140 346 190 350 250 346" stroke="#7FB2D0" stroke-width="12" fill="none" stroke-linecap="round"/>'
    b += '<rect x="610" y="120" width="76" height="190" fill="#D9C49A"/>' + almenas(610, 120, 76, "#D9C49A", 20, 12, 12)
    b += '<rect x="620" y="170" width="14" height="30" rx="6" fill="#4A3A2A"/><rect x="662" y="170" width="14" height="30" rx="6" fill="#4A3A2A"/>'
    b += '<rect x="240" y="280" width="380" height="40" fill="#CBB68A"/>'
    # estanque con escalones
    b += '<polygon points="250,320 610,320 670,430 190,430" fill="#6FA8C9"/>'
    b += '<polygon points="250,320 610,320 640,372 220,372" fill="#8CC0DA"/>'
    for i, y in enumerate([340, 360, 380, 402]):
        b += f'<line x1="{250 - (y - 320) * 0.55:.0f}" y1="{y}" x2="{610 + (y - 320) * 0.55:.0f}" y2="{y}" stroke="#FFFFFF" stroke-opacity="0.35" stroke-width="3"/>'
    b += '<g fill="none" stroke="#FFFFFF" stroke-opacity="0.55" stroke-width="3"><ellipse cx="430" cy="392" rx="60" ry="10"/></g>'
    b += palma(720, 440, 130, 0.9)
    return doc(b, d)


def betania():
    d, s = cielo("c", "#4B3F6B", "#F0B27A")
    b = s + sol(160, 150, 26, "#FFE9A8")
    b += '<path d="M0 450 V230 C160 200 330 250 520 300 C650 332 740 340 800 346 V450 Z" fill="#8F7650"/>'
    b += '<path d="M0 450 V320 C200 300 380 340 560 372 C660 390 740 392 800 396 V450 Z" fill="#7A6444"/>'
    for x, y, w, h in [(250, 262, 46, 34), (330, 280, 52, 38), (420, 300, 44, 34), (500, 322, 54, 38), (590, 344, 46, 32), (150, 262, 42, 30)]:
        b += casa(x, y, w, h, "#E9D8B7", luz=True)
    b += olivo(80, 300, 1.0) + olivo(610, 330, 0.8) + olivo(700, 390, 1.1) + olivo(380, 360, 0.9) + olivo(200, 330, 0.7)
    b += '<path d="M120 450 C220 410 330 380 440 372 C520 366 600 376 680 400" stroke="#CDB586" stroke-width="12" fill="none" stroke-linecap="round" opacity="0.8"/>'
    return doc(b, d)


def efrain():
    d, s = cielo("c", "#F5D79B", "#FBEBC8")
    b = s + sol(620, 110, 40, "#FFFBEA", "#FFF3C9")
    b += '<path d="M0 260 L120 210 L220 250 L330 200 L450 256 L560 214 L700 260 L800 230 V330 H0 Z" fill="#B9936A"/>'
    b += '<path d="M0 320 C160 280 320 330 480 300 C620 276 720 316 800 296 V450 H0 Z" fill="#E7C98E"/>'
    b += '<path d="M0 380 C180 350 360 396 540 366 C660 346 740 380 800 366 V450 H0 Z" fill="#D9B572"/>'
    for x, y, w, h in [(330, 298, 40, 28), (380, 292, 48, 34), (440, 300, 36, 26)]:
        b += casa(x, y, w, h, "#EEDDB5")
    # acacia
    b += '<path d="M150 400 C154 372 148 352 156 332" stroke="#5C4328" stroke-width="8" fill="none" stroke-linecap="round"/>'
    b += '<ellipse cx="156" cy="324" rx="56" ry="14" fill="#7E8F5E"/><ellipse cx="146" cy="316" rx="38" ry="10" fill="#94A26E"/>'
    b += '<path d="M0 430 C200 410 400 440 800 420 V450 H0 Z" fill="#C9A15A"/>'
    return doc(b, d)


def sicar():
    d, s = cielo("c", "#9CCBE6", "#F7EFD2")
    b = s + sol(120, 90, 28, "#FFF3C9", "#FFFFFF")
    # monte Garizín
    b += '<path d="M0 300 C120 270 220 200 330 150 C400 118 470 128 540 170 C640 230 720 270 800 286 V450 H0 Z" fill="#B7A27A"/>'
    b += '<path d="M0 340 C160 310 300 260 420 236 C560 210 700 280 800 320 V450 H0 Z" fill="#9DB07A"/>'
    b += '<path d="M0 392 C200 360 420 400 800 372 V450 H0 Z" fill="#7E9A5E"/>'
    # pozo de Jacob
    b += '<path d="M310 360 V404 C310 428 490 428 490 404 V360 Z" fill="#BFAE8A"/>'
    for y in (376, 394, 410):
        b += f'<path d="M312 {y} C380 {y + 12} 420 {y + 12} 488 {y}" stroke="#9C8B68" stroke-width="3" fill="none"/>'
    b += '<ellipse cx="400" cy="360" rx="90" ry="24" fill="#D8C8A2"/><ellipse cx="400" cy="360" rx="70" ry="17" fill="#2B1F18"/>'
    b += '<rect x="318" y="270" width="10" height="92" fill="#5C4328"/><rect x="472" y="270" width="10" height="92" fill="#5C4328"/>'
    b += '<rect x="310" y="262" width="180" height="12" rx="4" fill="#6B4A2B"/>'
    b += '<line x1="400" y1="274" x2="400" y2="336" stroke="#4A3A2A" stroke-width="3"/>'
    b += '<path d="M386 336 H414 L410 358 H390 Z" fill="#8A5E2E"/>'
    b += tinaja(560, 410, 0.55)
    return doc(b, d)


def cana():
    d, s = cielo("c", "#3E3B63", "#E7A06A")
    b = s
    b += '<path d="M0 330 C200 310 420 340 800 318 V450 H0 Z" fill="#7A5B3A"/>'
    for x, y, w, h in [(40, 230, 150, 110), (240, 250, 130, 90), (430, 236, 160, 104), (640, 252, 130, 88)]:
        b += casa(x, y, w, h, "#E9D8B7", luz=True)
    # guirnalda de lámparas
    b += '<path d="M190 240 C240 290 290 290 340 262 C400 232 460 232 520 252 C570 268 620 268 660 256" stroke="#4A3A2A" stroke-width="3" fill="none"/>'
    for cx, cy in [(230, 276), (270, 288), (310, 282), (370, 248), (420, 238), (470, 242), (560, 266), (610, 270)]:
        b += f'<circle cx="{cx}" cy="{cy}" r="14" fill="#FFD36B" opacity="0.3"/><circle cx="{cx}" cy="{cy}" r="6" fill="#FFE39A"/>'
    b += tinaja(210, 380, 0.5) + tinaja(250, 388, 0.5) + tinaja(600, 384, 0.5)
    b += palma(740, 400, 140, 0.8)
    return doc(b, d)


def cafarnaum():
    d, s = cielo("c", "#BFE0F0", "#F7F1D8")
    b = s + sol(650, 90, 28, "#FFF3C9", "#FFFFFF")
    b += '<path d="M0 230 C140 190 300 220 460 200 C600 184 700 214 800 196 V300 H0 Z" fill="#A9B59A"/>'
    d2, a = lago(280, "#8FB6CB", "#3C6D8C")
    d += d2
    b += a + ondas(280)
    b += barca(190, 330, 0.8, True) + barca(560, 360, 0.7, True)
    # orilla
    b += '<path d="M0 380 C200 360 420 392 800 366 V450 H0 Z" fill="#CDB586"/>'
    # sinagoga de basalto
    b += '<rect x="250" y="262" width="250" height="108" fill="#4D4B4A"/>'
    b += '<polygon points="236,262 375,208 514,262" fill="#3E3C3B"/>'
    b += columnas(268, 280, 5, 54, 90, 16, "#6A6766", "#4A4847")
    b += '<rect x="352" y="318" width="46" height="52" rx="18" fill="#242220"/>'
    # redes tendidas
    b += '<line x1="580" y1="330" x2="580" y2="388" stroke="#5C4328" stroke-width="5"/><line x1="720" y1="330" x2="720" y2="388" stroke="#5C4328" stroke-width="5"/>'
    b += '<path d="M580 336 C620 372 680 372 720 336 L720 360 C680 392 620 392 580 360 Z" fill="#E2D2A6" opacity="0.8"/>'
    return doc(b, d)


def tiberiades():
    d, s = cielo("c", "#BFE0F0", "#F7F1D8")
    b = s + sol(120, 90, 28, "#FFF3C9", "#FFFFFF")
    b += '<path d="M0 220 C140 160 300 200 460 170 C600 144 700 190 800 170 V330 H0 Z" fill="#A9B59A"/>'
    # teatro
    b += '<path d="M470 250 A90 70 0 0 1 650 250 Z" fill="#E0CFA6"/>'
    for r in (70, 52, 34):
        b += f'<path d="M{560 - r * 1.28:.0f} 250 A{r * 1.28:.0f} {r} 0 0 1 {560 + r * 1.28:.0f} 250" fill="none" stroke="#C4B083" stroke-width="3"/>'
    # ciudad con tejados rojos
    for x, y, w, h in [(110, 260, 56, 48), (180, 250, 62, 58), (256, 266, 50, 42), (330, 248, 66, 60), (672, 262, 52, 46), (734, 252, 48, 56)]:
        b += casa_teja(x, y, w, h)
    # torre y columnata
    b += '<rect x="408" y="206" width="38" height="104" fill="#D9C49A"/>' + almenas(408, 206, 38, "#D9C49A", 18, 10, 10)
    b += '<rect x="110" y="304" width="680" height="12" fill="#CBB68A"/>' + columnas(130, 280, 12, 52, 26, 10)
    d2, a = lago(316, "#7FA6BF", "#2F5D7A")
    d += d2
    b += a + ondas(316)
    b += barca(250, 370, 0.8, True) + barca(580, 392, 0.7, True)
    return doc(b, d)


def betsaida():
    d, s = cielo("c", "#6E7FA3", "#F6CE8A", "#E9A56A")
    b = s + sol(500, 250, 34)
    # Hermón con nieve
    b += '<path d="M240 270 L420 96 L600 270 Z" fill="#8A93AE"/><path d="M386 130 L420 96 L456 134 L436 126 L420 146 L404 124 Z" fill="#F4F6FA"/>'
    b += '<path d="M0 290 C140 260 280 280 420 264 C560 250 700 280 800 262 V320 H0 Z" fill="#7C8A63"/>'
    d2, a = lago(300, "#7FA6BF", "#2F5D7A")
    d += d2
    b += a + ondas(300)
    # orilla y cabañas de pescadores
    b += '<path d="M0 392 C180 366 420 400 800 374 V450 H0 Z" fill="#B59A66"/>'
    for x in (90, 230, 600):
        b += f'<polygon points="{x},388 {x + 40},330 {x + 80},388" fill="#8A6A3C"/><rect x="{x + 32}" y="360" width="16" height="28" fill="#3A2A1C"/>'
    # barca varada y redes
    b += '<path d="M360 408 Q420 366 480 408 Z" fill="#6B4223"/><rect x="354" y="404" width="132" height="7" rx="3" fill="#8A5E2E"/>'
    b += '<line x1="680" y1="340" x2="680" y2="400" stroke="#5C4328" stroke-width="5"/><line x1="770" y1="340" x2="770" y2="400" stroke="#5C4328" stroke-width="5"/>'
    b += '<path d="M680 346 C710 380 740 380 770 346 L770 370 C740 404 710 404 680 370 Z" fill="#E2D2A6" opacity="0.8"/>'
    return doc(b, d)


def nazaret():
    d, s = cielo("c", "#F3A9A0", "#FCE7B6", "#F7C58E")
    b = s + sol(400, 150, 30, "#FFF1C9", "#FFFFFF")
    b += '<path d="M0 250 C160 200 320 230 460 210 C620 188 720 224 800 206 V450 H0 Z" fill="#A9C98A"/>'
    b += '<path d="M0 300 C180 262 340 296 520 270 C660 250 740 280 800 268 V450 H0 Z" fill="#8DB06A"/>'
    # terrazas de cultivo
    for y, c in [(330, "#7FA45F"), (362, "#759A55"), (396, "#6A8E4C")]:
        b += f'<path d="M0 {y} C200 {y - 22} 420 {y + 12} 800 {y - 12} V450 H0 Z" fill="{c}"/>'
    for x, y, w, h in [(270, 274, 46, 32), (340, 262, 52, 38), (418, 278, 44, 30), (486, 266, 50, 36), (214, 296, 40, 28), (560, 288, 44, 30)]:
        b += casa(x, y, w, h, "#F0E2C4", "#D2BE96")
    # higuera y camino
    b += '<path d="M120 400 C124 380 118 366 126 350" stroke="#6B5A3E" stroke-width="8" fill="none" stroke-linecap="round"/>'
    b += '<circle cx="110" cy="338" r="26" fill="#6F9A58"/><circle cx="138" cy="334" r="24" fill="#86AE6A"/><circle cx="124" cy="318" r="22" fill="#6F9A58"/>'
    b += '<path d="M700 450 C640 410 560 380 470 330" stroke="#E4D2A6" stroke-width="12" fill="none" stroke-linecap="round" opacity="0.85"/>'
    return doc(b, d)


def contexto():
    d = ""
    b = '<rect width="800" height="450" fill="#EAD9B3"/>'
    b += '<rect x="14" y="14" width="772" height="422" rx="10" fill="none" stroke="#A98F5F" stroke-width="5"/>'
    # mar Mediterráneo y costa
    b += '<path d="M14 14 H300 C320 90 280 160 300 230 C320 300 350 360 340 436 H14 Z" fill="#8CB8D0"/>'
    b += '<path d="M300 14 C320 90 280 160 300 230 C320 300 350 360 340 436" fill="none" stroke="#B49A66" stroke-width="5"/>'
    # tierra
    b += '<path d="M300 14 H786 V436 H340 C350 360 320 300 300 230 C280 160 320 90 300 14 Z" fill="#E4CFA0"/>'
    # mar de Galilea, Jordán y mar Muerto
    b += '<ellipse cx="520" cy="130" rx="40" ry="54" fill="#8CB8D0"/>'
    b += '<path d="M522 184 C500 230 540 270 520 310 C508 336 540 346 548 352" stroke="#8CB8D0" stroke-width="9" fill="none" stroke-linecap="round"/>'
    b += '<ellipse cx="574" cy="384" rx="30" ry="46" fill="#6FA0BA"/>'
    # colinas
    b += '<path d="M660 60 C700 100 700 160 740 200" stroke="#C9AE7A" stroke-width="22" fill="none" stroke-linecap="round" opacity="0.6"/>'
    # ruta de Galilea a Jerusalén
    b += '<path d="M470 130 C450 190 470 240 462 280 C456 310 480 320 482 336" stroke="#7B1E2B" stroke-width="3" fill="none" stroke-dasharray="8 7"/>'
    # ciudades
    for cx, cy, r, col in [(482, 336, 11, "#7B1E2B"), (462, 270, 7, "#8A6D3B"), (470, 120, 7, "#8A6D3B"),
                           (496, 150, 7, "#8A6D3B"), (440, 150, 7, "#8A6D3B"), (420, 112, 7, "#8A6D3B"), (504, 96, 7, "#8A6D3B")]:
        b += f'<circle cx="{cx}" cy="{cy}" r="{r + 5}" fill="#FFFFFF" opacity="0.7"/><circle cx="{cx}" cy="{cy}" r="{r}" fill="{col}"/>'
    # águila y laurel de Roma: estandarte
    b += '<g transform="translate(150 330)"><line x1="0" y1="-120" x2="0" y2="60" stroke="#5C4328" stroke-width="6"/>'
    b += '<rect x="-30" y="-92" width="60" height="44" fill="#7B1E2B"/><circle cx="0" cy="-130" r="14" fill="#C79A3B"/>'
    b += '<path d="M-26 -136 Q0 -158 26 -136 Q0 -122 -26 -136 Z" fill="#C79A3B"/></g>'
    return doc(b, d)


ESCENAS = {
    "jerusalen": jerusalen,
    "betesda": betesda,
    "siloe": siloe,
    "betania": betania,
    "efrain": efrain,
    "sicar": sicar,
    "cana": cana,
    "cafarnaum": cafarnaum,
    "tiberiades": tiberiades,
    "betsaida": betsaida,
    "nazaret": nazaret,
    "contexto": contexto,
}

if __name__ == "__main__":
    os.makedirs(SALIDA, exist_ok=True)
    for nombre, fn in ESCENAS.items():
        with open(os.path.join(SALIDA, nombre + ".svg"), "w", encoding="utf-8") as f:
            f.write(fn())
        print("SVG", nombre)
