# simple_site_mentalize

Site institucional para **Mentalize Joias** — ateliê de joalheria autoral na
Vila Mariana, São Paulo. Publicado em **https://mentalizejoias.com.br** via
GitHub Pages.

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
- `CNAME` — domínio próprio lido pelo GitHub Pages (`mentalizejoias.com.br`)

## Rodar localmente

Os módulos ES exigem um servidor HTTP (não funcionam via `file://`):

```bash
python3 tools/servidor.py
```

Abra `http://localhost:8000/`. O site é servido na raiz do domínio, igual ao
local — o `--base` de `tools/servidor.py` existia para simular o subcaminho do
*project page* do GitHub Pages e não é mais necessário.

## Identidade visual

- **Cores e fontes:** `css/tokens.css` (paleta terracota/ameixa/oliva/creme;
  fontes **Avenir** e **Best Stories**).
- **Logotipo:** `assets/logo-preto.png` (fundo claro) e `assets/logo-branco.png`
  (fundo escuro) — as duas artes do manual da marca. O cabeçalho traz as duas no
  HTML e o CSS (`.marca-logo--claro` / `.marca-logo--escuro`, em
  `css/componentes.css`) mostra a que combina com o tema, sem filtro de inversão.
  O nome acessível fica no `aria-label` do link `.marca`, então as imagens são
  decorativas (`alt=""`).
- **Favicon e ícones do PWA:** o **"n" cursivo do wordmark**, creme sobre
  terracota. Gerados por `tools/gerar-icones.py` — ver abaixo.

### Ícones (favicon + PWA)

`assets/favicon.svg` e os três PNG de `assets/icones/` saem do mesmo desenho: o
`n` manuscrito de "me*n*talize", a letra que a Best Stories dá ao logotipo.

```bash
pip install fonttools brotli pillow
python3 tools/gerar-icones.py
```

Duas decisões que o script registra em comentário e vale repetir aqui:

- **O glifo é embutido como path vetorial**, extraído da fonte — não como
  `<text font-family="...">`. Num favicon nenhuma webfont carrega, então um
  `<text>` cairia numa fonte genérica do sistema. Era o que acontecia antes: o
  SVG pedia `Mulish` (fonte que o site nem usa mais) e o navegador desenhava a
  letra em Arial.
- **O `maskable` é menor de propósito** (62% da largura, contra 78% dos
  demais). O Android pode recortar o ícone em qualquer forma dentro de um
  círculo de 80% do lado; para a proporção deste glifo (~2,32:1) o limite é
  73,5%, e 62% deixa folga.

Os PNG são quadrados cheios, sem transparência e sem canto arredondado —
a mesma convenção dos ícones anteriores; só o `favicon.svg` arredonda. Ao
regerar, suba a `VERSAO` em `sw.js`: os quatro arquivos estão no `PRECACHE`.

### Capa de compartilhamento (og:image)

`assets/og-capa-negocio.png` (1200×630) é a imagem que aparece ao compartilhar
o site no WhatsApp, Instagram e Facebook. Gerada por:

```bash
python3 tools/gerar-capa-og.py
```

O script descomprime o `woff2` da Avenir para `ttf` em memória e desenha o texto
com `PIL.ImageFont` — mesma ideia do gerador de ícones: determinístico, sem
depender de um navegador resolver fonte. Era exatamente esse o defeito da versão
anterior, cujas duas linhas de texto saíram numa sans-serif genérica porque a
fonte da marca não carregou na hora de gerar.

A capa **não** entra no `PRECACHE` de `sw.js`: quem a consome são os crawlers das
redes sociais, não o site.

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

### Fonte Best Stories (manuscrita)

A segunda fonte do manual é a **Best Stories** — a manuscrita de onde vem o
`n` cursivo do wordmark "mentalize". Também auto-hospedada, em
`assets/fontes/best-stories.woff2`, com `@font-face` em `css/tokens.css`.

Ela **não** entra em `--fonte`. Fica no token `--fonte-manuscrita`, aplicado
ponto a ponto pela classe `.manuscrita` (`css/componentes.css`). Hoje o único
uso é o trecho final do H1 da Home:

```html
<h1>Sua joia começa nas <span class="manuscrita">suas próprias mãos</span></h1>
```

É a mesma lógica do wordmark, que mistura Avenir com uma letra da Best
Stories. Um `<span>`, não um `<em>`: muda a tipografia, não o significado.

Três coisas a respeitar ao usá-la:

- **Só acentos curtos** — uma palavra, uma assinatura, um heading. Em corpo de
  texto e em elementos pequenos (`.selo`, `.preco-mini`) fica ilegível.
- **Compensar o tamanho** — a altura-x dela é bem menor que a da Avenir, então
  no mesmo `font-size` parece encolhida. `1.4em`–`1.5em` equilibra.
- **Zerar a herança do título** — `font-weight: 400` (a fonte só existe em um
  peso; sem isso o navegador sintetiza negrito falso dentro de um `h1`) e
  `letter-spacing: normal` (o `h1` usa `-0.02em`, que cola as ligaduras).

A classe `.manuscrita` já faz as três coisas — reaproveite-a em vez de
redeclarar o token.

> **Licenciamento:** os arquivos da Avenir vieram como `.ttf` e o da Best
> Stories como `.otf` — formatos que normalmente correspondem a licença
> **desktop**. Auto-hospedar como webfont deixa o arquivo publicamente
> baixável e costuma exigir uma licença **web** separada. Vale confirmar com o
> fornecedor. **Decidido manter assim** — fica registrado aqui porque a
> exposição é da cliente, não porque haja ação pendente. A Best Stories
> (Rantau Studio) ao menos declara `fsType = 0` no `OS/2`, ou seja,
> incorporação instalável sem restrição — sinal favorável, mas que não
> substitui a licença.

## Publicar (GitHub Pages + domínio próprio)

O site é servido em **https://mentalizejoias.com.br** (domínio registrado na
GoDaddy, DNS na própria GoDaddy — nameservers `ns13/ns14.domaincontrol.com`).

1. Nas configurações do repositório: **Settings → Pages → Deploy from a branch →
   `main` → `/ (root)`**.
2. O repositório precisa ser **público** (plano gratuito do Pages).
3. Em **Settings → Pages → Custom domain**, informe `mentalizejoias.com.br`.
   O arquivo `CNAME` na raiz já contém esse valor — é ele que o Pages lê, então
   não apague nem renomeie.
4. Espere o certificado ser emitido e marque **Enforce HTTPS**.
5. Faça o merge da branch de trabalho em `main`; o Pages publica automaticamente.

### DNS na GoDaddy

Painel: **Meus produtos → Domínios → mentalizejoias.com.br → DNS**.

Trocar o apontamento do apex e do `www`:

| Ação | Tipo | Nome | Valor | TTL |
|---|---|---|---|---|
| **remover** | A | `@` | `13.248.243.5` (estacionamento GoDaddy) | — |
| **remover** | A | `@` | `76.223.105.230` (estacionamento GoDaddy) | — |
| criar | A | `@` | `185.199.108.153` | 600 |
| criar | A | `@` | `185.199.109.153` | 600 |
| criar | A | `@` | `185.199.110.153` | 600 |
| criar | A | `@` | `185.199.111.153` | 600 |
| criar | AAAA | `@` | `2606:50c0:8000::153` | 600 |
| criar | AAAA | `@` | `2606:50c0:8001::153` | 600 |
| criar | AAAA | `@` | `2606:50c0:8002::153` | 600 |
| criar | AAAA | `@` | `2606:50c0:8003::153` | 600 |
| **alterar** | CNAME | `www` | de `mentalizejoias.com.br` para `pgillets.github.io` | 600 |

Os quatro IPv4 e os quatro IPv6 são os endereços fixos do GitHub Pages para
domínio apex. O `www` como CNAME faz o Pages redirecionar `www` → apex sozinho,
com 301 — não é preciso configurar redirecionamento na GoDaddy.

**Não mexer** no registro `TXT` de `_dmarc` (é de e-mail, criado por padrão pela
GoDaddy) nem nos nameservers. O domínio hoje **não tem registro MX**, ou seja,
não há e-mail configurado nele — então essa troca de DNS não derruba nenhuma
caixa de e-mail.

⚠️ **Desligar o redirecionamento de domínio** em **Domain Settings → Forwarding**
antes de salvar o DNS. Os dois A de estacionamento vêm do *forwarding* da
GoDaddy; se ele continuar ativo, a GoDaddy recria esses registros e sobrescreve
os do GitHub.

Depois de propagar (normalmente minutos, até algumas horas), confira:

```bash
# deve devolver os quatro 185.199.x.153
python3 -c "import socket; print(sorted({i[4][0] for i in socket.getaddrinfo('mentalizejoias.com.br', 443)}))"
```

### Ao publicar mudanças

Suba a constante `VERSAO` em `sw.js` sempre que mudar um arquivo do `PRECACHE`,
para o service worker invalidar o cache antigo.

> O código-fonte continua público: o plano gratuito do GitHub Pages exige
> repositório público. O rodapé do site não linka mais para o repositório, mas
> isso só deixa de divulgá-lo — não o torna privado.

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
um anel de noivado) fica com preço **"Sob consulta"** — decidido, não é
pendência. Aparece em dois lugares na página: no card "Para viver um momento
especial" e na seção `#noivado`.

## Pendências de conteúdo

- **Página "Aula Experimental"** — a cliente pediu uma página nova para essa
  experiência ("PÁGINA NOVA AULA EXPERIMENTAL — BOTÃO: AULA DUPLA E WS AA"),
  mas o conteúdo ainda não veio. Nessa anotação, **WS = Workshop**; o que "AA"
  significa segue em aberto. Enquanto isso, o card "Experimente fazer sua
  primeira joia" na Home aponta para `presente.html#workshop-coletivo`, que
  descreve o mesmo workshop. Quando o conteúdo chegar: criar a página, incluir
  no `PAGINAS` de `js/componentes/cabecalho-site.js` e de `sw.js`, no
  `sitemap.xml`, e trocar o `href` do card.
- Fotos reais para a galeria, o hero, as alianças, a equipe e as demais
  páginas (hoje há 29 placeholders "em breve").
- Depoimentos/avaliações reais (ver seção "Avaliações do Google" acima).
- **Container do Google Tag Manager** — `GTM_CONTAINER_ID` em
  `js/consentimento.js` segue no valor de exemplo (ver seção "Analytics" acima).

Decisões já fechadas, que **não** são pendência: o preço da Aula Dupla fica
"Sob consulta", e a licença da Avenir fica como está (ver as duas seções
adiante).

## Preços: onde cada número aparece

O curso regular custa **R$ 337** (pacote de 2 a 4 aulas) e há **10% OFF
comprando em dupla**, o que dá R$ 303. Para não parecer contradição:

- A **Home** anuncia "a partir de R$ 303 **em dupla**" (o menor valor possível,
  com a condição explícita).
- A página **Cursos** mostra R$ 337 como valor cheio, com o banner do desconto
  logo acima dos planos.

Ao mexer em um, confira o outro.
