/*
 * site.js — ponto de entrada compartilhado pelas páginas de conteúdo do site
 * institucional (todas exceto 404.html, que não carrega este arquivo).
 *
 * Nenhum roteador, nenhuma vista: cada página já é HTML estático de verdade.
 * Este arquivo só liga melhorias progressivas por cima: cabeçalho/navegação
 * compartilhados, tema, funcionamento offline e o gate de consentimento de
 * cookies (que só carrega o Google Tag Manager depois do aceite — ver
 * consentimento.js).
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
import { iniciarConsentimento } from "./consentimento.js";

iniciarTema(document.getElementById("alternar-tema"));
registrarServiceWorker();
iniciarConsentimento();
