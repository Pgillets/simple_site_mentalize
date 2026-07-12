/*
 * pagina-404.js — redirecionamento de 404.html. Extraído do <script> inline
 * para permitir a mesma CSP restritiva ('self', sem unsafe-inline) usada nas
 * demais páginas do site.
 *
 * Caminhos internos da aplicação começam com o fragmento "#" e nunca chegam
 * até aqui — este script só trata caminhos realmente inexistentes. Detecção
 * pelo CAMINHO (não pelo hostname): funciona igual em localhost, no project
 * page e no domínio próprio, sem edição.
 */
(function () {
  var repositorio = "simple_site_mentalize";
  var segmentos = location.pathname.split("/").filter(Boolean);
  var naRaizDoProjeto = segmentos[0] === repositorio;
  var destino = naRaizDoProjeto ? "/" + repositorio + "/" : "/";
  document.getElementById("caminho").textContent = location.pathname;
  document.getElementById("link-inicio").setAttribute("href", destino);
  setTimeout(function () {
    location.replace(destino);
  }, 1200);
})();
