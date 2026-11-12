"""Gera a textura de fundo das telas (1920 × 1080)."""
import numpy as np
from PIL import Image, ImageFilter, ImageDraw
from pathlib import Path

W, H = 1920, 1080  # tela 16:9
OUT = Path(__file__).parent / "fundo"
OUT.mkdir(exist_ok=True)


def hex2rgb(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], dtype=np.float32)


def campo(seed, escala):
    """Ruído suave: ruído branco reduzido e ampliado, depois desfocado."""
    rng = np.random.default_rng(seed)
    w, h = max(2, W // escala), max(2, H // escala)
    img = Image.fromarray((rng.random((h, w)) * 255).astype(np.uint8))
    img = img.resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(escala / 2))
    a = np.asarray(img, dtype=np.float32) / 255.0
    return (a - a.mean()) / (a.std() + 1e-6)


def fibras(seed, n, cor):
    rng = np.random.default_rng(seed)
    img = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(img)
    for _ in range(n):
        x, y = rng.uniform(0, W), rng.uniform(0, H)
        ang = rng.uniform(0, np.pi)
        comp = rng.uniform(10, 45)
        pts = []
        for t in np.linspace(0, 1, 6):
            dx = np.cos(ang) * comp * t + rng.normal(0, 1.2)
            dy = np.sin(ang) * comp * t + rng.normal(0, 1.2)
            pts.append((x + dx, y + dy))
        d.line(pts, fill=int(rng.uniform(90, 200)), width=1)
    a = np.asarray(img.filter(ImageFilter.GaussianBlur(0.6)), dtype=np.float32) / 255.0
    return a


def papel(base, seed, grao, manchas, n_fibras, fibra_amp, nome):
    rng = np.random.default_rng(seed)
    b = hex2rgb(base)
    fino = rng.normal(0, 1, (H, W)).astype(np.float32)
    fino = np.asarray(Image.fromarray(((fino * 40) + 128).clip(0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.5)), dtype=np.float32)
    fino = (fino - fino.mean()) / (fino.std() + 1e-6)
    lum = grao * fino + manchas * (0.6 * campo(seed + 1, 60) + 0.4 * campo(seed + 2, 14))
    lum += fibra_amp * fibras(seed + 3, n_fibras, 1)
    rgb = b[None, None, :] * (1 + lum[..., None])
    Image.fromarray(rgb.clip(0, 255).astype(np.uint8)).save(OUT / nome, dpi=(300, 300))


papel("#374325", 21, grao=0.03, manchas=0.03, n_fibras=1100, fibra_amp=0.08, nome="textura.png")
from PIL import Image as _I
_I.open(OUT/"textura.png").save(OUT/"textura.jpg", quality=92, subsampling=0)
(OUT/"textura.png").unlink()
print("ok")
