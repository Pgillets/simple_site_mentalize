#!/usr/bin/env python3
"""
gerar-capa-og.py — gera assets/og-capa-negocio.png, a imagem que aparece quando
o site é compartilhado (WhatsApp, Instagram, Facebook, Twitter).

Por que existe: a capa anterior tinha o wordmark certo, mas as duas linhas de
texto saíram numa sans-serif genérica — a fonte da marca não carregava no
momento em que ela foi gerada. Agora que a Avenir é auto-hospedada no
repositório, o texto é desenhado com ela.

Como: o woff2 do repositório é descomprimido para ttf em memória com fontTools e
desenhado com PIL.ImageFont. Determinístico, sem depender de um navegador
resolver fonte — o mesmo princípio de tools/gerar-icones.py.

A geometria reproduz a capa anterior (posições verticais e a largura do
wordmark), com uma correção: o wordmark agora é centralizado pela TINTA, não
pela caixa do PNG. O arquivo do logotipo tem margens assimétricas (51px à
esquerda, 80px à direita), então centralizar a caixa deixava a palavra ~10px à
esquerda do centro.

Uso:
    pip install fonttools brotli pillow
    python3 tools/gerar-capa-og.py
"""

import io
import pathlib

from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont

RAIZ = pathlib.Path(__file__).resolve().parent.parent

LARGURA, ALTURA = 1200, 630          # proporção exigida por og:image
CREME = "#fefdf2"
TERRACOTA = "#9f3e2e"
OLIVA = "#666646"

LOGO = RAIZ / "assets/logo-preto.png"
FONTE_TITULO = RAIZ / "assets/fontes/avenir-heavy.woff2"

LARGURA_WORDMARK = 540               # largura da tinta do wordmark
TOPO_WORDMARK = 179

LINHAS = [
    # (texto, cor, topo da tinta, altura da tinta) — medidos da capa anterior,
    # para o resultado ficar na mesma escala e só a fonte mudar.
    ("Ateliê de joalheria autoral", TERRACOTA, 311, 29),
    ("Vila Mariana · São Paulo", OLIVA, 357, 18),
]


def carregar_fonte(caminho_woff2):
    """Descomprime o woff2 para ttf em memória e devolve os bytes."""
    fonte = TTFont(caminho_woff2)
    fonte.flavor = None
    buffer = io.BytesIO()
    fonte.save(buffer)
    return buffer.getvalue()


def caixa_da_tinta(imagem, fundo, tolerancia=18):
    """Bounding box do que difere do fundo. Usado para medir e para centralizar."""
    px = imagem.convert("RGB").load()
    largura, altura = imagem.size
    xs, ys = [], []
    for y in range(altura):
        for x in range(largura):
            if any(abs(a - b) > tolerancia for a, b in zip(px[x, y], fundo)):
                xs.append(x)
                ys.append(y)
    if not xs:
        return None
    return min(xs), min(ys), max(xs), max(ys)


def tamanho_para_altura(bytes_fonte, texto, altura_alvo):
    """Acha, por busca binária, o tamanho em que a tinta do texto tem a altura pedida."""
    def altura_em(tamanho):
        fonte = ImageFont.truetype(io.BytesIO(bytes_fonte), tamanho)
        x0, y0, x1, y1 = fonte.getbbox(texto)
        return y1 - y0

    baixo, alto = 4, 200
    while alto - baixo > 1:
        meio = (baixo + alto) // 2
        if altura_em(meio) < altura_alvo:
            baixo = meio
        else:
            alto = meio
    # devolve o que fica mais perto do alvo
    return min((baixo, alto), key=lambda t: abs(altura_em(t) - altura_alvo))


def main():
    fundo_rgb = Image.new("RGB", (1, 1), CREME).getpixel((0, 0))
    capa = Image.new("RGB", (LARGURA, ALTURA), CREME)

    # --- wordmark, centralizado pela tinta ---
    logo = Image.open(LOGO).convert("RGBA")
    alfa = logo.getchannel("A")
    caixa = alfa.getbbox()                      # recorta as margens do PNG
    logo = logo.crop(caixa)
    escala = LARGURA_WORDMARK / logo.width
    logo = logo.resize(
        (LARGURA_WORDMARK, round(logo.height * escala)), Image.LANCZOS
    )
    capa.paste(logo, ((LARGURA - logo.width) // 2, TOPO_WORDMARK), logo)

    # --- as duas linhas de texto, em Avenir ---
    bytes_fonte = carregar_fonte(FONTE_TITULO)
    desenho = ImageDraw.Draw(capa)
    usados = []
    for texto, cor, topo, altura_tinta in LINHAS:
        tamanho = tamanho_para_altura(bytes_fonte, texto, altura_tinta)
        fonte = ImageFont.truetype(io.BytesIO(bytes_fonte), tamanho)
        x0, y0, x1, y1 = fonte.getbbox(texto)
        # getbbox devolve a caixa da tinta relativa à origem do desenho, então
        # descontar x0/y0 alinha a TINTA no ponto pedido, não a caixa da fonte.
        desenho.text(
            (round((LARGURA - (x1 - x0)) / 2 - x0), topo - y0),
            texto, font=fonte, fill=cor,
        )
        usados.append((texto, tamanho, x1 - x0, y1 - y0))

    destino = RAIZ / "assets/og-capa-negocio.png"
    capa.save(destino, optimize=True)

    print(destino.relative_to(RAIZ), f"{LARGURA}x{ALTURA}")
    print(f"  wordmark: {logo.width}x{logo.height} em y={TOPO_WORDMARK}")
    for texto, tamanho, largura, altura in usados:
        print(f'  "{texto}" — Avenir Heavy {tamanho}px, tinta {largura}x{altura}')
    print("  caixa total da tinta:", caixa_da_tinta(capa, fundo_rgb))


if __name__ == "__main__":
    main()
