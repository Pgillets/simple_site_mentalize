/*
 * pagina-404.js — redirecionamento de 404.html. Extraído do <script> inline
 * para permitir a mesma CSP restritiva ('self', sem unsafe-inline) usada nas
 * demais páginas do site.
 *
 * Caminhos internos da aplicação começam com o fragmento "#" e nunca chegam
 * até aqui — este script só trata caminhos realmente inexistentes.
 *
 * O site é servido na raiz de mentalizejoias.com.br, então o destino é sempre
 * "/". Antes havia aqui uma detecção do subcaminho /simple_site_mentalize/,
 * necessária enquanto o endereço era o project page do GitHub Pages; com o
 * domínio próprio ela deixou de ter função.
 */
(function () {
  var destino = "/";
  document.getElementById("caminho").textContent = location.pathname;
  document.getElementById("link-inicio").setAttribute("href", destino);
  setTimeout(function () {
    location.replace(destino);
  }, 1200);
})();
