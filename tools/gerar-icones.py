#!/usr/bin/env python3
"""
gerar-icones.py — gera o favicon e os ícones do PWA a partir do "n" cursivo do
wordmark "mentalize".

O "n" é a letra manuscrita do logotipo, desenhada na fonte Best Stories. Em vez
de escrever a letra como <text> (num favicon nenhuma webfont carrega, então o
navegador cairia numa fonte genérica), o contorno do glifo é extraído da fonte e
embutido como PATH VETORIAL. O resultado não depende de fonte nenhuma.

O glifo tem um único contorno e nenhum furo, então o preenchimento é um polígono
simples: as 21 cúbicas são achatadas e desenhadas com o Pillow, em 4x, com
redução final para suavizar. Determinístico, sem navegador no caminho.

Uso:
    pip install fonttools brotli pillow
    python3 tools/gerar-icones.py

Escreve: assets/favicon.svg, assets/icones/icone-256.png,
         assets/icones/icone-512.png, assets/icones/icone-maskable-512.png
"""

import pathlib

from PIL import Image, ImageDraw
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont

RAIZ = pathlib.Path(__file__).resolve().parent.parent
FONTE = RAIZ / "assets/fontes/best-stories.woff2"

FUNDO = "#9f3e2e"   # terracota da marca
TINTA = "#fefdf2"   # creme da marca

# Largura da marca como fração do lado do ícone.
#   - FRACAO: ícones comuns e favicon.
#   - FRACAO_MASCARA: ícone maskable. O Android pode recortar o ícone em
#     qualquer forma dentro de um círculo de 80% do lado, então a marca precisa
#     caber nesse círculo. Para este glifo (proporção ~2,32:1) o limite é 73,5%;
#     62% deixa folga confortável.
FRACAO = 0.781
FRACAO_MASCARA = 0.62

SUPERAMOSTRAGEM = 4


def contorno_do_n():
    """Devolve (pontos, caixa) do glifo "n" em unidades da fonte, y para cima."""
    fonte = TTFont(FONTE)
    glifos = fonte.getGlyphSet()
    nome = fonte.getBestCmap()[ord("n")]

    gravacao = RecordingPen()
    glifos[nome].draw(gravacao)

    pontos = []
    atual = None

    def cubica(p0, p1, p2, p3, passos=48):
        for i in range(1, passos + 1):
            t = i / passos
            u = 1 - t
            yield (
                u * u * u * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t * t * t * p3[0],
                u * u * u * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t * t * t * p3[1],
            )

    for operacao, argumentos in gravacao.value:
        if operacao == "moveTo":
            atual = argumentos[0]
            pontos.append(atual)
        elif operacao == "lineTo":
            atual = argumentos[0]
            pontos.append(atual)
        elif operacao == "curveTo":
            c1, c2, fim = argumentos
            pontos.extend(cubica(atual, c1, c2, fim))
            atual = fim
        elif operacao == "qCurveTo":
            raise SystemExit("glifo com curva quadrática — este script espera cúbicas (CFF)")

    xs = [p[0] for p in pontos]
    ys = [p[1] for p in pontos]
    return pontos, (min(xs), min(ys), max(xs), max(ys))


def escrever_favicon(caixa=64, raio=16):
    """SVG do favicon: quadrado arredondado + o path do glifo, sem fonte."""
    fonte = TTFont(FONTE)
    glifos = fonte.getGlyphSet()
    nome = fonte.getBestCmap()[ord("n")]

    caneta = SVGPathPen(glifos)
    glifos[nome].draw(caneta)
    d = caneta.getCommands()

    _, (xmin, ymin, xmax, ymax) = contorno_do_n()
    largura_glifo, altura_glifo = xmax - xmin, ymax - ymin

    largura = caixa * FRACAO
    escala = largura / largura_glifo
    x0 = (caixa - largura) / 2 - xmin * escala
    y0 = (caixa - altura_glifo * escala) / 2 + ymax * escala

    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {caixa} {caixa}" '
        f'role="img" aria-label="Mentalize">\n'
        f'  <rect width="{caixa}" height="{caixa}" rx="{raio}" fill="{FUNDO}"/>\n'
        f'  <path transform="translate({x0:.4f} {y0:.4f}) scale({escala:.6f} -{escala:.6f})" '
        f'fill="{TINTA}" d="{d}"/>\n'
        f"</svg>\n"
    )
    destino = RAIZ / "assets/favicon.svg"
    destino.write_text(svg, encoding="utf-8")
    return destino


def escrever_png(caminho, lado, fracao):
    """PNG de quadrado cheio (a convenção dos ícones atuais) com a marca ao centro."""
    pontos, (xmin, ymin, xmax, ymax) = contorno_do_n()
    largura_glifo, altura_glifo = xmax - xmin, ymax - ymin

    grande = lado * SUPERAMOSTRAGEM
    largura = grande * fracao
    escala = largura / largura_glifo
    altura = altura_glifo * escala
    x0 = (grande - largura) / 2
    y0 = (grande - altura) / 2

    # y da fonte cresce para cima; o da imagem, para baixo.
    poligono = [
        (x0 + (x - xmin) * escala, y0 + (ymax - y) * escala)
        for x, y in pontos
    ]

    imagem = Image.new("RGB", (grande, grande), FUNDO)
    ImageDraw.Draw(imagem).polygon(poligono, fill=TINTA)
    imagem = imagem.resize((lado, lado), Image.LANCZOS)

    caminho.parent.mkdir(parents=True, exist_ok=True)
    imagem.save(caminho, optimize=True)
    return caminho


def main():
    print(escrever_favicon().relative_to(RAIZ))
    for nome, lado, fracao in (
        ("icone-256.png", 256, FRACAO),
        ("icone-512.png", 512, FRACAO),
        ("icone-maskable-512.png", 512, FRACAO_MASCARA),
    ):
        print(escrever_png(RAIZ / "assets/icones" / nome, lado, fracao).relative_to(RAIZ))


if __name__ == "__main__":
    main()
