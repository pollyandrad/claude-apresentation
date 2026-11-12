"""Monta o PPTX editável a partir dos fundos e dos textos medidos por render.js.
Cada slide = imagem de fundo (textura + palavra grande) + caixas de texto editáveis.
"""
import json, re
from pathlib import Path
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn

AQUI = Path(__file__).parent
dados = json.loads((AQUI / "fundo" / "pptx" / "dados.json").read_text())
PX = 6350  # 1 px de 1920 → EMU num slide de 13,333 in
prs = Presentation()
prs.slide_width, prs.slide_height = Emu(1920 * PX), Emu(1080 * PX)
vazio = prs.slide_layouts[6]

def cor(css):
    n = [int(float(v)) for v in re.findall(r"[\d.]+", css)[:3]]
    return RGBColor(*n)

for t in dados:
    s = prs.slides.add_slide(vazio)
    s.shapes.add_picture(t["fundo"], 0, 0, prs.slide_width, prs.slide_height)
    if t["foto"]:
        f = t["foto"]
        r = s.shapes.add_shape(1, Emu(int(f["x"] * PX)), Emu(int(f["y"] * PX)), Emu(int(f["w"] * PX)), Emu(int(f["h"] * PX)))
        r.fill.background(); r.line.color.rgb = RGBColor(0xBA, 0xD9, 0x86); r.line.width = Pt(1)
        r.name = "Foto da convidada (substituir pela imagem)"
    for tx in t["textos"]:
        pad = 6
        b = s.shapes.add_textbox(Emu(int((tx["x"] - pad) * PX)), Emu(int((tx["y"] - pad) * PX)), Emu(int((tx["w"] + 2 * pad + 40) * PX)), Emu(int((tx["h"] + 2 * pad) * PX)))
        tf = b.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = Emu(pad * PX)
        tf.vertical_anchor = MSO_ANCHOR.TOP
        p = tf.paragraphs[0]
        if tx["lh"]:
            p.line_spacing = Pt(tx["lh"] * 0.5)
        for run in tx["runs"]:
            partes = run["txt"].split("\n")
            for i, parte in enumerate(partes):
                if i > 0:
                    p = tf.add_paragraph()
                    if tx["lh"]:
                        p.line_spacing = Pt(tx["lh"] * 0.5)
                if not parte:
                    continue
                r = p.add_run()
                r.text = parte.upper() if tx["upper"] else parte
                f = r.font
                f.name = tx["font"]; f.size = Pt(tx["size"] * 0.5); f.italic = run["italic"]; f.color.rgb = cor(run["color"])
                if tx["spacing"]:
                    r._r.get_or_add_rPr().set("spc", str(int(tx["spacing"] * 0.5 * 100)))
        for par in tf.paragraphs:
            par.alignment = PP_ALIGN.LEFT
    s.notes_slide.notes_text_frame.text = f"Tela {t['n']:02d} · {t['arquivo']}. Avance manualmente; sem transições automáticas."

out = AQUI / "saida" / "CAISA-DAY-2026_telas-de-projecao_EDITAVEL.pptx"
prs.save(out)
print("salvo", out)
