/*
 * consentimento.js — faixa de cookies + carregamento do Google Tag Manager.
 *
 * Nada de rastreador de terceiro (GTM e, dentro dele, Pixel da Meta/GA4/Ads
 * quando configurados) executa antes do visitante aceitar. Sem Consent Mode
 * do Google (gtag('consent', ...)) de propósito: aqui a régua é simples —
 * zero código de terceiro roda antes do clique em "Aceitar". Mesmo padrão de
 * localStorage com try/catch de js/tema.js (chave própria, falha graciosa se
 * localStorage estiver indisponível).
 *
 * O <noscript><iframe> oficial do GTM foi omitido de propósito: ele dispara
 * sem qualquer possibilidade de checar consentimento (não há JS pra isso),
 * o que contradiz o gate — cobre um público residual (JS desligado) que não
 * compensa o risco de rastrear sem consentimento.
 */

// EDITE AQUI quando tiver o container do Google Tag Manager (formato GTM-XXXXXXX).
const GTM_CONTAINER_ID = "GTM-XXXXXXX";

const CHAVE = "consentimento-cookies";

function escolhaSalva() {
  try {
    return localStorage.getItem(CHAVE);
  } catch {
    return null;
  }
}

function salvarEscolha(valor) {
  try {
    localStorage.setItem(CHAVE, valor);
  } catch {
    /* sem persistência, a escolha vale só até o próximo carregamento */
  }
}

/** Injeta o loader do GTM (script próprio, mesma origem; só o destino do
 * carregamento dinâmico é cross-origin — é essa URL que a CSP libera). */
function carregarGTM() {
  if (document.getElementById("gtm-loader")) return; // não injeta duas vezes
  window.dataLayer = window.dataLayer || [];
  window.dataLayer.push({ "gtm.start": Date.now(), event: "gtm.js" });
  const script = document.createElement("script");
  script.id = "gtm-loader";
  script.async = true;
  script.src = `https://www.googletagmanager.com/gtm.js?id=${GTM_CONTAINER_ID}`;
  document.head.appendChild(script);
}

function criarFaixa() {
  const faixa = document.createElement("div");
  faixa.className = "faixa-cookies";
  faixa.id = "faixa-cookies";
  faixa.setAttribute("role", "region");
  faixa.setAttribute("aria-label", "Aviso de cookies");

  const texto = document.createElement("p");
  texto.textContent =
    "Usamos cookies para entender como você usa o site e mostrar anúncios mais relevantes. " +
    "Veja nossa política de privacidade.";

  const link = document.createElement("a");
  link.href = "./privacidade.html";
  link.textContent = "Política de Privacidade";
  texto.append(" ", link);

  const botoes = document.createElement("div");
  botoes.className = "grupo-botoes";

  const rejeitar = document.createElement("button");
  rejeitar.type = "button";
  rejeitar.className = "botao";
  rejeitar.textContent = "Rejeitar";
  rejeitar.addEventListener("click", () => responder("rejeitado"));

  const aceitar = document.createElement("button");
  aceitar.type = "button";
  aceitar.className = "botao botao-primario";
  aceitar.textContent = "Aceitar";
  aceitar.addEventListener("click", () => responder("aceito"));

  botoes.append(rejeitar, aceitar);
  faixa.append(texto, botoes);
  document.body.append(faixa);

  function responder(valor) {
    salvarEscolha(valor);
    faixa.remove();
    if (valor === "aceito") carregarGTM();
  }
}

function reabrirFaixa() {
  if (document.getElementById("faixa-cookies")) return;
  criarFaixa();
}

export function iniciarConsentimento() {
  const escolha = escolhaSalva();
  if (escolha === "aceito") {
    carregarGTM();
  } else if (escolha !== "rejeitado") {
    criarFaixa();
  }

  // Link "Gerenciar cookies" no rodapé de cada página reabre a faixa.
  document.querySelectorAll(".gerenciar-cookies").forEach((botao) => {
    botao.addEventListener("click", (evento) => {
      evento.preventDefault();
      reabrirFaixa();
    });
  });
}
