#!/usr/bin/env python3
"""Genera las ilustraciones de portada de los temas del folleto (ilustraciones/temaN.svg).

Mismo estilo plano que las de personajes y ciudades: escenas sencillas, sin rostros.
"""
import os

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ilustraciones")
PIEL = "#D9A877"


def svg(cuerpo, defs=""):
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 450" width="800" height="450">\n'
        f"<defs>{defs}</defs>\n{cuerpo}\n</svg>\n"
    )


def degradado(id_, *paradas):
    s = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in paradas)
    return f'<linearGradient id="{id_}" x1="0" y1="0" x2="0" y2="1">{s}</linearGradient>'


def persona(x, y, esc=1.0, tunica="#8A6B4A", manto=None, brazo=None, cabeza=PIEL, aureola=False, pelo=None):
    """Figura sencilla. (x, y) = centro de los pies. brazo: 'arriba' o 'adelante'."""
    g = [f'<g transform="translate({x} {y}) scale({esc})">']
    g.append(f'<path d="M-22 0 L-15 -78 Q0 -88 15 -78 L22 0 Z" fill="{tunica}"/>')
    if manto:
        g.append(f'<path d="M-15 -78 Q0 -88 15 -78 L22 0 L6 0 L0 -60 Z" fill="{manto}"/>')
    if brazo == "arriba":
        g.append(f'<path d="M12 -74 L34 -118" stroke="{tunica}" stroke-width="9" stroke-linecap="round"/>')
        g.append(f'<circle cx="35" cy="-122" r="5" fill="{cabeza}"/>')
    elif brazo == "adelante":
        g.append(f'<path d="M12 -70 L38 -62" stroke="{tunica}" stroke-width="9" stroke-linecap="round"/>')
        g.append(f'<circle cx="40" cy="-61" r="5" fill="{cabeza}"/>')
    g.append(f'<circle cx="0" cy="-98" r="13" fill="{cabeza}"/>')
    if pelo:
        g.append(f'<path d="M-13 -100 Q0 -118 13 -100 Q8 -106 0 -106 Q-8 -106 -13 -100 Z" fill="{pelo}"/>')
    if aureola:
        g.append('<circle cx="0" cy="-98" r="22" fill="none" stroke="#FFE9A8" stroke-width="3" opacity="0.9"/>')
    g.append("</g>")
    return "".join(g)


def paloma(x, y, esc=1.0):
    return (
        f'<g transform="translate({x} {y}) scale({esc})">'
        '<path d="M-42 -6 Q-22 -34 0 -8 Q-18 -14 -42 -6 Z" fill="#FFFFFF"/>'
        '<path d="M42 -6 Q22 -34 0 -8 Q18 -14 42 -6 Z" fill="#F1F4F8"/>'
        '<ellipse cx="0" cy="2" rx="14" ry="9" fill="#FFFFFF"/>'
        '<circle cx="-12" cy="-5" r="6" fill="#FFFFFF"/>'
        '<path d="M-18 -5 L-26 -3 L-18 -1 Z" fill="#E9A56A"/>'
        '<path d="M12 4 L30 12 L12 10 Z" fill="#E6EAF0"/>'
        "</g>"
    )


def rayos(cx, cy, n, r1, r2, color="#FFE9A8", op=0.55, ancho=5):
    import math

    s = []
    for i in range(n):
        a = 2 * math.pi * i / n
        x1, y1 = cx + r1 * math.cos(a), cy + r1 * math.sin(a)
        x2, y2 = cx + r2 * math.cos(a), cy + r2 * math.sin(a)
        s.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}"/>')
    return f'<g stroke="{color}" stroke-width="{ancho}" stroke-linecap="round" opacity="{op}">{"".join(s)}</g>'


def barca(x, y, esc=1.0, vela=True):
    v = (
        '<line x1="0" y1="-70" x2="0" y2="-2" stroke="#4A3A2A" stroke-width="4"/>'
        '<path d="M3 -66 L3 -6 L48 -6 Z" fill="#F1E6CC"/>'
        if vela
        else ""
    )
    return (
        f'<g transform="translate({x} {y}) scale({esc})">'
        '<path d="M-60 0 L60 0 Q48 30 20 32 L-20 32 Q-48 30 -60 0 Z" fill="#6B4223"/>'
        '<rect x="-60" y="-4" width="120" height="6" rx="3" fill="#8A5E2E"/>'
        f"{v}</g>"
    )


def olas(x, y, n=3, color="#FFFFFF", op=0.45):
    return "".join(
        f'<path d="M{x + i * 30} {y + i * 18} q18 -6 36 0 t36 0 t36 0" stroke="{color}" stroke-opacity="{op}" '
        'stroke-width="3" fill="none" stroke-linecap="round"/>'
        for i in range(n)
    )


# ---------------------------------------------------------------- Tema 1
def tema1():
    d = degradado("c", (0, "#2F4F6F"), (0.65, "#EBB27A"), (1, "#F8DCA0"))
    cuerpo = [
        '<rect width="800" height="450" fill="url(#c)"/>',
        '<circle cx="400" cy="250" r="70" fill="#FFE9A8"/>',
        rayos(400, 250, 28, 90, 170),
        '<path d="M0 330 C200 296 420 312 800 292 V450 H0 Z" fill="#B9A06A"/>',
        '<path d="M0 372 C240 344 520 364 800 340 V450 H0 Z" fill="#8F7A4D"/>',
    ]
    figuras = [
        (110, 392, 1.0, "#7C8CA8", None, None),
        (205, 382, 1.08, "#A5483F", "#E9D9B0", None),
        (300, 376, 1.0, "#5E7F5A", None, "adelante"),
        (400, 372, 1.18, "#F1E6CC", "#C9A24B", "arriba"),
        (500, 376, 1.0, "#8A5E8F", None, None),
        (595, 382, 1.08, "#B98B3C", "#6B4223", None),
        (690, 392, 1.0, "#3F6B86", None, "adelante"),
    ]
    for x, y, e, t, m, b in figuras:
        cuerpo.append(persona(x, y, e, t, m, b, aureola=(x == 400), pelo="#4A3322"))
    return svg("".join(cuerpo), d)


# ---------------------------------------------------------------- Tema 2
def tema2():
    d = degradado("c", (0, "#1B2A41"), (1, "#4B5D7A")) + (
        '<radialGradient id="luz" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#FFE9A8" stop-opacity="0.85"/>'
        '<stop offset="1" stop-color="#FFE9A8" stop-opacity="0"/></radialGradient>'
    )
    cuerpo = [
        '<rect width="800" height="450" fill="url(#c)"/>',
        '<rect y="360" width="800" height="90" fill="#5A3E26"/>',
        '<circle cx="400" cy="250" r="230" fill="url(#luz)"/>',
        rayos(400, 120, 14, 40, 150, op=0.35, ancho=4),
        paloma(400, 100, 1.3),
        # atril
        '<path d="M360 372 L440 372 L420 318 L380 318 Z" fill="#6B4223"/>',
        '<rect x="388" y="300" width="24" height="22" fill="#6B4223"/>',
        # libro abierto
        '<path d="M400 262 Q340 244 270 262 L270 322 Q340 304 400 322 Z" fill="#F4E8C8" stroke="#CDB68A" stroke-width="3"/>',
        '<path d="M400 262 Q460 244 530 262 L530 322 Q460 304 400 322 Z" fill="#FBF3DC" stroke="#CDB68A" stroke-width="3"/>',
        '<g stroke="#B9A57A" stroke-width="2.5" opacity="0.8">'
        + "".join(f'<line x1="290" y1="{276 + i * 9}" x2="385" y2="{274 + i * 9}"/>' for i in range(5))
        + "".join(f'<line x1="415" y1="{274 + i * 9}" x2="510" y2="{276 + i * 9}"/>' for i in range(5))
        + "</g>",
        # velas
        '<rect x="170" y="318" width="26" height="54" rx="3" fill="#F1E6CC"/>',
        '<path d="M183 316 C168 298 178 284 183 270 C190 284 200 298 183 316 Z" fill="#F28C28"/>',
        '<path d="M183 314 C176 302 181 294 183 288 C187 294 192 302 183 314 Z" fill="#FFD36B"/>',
        '<rect x="604" y="332" width="22" height="40" rx="3" fill="#F1E6CC"/>',
        '<path d="M615 330 C602 314 610 302 615 290 C620 302 628 314 615 330 Z" fill="#F28C28"/>',
        '<path d="M615 328 C609 318 613 311 615 306 C618 311 622 318 615 328 Z" fill="#FFD36B"/>',
    ]
    return svg("".join(cuerpo), d)


# ---------------------------------------------------------------- Tema 3
def tema3():
    d = degradado("c", (0, "#6B4A36"), (1, "#C98F57"))
    cuerpo = [
        '<rect width="800" height="450" fill="url(#c)"/>',
        # ventana con arco
        '<path d="M330 250 V120 Q400 40 470 120 V250 Z" fill="#2F3F5C"/>',
        '<circle cx="400" cy="130" r="9" fill="#FFE9A8"/><circle cx="360" cy="165" r="5" fill="#FFE9A8"/><circle cx="440" cy="170" r="6" fill="#FFE9A8"/>',
        '<rect y="360" width="800" height="90" fill="#4A3322"/>',
        # lámpara
        '<line x1="640" y1="0" x2="640" y2="110" stroke="#3E2B19" stroke-width="4"/>',
        '<ellipse cx="640" cy="130" rx="24" ry="16" fill="#8A5E2E"/>',
        '<path d="M640 108 C626 92 634 80 640 66 C646 80 654 92 640 108 Z" fill="#F28C28"/>',
        '<circle cx="640" cy="120" r="70" fill="#FFE9A8" opacity="0.18"/>',
        # personas: el amado se recuesta sobre el pecho del Maestro
        persona(335, 330, 1.25, "#5E7F5A", None, None, pelo="#4A3322"),
        persona(445, 330, 1.35, "#F1E6CC", "#B04A3F", "adelante", aureola=True, pelo="#4A3322"),
        # el discípulo se inclina hacia Jesús
        '<g transform="translate(335 330) scale(1.25)"><path d="M0 -86 Q18 -92 34 -78" stroke="#5E7F5A" stroke-width="8" fill="none" stroke-linecap="round"/></g>',
        # mesa
        '<rect x="120" y="318" width="560" height="22" rx="6" fill="#8A5E2E"/>',
        '<rect x="140" y="338" width="14" height="74" fill="#6B4223"/><rect x="646" y="338" width="14" height="74" fill="#6B4223"/>',
        '<path d="M150 318 H650 V334 Q400 350 150 334 Z" fill="#F4ECD6"/>',
        # pan, copa, uvas
        '<ellipse cx="250" cy="312" rx="38" ry="10" fill="#C9A24B"/>',
        '<ellipse cx="250" cy="304" rx="30" ry="12" fill="#E4B766"/>',
        '<path d="M520 316 L534 316 L538 286 L516 286 Z" fill="#C0C7D2"/>',
        '<rect x="522" y="316" width="6" height="8" fill="#C0C7D2"/><rect x="512" y="322" width="26" height="4" rx="2" fill="#C0C7D2"/>',
        '<path d="M517 290 L537 290 L536 298 L518 298 Z" fill="#8E2B3A"/>',
        '<g fill="#6A3B7A"><circle cx="585" cy="308" r="8"/><circle cx="600" cy="308" r="8"/><circle cx="592" cy="296" r="8"/></g>',
    ]
    return svg("".join(cuerpo), d)


# ---------------------------------------------------------------- Tema 4
def tema4():
    d = degradado("c", (0, "#33507A"), (0.55, "#E9A56A"), (1, "#F8DCA0")) + degradado(
        "rio", (0, "#7FA6BF"), (1, "#2F5D7A")
    )
    cuerpo = [
        '<rect width="800" height="450" fill="url(#c)"/>',
        '<circle cx="610" cy="220" r="60" fill="#FFE9A8"/>',
        '<path d="M0 290 C120 230 260 250 380 285 C500 250 660 230 800 280 V450 H0 Z" fill="#D6AE72"/>',
        '<path d="M0 330 C180 296 380 330 560 316 C660 308 740 318 800 330 V450 H0 Z" fill="#C0945A"/>',
        '<path d="M0 380 C200 360 420 392 800 368 V450 H0 Z" fill="url(#rio)"/>',
        olas(60, 398, 2),
        olas(470, 400, 2),
        # cactus / arbusto seco
        '<g stroke="#6E5535" stroke-width="4" fill="none" stroke-linecap="round"><path d="M110 330 L110 296 M110 312 L96 300 M110 318 L124 304"/></g>',
        # el Bautista: túnica de pelo de camello, brazo en alto
        persona(330, 372, 1.5, "#8A6B4A", None, "arriba", pelo="#3A2A1C"),
        '<g transform="translate(330 372) scale(1.5)" stroke="#6B4F33" stroke-width="2" opacity="0.7"><line x1="-12" y1="-60" x2="-8" y2="-52"/><line x1="-2" y1="-50" x2="2" y2="-42"/><line x1="8" y1="-40" x2="12" y2="-32"/><line x1="-10" y1="-30" x2="-6" y2="-22"/><line x1="2" y1="-22" x2="6" y2="-14"/></g>',
        '<rect x="316" y="324" width="28" height="5" rx="2" fill="#4A3320"/>',
        # voz: ondas desde la boca / mano
        '<g fill="none" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" opacity="0.8">'
        '<path d="M410 232 q22 -22 0 -44"/><path d="M432 240 q36 -30 0 -60"/><path d="M456 248 q50 -38 0 -76"/></g>',
    ]
    return svg("".join(cuerpo), d)


# ---------------------------------------------------------------- Tema 5
def cordero(x, y, esc=1.0):
    return (
        f'<g transform="translate({x} {y}) scale({esc})">'
        '<g fill="#4A3A2A"><rect x="-34" y="0" width="8" height="30" rx="3"/><rect x="-14" y="2" width="8" height="28" rx="3"/>'
        '<rect x="12" y="2" width="8" height="28" rx="3"/><rect x="32" y="0" width="8" height="30" rx="3"/></g>'
        '<g fill="#FFFFFF" stroke="#D9DEE6" stroke-width="2"><circle cx="-28" cy="-12" r="22"/><circle cx="-6" cy="-24" r="24"/>'
        '<circle cx="20" cy="-22" r="24"/><circle cx="40" cy="-8" r="22"/><circle cx="6" cy="0" r="22"/></g>'
        '<ellipse cx="-58" cy="-20" rx="16" ry="18" fill="#3A2F27"/>'
        '<ellipse cx="-70" cy="-34" rx="10" ry="5" fill="#3A2F27" transform="rotate(-30 -70 -34)"/>'
        '<circle cx="-64" cy="-24" r="2.4" fill="#FFFFFF"/>'
        # estandarte con cruz
        '<line x1="30" y1="-30" x2="30" y2="-100" stroke="#7A5A33" stroke-width="4"/>'
        '<path d="M30 -100 L78 -90 L30 -78 Z" fill="#FFFFFF" stroke="#C0C7D2" stroke-width="2"/>'
        '<path d="M52 -96 V-82 M45 -90 H59" stroke="#B04A3F" stroke-width="3"/>'
        "</g>"
    )


def tema5():
    d = degradado("c", (0, "#8FB8D6"), (1, "#F8EBCB")) + degradado("rio", (0, "#7DB0CE"), (1, "#386F92"))
    cuerpo = [
        '<rect width="800" height="450" fill="url(#c)"/>',
        rayos(480, 80, 16, 36, 150, color="#FFFFFF", op=0.6, ancho=6),
        paloma(480, 80, 1.5),
        '<path d="M0 300 C200 276 420 292 800 272 V450 H0 Z" fill="#A9B788"/>',
        '<rect y="352" width="800" height="98" fill="url(#rio)"/>',
        olas(80, 380, 3),
        olas(520, 392, 2),
        # el Bautista señala
        persona(170, 372, 1.5, "#8A6B4A", None, "arriba", pelo="#3A2A1C"),
        # el Cordero
        cordero(520, 340, 1.4),
    ]
    return svg("".join(cuerpo), d)


# ---------------------------------------------------------------- Tema 6
def tema6():
    d = degradado("c", (0, "#1F3B57"), (0.5, "#6E86B4"), (1, "#F6CE8A"))
    cuerpo = [
        '<rect width="800" height="450" fill="url(#c)"/>',
        # sol que crece, a la derecha
        '<circle cx="560" cy="250" r="150" fill="#FFE9A8" opacity="0.35"/>',
        '<circle cx="560" cy="250" r="110" fill="#FFE9A8" opacity="0.6"/>',
        '<circle cx="560" cy="250" r="78" fill="#FFF3C4"/>',
        rayos(560, 250, 24, 130, 230, op=0.5, ancho=6),
        # luna / estrella pequeña que disminuye, a la izquierda
        '<circle cx="150" cy="110" r="22" fill="#E9EEF7"/><circle cx="160" cy="104" r="19" fill="#2B4968"/>',
        '<circle cx="110" cy="170" r="3" fill="#E9EEF7"/><circle cx="200" cy="60" r="2.5" fill="#E9EEF7"/><circle cx="60" cy="90" r="2" fill="#E9EEF7"/>',
        '<path d="M0 340 C200 316 420 332 800 312 V450 H0 Z" fill="#7C8CA8"/>',
        '<path d="M0 390 C240 364 520 384 800 360 V450 H0 Z" fill="#4F5F7D"/>',
        # el Bautista, de rodillas/inclinado hacia la luz
        persona(300, 392, 1.5, "#8A6B4A", None, "adelante", pelo="#3A2A1C"),
        # cruz de luz en el sol
        '<path d="M560 196 V304 M506 250 H614" stroke="#FFFFFF" stroke-width="9" stroke-linecap="round" opacity="0.85"/>',
    ]
    return svg("".join(cuerpo), d)


# ---------------------------------------------------------------- Tema 7
def tema7():
    d = degradado("c", (0, "#1F3B57"), (0.7, "#E9A56A"), (1, "#F6CE8A")) + degradado(
        "lago", (0, "#7FA6BF"), (1, "#2F5D7A")
    )
    red = (
        '<pattern id="red" width="10" height="10" patternUnits="userSpaceOnUse">'
        '<path d="M0 0 L10 10 M10 0 L0 10" stroke="#E2D2A6" stroke-width="1.5"/></pattern>'
    )
    cuerpo = [
        '<rect width="800" height="450" fill="url(#c)"/>',
        '<circle cx="250" cy="222" r="52" fill="#FFE9A8"/>',
        '<rect y="222" width="800" height="228" fill="url(#lago)"/>',
        '<g fill="#FFE9A8"><ellipse cx="250" cy="236" rx="48" ry="5" opacity="0.7"/><ellipse cx="250" cy="256" rx="36" ry="4" opacity="0.5"/>'
        '<ellipse cx="250" cy="274" rx="24" ry="3" opacity="0.35"/></g>',
        barca(150, 300, 0.9),
        '<ellipse cx="105" cy="296" rx="34" ry="13" fill="url(#red)" stroke="#E2D2A6" stroke-width="2"/>',
        # orilla
        '<path d="M300 450 C340 360 480 330 800 336 V450 Z" fill="#C9B47E"/>',
        '<path d="M360 450 C400 392 520 372 800 380 V450 Z" fill="#B59F68"/>',
        # peces y red
        '<g fill="#9DB4C0"><ellipse cx="440" cy="420" rx="22" ry="7"/><polygon points="460,420 474,413 474,427"/>'
        '<ellipse cx="520" cy="432" rx="20" ry="6.5" transform="rotate(-8 520 432)"/><polygon points="538,430 551,423 552,437"/></g>',
        # los primeros discípulos y Jesús
        persona(520, 378, 1.25, "#7C8CA8", None, None, pelo="#4A3322"),
        persona(610, 374, 1.3, "#5E7F5A", None, "adelante", pelo="#3A2A1C"),
        persona(690, 372, 1.25, "#A5483F", None, None, pelo="#4A3322"),
        persona(440, 384, 1.5, "#F1E6CC", "#C9A24B", "adelante", aureola=True, pelo="#4A3322"),
    ]
    return svg("".join(cuerpo), d + red)


def main():
    for i, f in enumerate([tema1, tema2, tema3, tema4, tema5, tema6, tema7], start=1):
        ruta = os.path.join(RAIZ, f"tema{i}.svg")
        with open(ruta, "w", encoding="utf-8") as fh:
            fh.write(f())
        print("OK", ruta)


if __name__ == "__main__":
    main()
