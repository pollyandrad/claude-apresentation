"""Recria a logo CAISA em vetor monocromático (uso: marca d'água clarinha de fundo).

Releitura feita a partir da imagem de referência enviada pela cliente: anel externo,
"C" serifado envolvendo meio cérebro e uma taça com caduceu alado, e "CAISA" embaixo.
Não substitui o arquivo oficial da marca.
Uso: python3 marcela-designs/logo/recriar_logo.py
"""
import math
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

AQUI = Path(__file__).parent
FONTE = TTFont(AQUI / "_fonte" / "CormorantGaramond-Medium.ttf")
GS = FONTE.getGlyphSet()
CMAP = FONTE.getBestCmap()
UPM = FONTE["head"].unitsPerEm
CAP = FONTE["OS/2"].sCapHeight or 0.63 * UPM


def glifo(ch, x, base, altura_caixa_alta):
    """Path SVG de um caractere, com a caixa alta medindo `altura_caixa_alta`."""
    nome = CMAP[ord(ch)]
    s = altura_caixa_alta / CAP
    pen = SVGPathPen(GS)
    GS[nome].draw(TransformPen(pen, (s, 0, 0, -s, x, base)))
    return pen.getCommands(), GS[nome].width * s


def palavra(txt, cx, base, alt, espaco):
    larguras = [glifo(c, 0, 0, alt)[1] for c in txt]
    total = sum(larguras) + espaco * (len(txt) - 1)
    x = cx - total / 2
    d = []
    for c, w in zip(txt, larguras):
        d.append(glifo(c, x, base, alt)[0])
        x += w + espaco
    return " ".join(d)


def cobra(x0, y0, y1, amp, fase, passos=60):
    pts = []
    for i in range(passos + 1):
        t = i / passos
        y = y0 + (y1 - y0) * t
        a = amp * (1 - 0.35 * t)
        pts.append((x0 + a * math.sin(fase + t * 2.6 * math.pi), y))
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)


def asa(cx, y, lado):
    """Três penas afinando, para um lado (+1 direita, -1 esquerda)."""
    d = []
    for i, (comp, dy) in enumerate([(80, 0), (64, 13), (46, 26)]):
        x0 = cx + lado * 8
        x1 = cx + lado * (8 + comp)
        d.append(f"M{x0} {y + dy} Q{(x0 + x1) / 2} {y + dy - 10 + i * 2} {x1} {y + dy - 14 + i * 4}")
    return " ".join(d)


C_path = glifo("C", 318, 568, 360)[0]
caisa = palavra("CAISA", 512, 752, 80, 24)

# meio cérebro (hemisfério esquerdo), lado reto à direita
cerebro_contorno = (
    "M498 300 L498 492 "
    "C478 500 458 496 452 482 C430 488 410 474 414 452 C394 446 388 424 400 410 "
    "C384 398 384 374 400 364 C390 346 398 324 418 322 C420 302 442 290 462 298 "
    "C472 288 490 290 498 300 Z"
)
cerebro_sulcos = " ".join([
    "M498 330 C480 326 470 340 478 352 C486 362 474 374 460 368",
    "M440 312 C448 330 434 340 424 336",
    "M498 392 C482 384 466 392 470 406 C474 420 458 428 446 418",
    "M412 386 C426 380 438 392 432 404",
    "M498 452 C484 444 470 452 474 466",
    "M434 446 C444 438 456 446 452 460",
])

taca = "M548 352 C536 432 566 478 612 480 C658 478 688 432 676 352"
base_taca = "M576 492 L648 492 M588 503 L636 503"
haste = "M612 300 L612 476"
cobras = cobra(612, 330, 452, 16, 0) + " " + cobra(612, 330, 452, 16, math.pi)
asas = asa(612, 312, -1) + " " + asa(612, 312, 1)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="262 148 500 624">
  <!-- Releitura monocromática da logo CAISA para marca d'água. Não é o arquivo oficial. -->
  <g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round">
    <circle cx="512" cy="395" r="236" stroke-width="9"/>
    <path d="{cerebro_contorno}" stroke-width="7"/>
    <path d="{cerebro_sulcos}" stroke-width="6"/>
    <path d="{taca}" stroke-width="9"/>
    <path d="{base_taca}" stroke-width="7"/>
    <path d="{haste}" stroke-width="6"/>
    <path d="{cobras}" stroke-width="5"/>
    <path d="{asas}" stroke-width="6"/>
  </g>
  <g fill="currentColor">
    <circle cx="612" cy="294" r="8"/>
    <path d="{C_path}"/>
    <path d="{caisa}"/>
  </g>
</svg>
'''
(AQUI / "caisa-logo-releitura.svg").write_text(svg)
for nome, cor in [("verde-claro", "#BAD986"), ("off-white", "#F6F6F2"), ("verde-musgo", "#374325")]:
    (AQUI / f"caisa-logo-releitura_{nome}.svg").write_text(svg.replace("currentColor", cor))
print("ok")
