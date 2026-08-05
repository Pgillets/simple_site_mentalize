/*
 * <cabecalho-site> — cabeçalho e navegação compartilhados entre as páginas.
 *
 * Light DOM (sem shadow root) de propósito: js/tema.js localiza o botão de
 * tema com document.getElementById("alternar-tema"); um shadow root tornaria
 * esse botão invisível para essa busca. Em light DOM, o CSS global já
 * existente (.topo-conteudo, .marca, .marca-logo, .topo nav — css/componentes.css)
 * estiliza este componente de graça, sem duplicar nada aqui dentro.
 *
 * O único lugar a editar para adicionar, renomear ou remover uma página do
 * site é o array PAGINAS abaixo.
 *
 * A marca ("mentalize" com o "n" manuscrito) já vem como markup estático
 * dentro de <cabecalho-site> em cada página (<a class="marca"><img
 * class="marca-logo" ...></a>) — assim ela existe no HTML servido, visível
 * a crawlers que não executam JavaScript. Este componente só a reaproveita;
 * se por algum motivo ela não estiver presente, cria como fallback. No tema
 * escuro a arte preta é invertida para branca via CSS (.marca-logo).
 *
 * Uso (em cada página):
 *   <header class="topo">
 *     <cabecalho-site class="topo-conteudo" data-pagina="sobre"
 *                     nome-negocio="Mentalize Joias">
 *       <a class="marca" href="./index.html">
 *         <img class="marca-logo" src="./assets/logo-preto.png" alt="Mentalize Joias" width="128" height="24">
 *       </a>
 *     </cabecalho-site>
 *     <noscript>...link de navegação em texto puro...</noscript>
 *   </header>
 */

const PAGINAS = [
  { pagina: "inicio", href: "./index.html", rotulo: "Início" },
  { pagina: "cursos", href: "./cursos.html", rotulo: "Cursos" },
  { pagina: "aliancas", href: "./aliancas.html", rotulo: "Alianças" },
  { pagina: "empresas", href: "./empresas.html", rotulo: "Empresas" },
  { pagina: "presente", href: "./presente.html", rotulo: "Presente" },
  { pagina: "sobre", href: "./sobre.html", rotulo: "Sobre" },
  { pagina: "galeria", href: "./galeria.html", rotulo: "Galeria" },
  { pagina: "contato", href: "./contato.html", rotulo: "Contato" },
];

class CabecalhoSite extends HTMLElement {
  // Sem observedAttributes: "data-pagina" e "nome-negocio" são lidos uma
  // única vez, em connectedCallback. Não há navegação client-side neste
  // template — cada página é um carregamento de documento novo — então
  // nada aqui precisa reagir a mudanças de atributo depois de montado.
  connectedCallback() {
    if (this.dataset.montado) return;
    this.dataset.montado = "true";

    const nomeDoNegocio = this.getAttribute("nome-negocio") ?? "";
    const paginaAtual = this.getAttribute("data-pagina") ?? "";

    // A marca normalmente já vem como markup estático (ver comentário acima).
    // Fallback: cria caso a página não a inclua.
    if (!this.querySelector(".marca")) {
      const marca = document.createElement("a");
      marca.className = "marca";
      marca.href = "./index.html";
      const logo = document.createElement("img");
      logo.className = "marca-logo";
      logo.src = "./assets/logo-preto.png";
      logo.alt = nomeDoNegocio;
      logo.width = 128;
      logo.height = 24;
      marca.append(logo);
      this.append(marca);
    }

    const nav = document.createElement("nav");
    nav.setAttribute("aria-label", "Navegação principal");
    for (const item of PAGINAS) {
      const link = document.createElement("a");
      link.href = item.href;
      link.textContent = item.rotulo;
      if (item.pagina && item.pagina === paginaAtual) {
        link.setAttribute("aria-current", "page");
      }
      nav.append(link);
    }

    const botaoTema = document.createElement("button");
    botaoTema.type = "button";
    botaoTema.id = "alternar-tema";
    botaoTema.setAttribute("aria-label", "Alternar tema");

    this.append(nav, botaoTema);
  }
}

customElements.define("cabecalho-site", CabecalhoSite);
