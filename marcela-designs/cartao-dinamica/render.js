// Gera os arquivos de impressão do cartão da dinâmica final.
// Uso: node marcela-designs/cartao-dinamica/render.js
const { chromium } = require('playwright');
const path = require('path');

const src = 'file://' + path.join(__dirname, 'cartao.html');
const out = (f) => path.join(__dirname, 'saida', f);

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();

  const pdf = async (query, file) => {
    await page.goto(src + query);
    await page.evaluate(() => document.fonts.ready);
    await page.pdf({ path: out(file), width: '106mm', height: '156mm', printBackground: true, preferCSSPageSize: true });
  };
  // Arquivos finais para a gráfica (com sangria, sem guias)
  await pdf('?lado=frente', 'CAISA-DAY-2026_cartao-dinamica_FRENTE_100x150_sangria3mm.pdf');
  await pdf('?lado=verso', 'CAISA-DAY-2026_cartao-dinamica_VERSO_100x150_sangria3mm.pdf');
  await pdf('', 'CAISA-DAY-2026_cartao-dinamica_FRENTE-E-VERSO.pdf');
  // Prova com guias de corte (vermelho) e de segurança (azul)
  await pdf('?guias=1', 'PROVA_com-guias_cartao-dinamica.pdf');

  // PNG 300 dpi de cada lado (106 mm ≈ 1252 px a 300 dpi)
  const pxPerMm = 300 / 25.4;
  const cssPxPerMm = 96 / 25.4;
  await page.setViewportSize({ width: Math.round(106 * cssPxPerMm), height: Math.round(156 * cssPxPerMm) });
  for (const lado of ['frente', 'verso']) {
    const p2 = await browser.newPage({ deviceScaleFactor: pxPerMm / cssPxPerMm, viewport: { width: Math.round(106 * cssPxPerMm), height: Math.round(156 * cssPxPerMm) } });
    await p2.goto(src + '?lado=' + lado);
    await p2.evaluate(() => document.fonts.ready);
    await p2.locator('#' + lado).screenshot({ path: out(`CAISA-DAY-2026_cartao-dinamica_${lado.toUpperCase()}_300dpi.png`) });
    await p2.close();
  }
  await browser.close();
})();
