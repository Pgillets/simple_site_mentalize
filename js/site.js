/*
 * site.js — ponto de entrada compartilhado pelas 5 páginas do site
 * institucional (index.html, cursos.html, sobre.html, galeria.html,
 * contato.html).
 *
 * Nenhum roteador, nenhuma vista: cada página já é HTML estático de verdade.
 * Este arquivo só liga melhorias progressivas por cima: cabeçalho/navegação
 * compartilhados, tema e funcionamento offline.
 *
 * Import do cabeçalho ANTES de iniciarTema(): customElements.define() faz o
 * upgrade de elementos já presentes no documento de forma síncrona, então o
 * botão #alternar-tema (que <cabecalho-site> cria) já existe no light DOM
 * no momento em que iniciarTema() faz o getElementById — nenhuma mudança
 * necessária em tema.js.
 */

import "./componentes/cabecalho-site.js";

import { iniciarTema } from "./tema.js";
import { registrarServiceWorker } from "./sw-registro.js";

iniciarTema(document.getElementById("alternar-tema"));
registrarServiceWorker();
