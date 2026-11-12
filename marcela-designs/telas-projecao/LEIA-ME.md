# Kit de telas de projeção · CAISA DAY 2026

**Formato:** 16:9, 1920 × 1080 px. **Confirme a proporção do telão do local antes do evento.**
**Paleta:** identidade Marcela (verde-musgo, verde-claro, off-white), com textura de papel e fundo escuro, pensado para um salão com pouca luz.

## Arquivos em `saida/`
| Arquivo | Para quê |
|---|---|
| `png/CAISA-DAY-2026_tela-01_recepcao.png` … `tela-10_agradecimento.png` | Uma imagem por tela, numerada na ordem do roteiro. É o mais seguro para a cerimonialista. |
| `CAISA-DAY-2026_telas-de-projecao_10-telas.pdf` | As 10 telas em sequência, para conferência ou projeção em PDF. |
| `CAISA-DAY-2026_telas-de-projecao_EDITAVEL.pptx` | Apresentação contínua e editável, com os textos em caixas, sem transições e sem animações. |
| `fontes/` | Instrument Serif e Poppins. **Instale-as no computador que vai editar ou projetar o PPTX.** |

## Telas que precisam de ajuste antes do evento
- **03 · Convidada:** colocar a foto real no retângulo e o nome e o título da fala. Duplique a tela para cada convidada.
- **05 · Reflexão com Marcela:** o título "Da consciência ao movimento" é provisório.
- **07 · Dinâmica final:** a frase pode mudar conforme o roteiro definitivo. Não usar em divulgação.
- **08 · Momento do pin:** substituir o texto entre colchetes pelo texto aprovado pela organizadora.

## Para editar a fonte do design
Altere `telas.html` e rode:
`node marcela-designs/telas-projecao/render.js && python3 marcela-designs/telas-projecao/gerar_pptx.py`
