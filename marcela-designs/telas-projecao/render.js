// Gera PNGs numerados, PDF contínuo e os dados para o PPTX editável.
// Uso: node marcela-designs/telas-projecao/render.js && python3 marcela-designs/telas-projecao/gerar_pptx.py
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const src = 'file://' + path.join(__dirname, 'telas.html');
const out = (...f) => path.join(__dirname, 'saida', ...f);

(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await p.goto(src);
  await p.evaluate(() => document.fonts.ready);
  const telas = await p.evaluate(() => window.TELAS);
  const dados = [];
  fs.mkdirSync(out('png'), { recursive: true });
  fs.mkdirSync(path.join(__dirname, 'fundo', 'pptx'), { recursive: true });
  for (const t of telas) {
    const nome = `${String(t.n).padStart(2, '0')}_${t.nome}`;
    await p.goto(src + '?n=' + t.n);
    await p.evaluate(() => document.fonts.ready);
    await p.screenshot({ path: out('png', `CAISA-DAY-2026_tela-${nome}.png`) });
    // textos editáveis: posição, tamanho e estilos por trecho
    const textos = await p.evaluate(() => [...document.querySelectorAll('.t')].map(el => {
      const r = el.getBoundingClientRect(), cs = getComputedStyle(el);
      const runs = [];
      const walk = (node, inh) => node.childNodes.forEach(c => {
        if (c.nodeType === 3) { if (c.textContent.trim() || c.textContent === ' ') runs.push({ ...inh, txt: c.textContent.replace(/\s+/g, ' ') }); }
        else if (c.tagName === 'BR') runs.push({ ...inh, txt: '\n' });
        else { const s = getComputedStyle(c); walk(c, { ...inh, italic: s.fontStyle === 'italic', color: s.color }); }
      });
      walk(el, { italic: cs.fontStyle === 'italic', color: cs.color });
      return { x: r.x, y: r.y, w: r.width, h: r.height, size: parseFloat(cs.fontSize), lh: parseFloat(cs.lineHeight) || null,
        font: cs.fontFamily.includes('Pop') ? 'Poppins' : 'Instrument Serif', upper: cs.textTransform === 'uppercase',
        spacing: parseFloat(cs.letterSpacing) || 0, align: cs.textAlign, runs };
    }));
    const foto = await p.evaluate(() => { const f = document.querySelector('.foto'); if (!f) return null; const r = f.getBoundingClientRect(); return { x: r.x, y: r.y, w: r.width, h: r.height }; });
    await p.goto(src + '?semtexto=1&n=' + t.n);
    await p.evaluate(() => document.fonts.ready);
    const fundo = path.join(__dirname, 'fundo', 'pptx', `${nome}.jpg`);
    await p.screenshot({ path: fundo, type: 'jpeg', quality: 92 });
    dados.push({ ...t, arquivo: nome, fundo, textos, foto });
  }
  fs.writeFileSync(path.join(__dirname, 'fundo', 'pptx', 'dados.json'), JSON.stringify(dados, null, 1));
  await p.goto(src);
  await p.evaluate(() => document.fonts.ready);
  await p.pdf({ path: out('CAISA-DAY-2026_telas-de-projecao_10-telas.pdf'), width: '1920px', height: '1080px', printBackground: true });
  await b.close();
})();
