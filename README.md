# simple_site_mentalize

Site institucional para **Mentalize Joias** — ateliê de joalheria autoral na
Vila Mariana, São Paulo. Hospedado via GitHub Pages.

Construído a partir do template [`simple_single_page_app`](https://github.com/pgillets/simple_single_page_app):
HTML/CSS/JS estático, **sem etapa de build** — `git push` é o deploy inteiro.

## Páginas

- `index.html` — início (hero + resumo das ofertas)
- `cursos.html` — curso regular de joalheria em cera (pacotes Experimentar/Desenvolver/Aprofundar)
- `aliancas.html` — alianças feitas à mão, para casais
- `empresas.html` — workshops corporativos
- `presente.html` — gift card / presentear uma experiência
- `sobre.html` — a história do ateliê e as fundadoras
- `galeria.html` — galeria (placeholders "em breve" até haver fotos reais)
- `contato.html` — endereço, WhatsApp e Instagram
- `privacidade.html` — política de privacidade (cookies, Google/Meta)
- `404.html` — página de erro com redirecionamento

## Rodar localmente

Os módulos ES exigem um servidor HTTP (não funcionam via `file://`):

```bash
python3 tools/servidor.py
```

Abra `http://localhost:8000/`. Para simular o prefixo do GitHub Pages:

```bash
python3 tools/servidor.py --base simple_site_mentalize
```

## Identidade visual

- **Cores e fontes:** `css/tokens.css` (paleta terracota/ameixa/oliva/creme; fonte **Avenir**).
- **Logotipo:** `assets/logo-preto.png` (fundo claro) e `assets/logo-branco.png` (fundo escuro). O wordmark é usado como imagem no cabeçalho; no tema escuro, a arte preta é invertida via CSS.

### Fonte Avenir (auto-hospedada)

A Avenir é a fonte da marca e fica **auto-hospedada** em `assets/fontes/`, em
`woff2` — sem Google Fonts. Por isso a CSP de todas as páginas usa
`style-src 'self'; font-src 'self'`, sem liberar domínio de terceiro.

Os `@font-face` estão no topo de `css/tokens.css`. Três arquivos cobrem a
escala que o CSS usa:

| Arquivo | `font-weight` declarado | Uso |
|---|---|---|
| `avenir-book.woff2` | `300 350` | disponível para texto de exibição mais leve |
| `avenir-regular.woff2` | `400 500` | corpo de texto |
| `avenir-heavy.woff2` | `600 900` | títulos, botões, preços |

O Heavy é declarado como faixa (`600 900`) de propósito: o CSS usa 600, 700 e
800, e assim os três resolvem para o mesmo arquivo real, sem o navegador
sintetizar negrito falso.

Para trocar ou acrescentar um peso: converta o `.ttf` com
`python3 -c "from fontTools.ttLib import TTFont; f=TTFont('X.ttf'); f.flavor='woff2'; f.save('assets/fontes/x.woff2')"`
(precisa de `pip install fonttools brotli`), adicione o `@font-face` e inclua o
arquivo no `PRECACHE` de `sw.js`, subindo a `VERSAO`.

> **Licenciamento:** os arquivos vieram como `.ttf`, que normalmente
> correspondem a licença **desktop**. Auto-hospedar como webfont deixa o
> arquivo publicamente baixável e costuma exigir uma licença **web** separada.
> Vale confirmar com o fornecedor da licença antes de manter isso em produção.

## Publicar (GitHub Pages)

1. Nas configurações do repositório: **Settings → Pages → Deploy from a branch → `main` → `/ (root)`**.
2. O repositório precisa ser **público** (plano gratuito do Pages).
3. Faça o merge da branch de trabalho em `main`; o Pages publica automaticamente.

Ao publicar mudanças em arquivos do PRECACHE, suba a constante `VERSAO` em
`sw.js` para o service worker invalidar o cache antigo.

## Analytics: Meta Pixel e Google Tag Manager

O site já vem preparado para rastreamento via **Google Tag Manager (GTM)**,
mas nada carrega até o visitante aceitar a faixa de cookies (`js/consentimento.js`) —
ver `privacidade.html` para o texto mostrado a ele.

Para ativar:

1. Crie uma conta no [Google Tag Manager](https://tagmanager.google.com/) e
   pegue o **Container ID** (formato `GTM-XXXXXXX`).
2. Cole esse ID na constante `GTM_CONTAINER_ID`, no topo de `js/consentimento.js`
   — é o único lugar do código que precisa ser editado.
3. **O Pixel da Meta, o Google Analytics (GA4), o Google Ads e qualquer outra
   tag são configurados depois, dentro do próprio painel do GTM** (Meta tem um
   template oficial de "Facebook Pixel" na galeria de templates do GTM) —
   não é necessário editar o site de novo para isso.
4. Publique o container no GTM.

Enquanto `GTM_CONTAINER_ID` estiver com o valor de exemplo (`GTM-XXXXXXX`), o
clique em "Aceitar" tenta carregar um container inexistente — falha em
silêncio, sem quebrar a página, só não envia dados de verdade.

A CSP de cada página já libera os domínios necessários do Google
(`googletagmanager.com`, `google-analytics.com`) e da Meta
(`connect.facebook.net`, `facebook.com`) para scripts, chamadas de rede e o
pixel de imagem de fallback.

## Banner promocional (10% OFF em dupla)

O banner "10% OFF em qualquer pacote comprando em dupla" está ativo em
`cursos.html` (classe `.faixa-promo`, definida em `css/negocio.css`). Para
desativar, basta remover o `<p class="faixa-promo">...</p>` da página — não
depende de nenhum outro arquivo.

## Avaliações do Google

Ainda não temos o link do perfil da Mentalize no Google Meu Negócio/Maps, então
os blocos "O que dizem os casais/as equipes/quem já presenteou"
(`aliancas.html`, `empresas.html`, `presente.html`) usam o mesmo placeholder
discreto "em breve" já usado para depoimentos. Quando o link existir, dá pra:

1. Trocar o placeholder por citações reais copiadas do perfil (mais simples,
   sem custo, sem mudança de CSP); ou
2. Embutir um widget ao vivo — normalmente exige uma API key do Google Places
   (com billing) ou um serviço de terceiro, e mudanças na CSP de cada página
   para liberar o domínio usado.

## Aula Dupla (anel de noivado)

Em `presente.html`, a experiência "Aula Dupla" (recomendada para quem vai criar
um anel de noivado) está com preço "Sob consulta" — o valor ainda não foi
definido.

## Pendências de conteúdo

- **Página "Aula Experimental"** — a cliente pediu uma página nova para essa
  experiência ("PÁGINA NOVA AULA EXPERIMENTAL"), mas o conteúdo ainda não veio.
  Enquanto isso, o card "Experimente fazer sua primeira joia" na Home aponta
  para `presente.html#workshop-coletivo`, que descreve o mesmo workshop.
  Quando o conteúdo chegar: criar a página, incluir no `PAGINAS` de
  `js/componentes/cabecalho-site.js` e de `sw.js`, no `sitemap.xml`, e trocar o
  `href` do card.
- Fotos reais para a galeria, o hero, as alianças, a equipe e as demais
  páginas (hoje há placeholders "em breve" em todas elas).
- Depoimentos/avaliações reais (ver seção "Avaliações do Google" acima).
- Preço da Aula Dupla (ver seção acima).
- Confirmar a licença **web** da Avenir (ver "Fonte Avenir" acima).

## Preços: onde cada número aparece

O curso regular custa **R$ 337** (pacote de 2 a 4 aulas) e há **10% OFF
comprando em dupla**, o que dá R$ 303. Para não parecer contradição:

- A **Home** anuncia "a partir de R$ 303 **em dupla**" (o menor valor possível,
  com a condição explícita).
- A página **Cursos** mostra R$ 337 como valor cheio, com o banner do desconto
  logo acima dos planos.

Ao mexer em um, confira o outro.
