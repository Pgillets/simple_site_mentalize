# simple_site_mentalize

Site institucional para **Mentalize Joias** — ateliê de joalheria autoral na
Vila Mariana, São Paulo. Hospedado via GitHub Pages.

Construído a partir do template [`simple_single_page_app`](https://github.com/pgillets/simple_single_page_app):
HTML/CSS/JS estático, **sem etapa de build** — `git push` é o deploy inteiro.

## Páginas

- `index.html` — início (hero + resumo das ofertas)
- `cursos.html` — cursos, alianças, empresas, gift card e FAQ (com os valores)
- `sobre.html` — o ateliê e as fundadoras
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

- **Cores e fontes:** `css/tokens.css` (paleta terracota/ameixa/oliva/creme; fonte Mulish).
- **Logotipo:** `assets/logo-preto.png` (fundo claro) e `assets/logo-branco.png` (fundo escuro). O wordmark é usado como imagem no cabeçalho; no tema escuro, a arte preta é invertida via CSS.

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

## Pendências de conteúdo

- Fotos reais para a galeria, o hero e as alianças (hoje há placeholders "em breve").
- Depoimentos reais de alunos/casais (a seção em `sobre.html` está aguardando).
