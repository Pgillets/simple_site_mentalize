#!/usr/bin/env python3
"""
gerar-gtm.py — gera um contêiner do Google Tag Manager pronto para importar,
no padrão de nomenclatura da gestora de tráfego (referência: contêiner MACPSI).

Como funciona o rastreamento: cada link de WhatsApp do site carrega um
utm_content único (ex.: wa.me/...?utm_content=cursos_experimentar). O WhatsApp
ignora o parâmetro; o GTM lê a URL clicada e sabe exatamente qual botão gerou o
lead. Este script VARRE OS PRÓPRIOS HTML do site para descobrir os slugs, então
o contêiner gerado nunca dessincroniza do que está publicado.

O que o JSON contém, no padrão dela:
  - variável "Click - utm_content" (URL do clique → componente consulta)
  - constantes "GA4 - ID de métricas" (G-T8PV0H218F) e "Meta - Pixel ID"
    (1263186065151365) — para trocar um ID, é um lugar só
  - um acionador "[Lead] Botão WPP - ..." por slug (Apenas links,
    Click URL contém wa.me + Click - utm_content contém <slug>)
  - tag "00 - [GT] GA4" (Tag do Google, acionador Initialization)
  - tag "00 - [Meta] Pixel - Código base" (HTML: fbq init + PageView, sem o
    <noscript> — mesma razão do gate de consentimento do site)
  - tag "01 - [Meta] Lead - Botão WPP" (fbq Lead com o slug em content_name),
    disparada por TODOS os acionadores [Lead]
  - uma tag "02 - [GA4] Evento - ... - clickwpp_<slug>" por acionador

O que fica manual no painel (documentado no README):
  - tags 01 de conversão do Google Ads (dependem das conversões criadas no Ads)
  - publicar o contêiner

Uso:
    python3 tools/gerar-gtm.py            # escreve tools/gtm-mentalize.json
"""

import json
import pathlib
import re
import sys
from datetime import datetime, timezone

RAIZ = pathlib.Path(__file__).resolve().parent.parent
DESTINO = RAIZ / "tools/gtm-mentalize.json"

# Rótulo humano de cada slug, no formato "<Página> - <Seção>" da gestora.
ROTULOS = {
    "inicio_hero": "Home - Hero",
    "inicio_cta_final": "Home - CTA final",
    "aula_exp_duas_aulas": "Aula Experimental - Duas Aulas",
    "aula_exp_workshop": "Aula Experimental - Workshop",
    "aula_exp_cta_final": "Aula Experimental - CTA final",
    "cursos_experimentar": "Cursos - Pacote Experimentar",
    "cursos_desenvolver": "Cursos - Pacote Desenvolver",
    "cursos_aprofundar": "Cursos - Pacote Aprofundar",
    "cursos_fundicao": "Cursos - Seção Fundição",
    "cursos_cta_final": "Cursos - CTA final",
    "aliancas_ws_coletivo": "Alianças - Workshop coletivo",
    "aliancas_ws_privativo_cera": "Alianças - Workshop privativo cera",
    "aliancas_ws_privativo_metal": "Alianças - Workshop privativo metal",
    "aliancas_cta_final": "Alianças - CTA final",
    "empresas_cta_final": "Empresas - CTA final",
    "presente_ws_coletivo": "Presente - Workshop coletivo",
    "presente_hobby": "Presente - Novo hobby",
    "presente_privativo": "Presente - Workshop privativo",
    "presente_noivado": "Presente - Anel de noivado",
    "presente_cta_final": "Presente - CTA final",
    "sobre_cta_final": "Sobre - CTA final",
    "galeria_cta_final": "Galeria - CTA final",
    "contato_numero": "Contato - Número",
    "contato_botao": "Contato - Botão",
    "privacidade_dados": "Privacidade - Dados",
    "rodape": "Rodapé (todas as páginas)",
}


def slugs_do_site():
    achados = set()
    for arquivo in sorted(RAIZ.glob("*.html")):
        texto = arquivo.read_text(encoding="utf-8")
        for m in re.finditer(r'href="https://wa\.me/[^"]*utm_content=([a-z0-9_]+)', texto):
            achados.add(m.group(1))
    return sorted(achados)


def main():
    slugs = slugs_do_site()
    sem_rotulo = [s for s in slugs if s not in ROTULOS]
    if sem_rotulo:
        sys.exit(f"slugs no site sem rótulo definido no script: {sem_rotulo}")

    proximo = iter(range(1, 1000))

    variaveis = [
        {
            "variableId": "1",
            "name": "Click - utm_content",
            "type": "u",
            "parameter": [
                {"type": "TEMPLATE", "key": "component", "value": "QUERY"},
                {"type": "TEMPLATE", "key": "queryKey", "value": "utm_content"},
                {"type": "TEMPLATE", "key": "customUrlSource", "value": "{{Click URL}}"},
            ],
        },
        {
            "variableId": "2",
            "name": "GA4 - ID de métricas",
            "type": "c",
            "parameter": [{"type": "TEMPLATE", "key": "value", "value": "G-T8PV0H218F"}],
        },
        {
            "variableId": "3",
            "name": "Meta - Pixel ID",
            "type": "c",
            "parameter": [{"type": "TEMPLATE", "key": "value", "value": "1263186065151365"}],
        },
    ]

    # acionador de inicialização próprio (equivalente ao builtin "Initialization
    # - All Pages", sem depender do id interno do builtin)
    acionadores = [
        {"triggerId": "10", "name": "Initialization - Todas as páginas", "type": "INIT"}
    ]
    tags = [
        {
            "tagId": "100",
            "name": "00 - [GT] GA4",
            "type": "googtag",
            "parameter": [
                {"type": "TEMPLATE", "key": "tagId", "value": "{{GA4 - ID de métricas}}"}
            ],
            "firingTriggerId": ["10"],
            "tagFiringOption": "ONCE_PER_EVENT",
        }
    ]

    for indice, slug in enumerate(slugs):
        rotulo = ROTULOS[slug]
        id_acionador = str(11 + indice)
        acionadores.append(
            {
                "triggerId": id_acionador,
                "name": f"[Lead] Botão WPP - {rotulo}",
                "type": "LINK_CLICK",
                "filter": [
                    {
                        "type": "CONTAINS",
                        "parameter": [
                            {"type": "TEMPLATE", "key": "arg0", "value": "{{Click URL}}"},
                            {"type": "TEMPLATE", "key": "arg1", "value": "wa.me"},
                        ],
                    },
                    {
                        "type": "CONTAINS",
                        "parameter": [
                            {"type": "TEMPLATE", "key": "arg0", "value": "{{Click - utm_content}}"},
                            {"type": "TEMPLATE", "key": "arg1", "value": slug},
                        ],
                    },
                ],
                "waitForTags": {"type": "BOOLEAN", "value": "false"},
                "checkValidation": {"type": "BOOLEAN", "value": "false"},
            }
        )
        evento = f"clickwpp_{slug}"
        assert len(evento) <= 40, f"nome de evento GA4 acima de 40 caracteres: {evento}"
        tags.append(
            {
                "tagId": str(101 + indice),
                "name": f"02 - [GA4] Evento - Botão WPP {rotulo} - {evento}",
                "type": "gaawe",
                "parameter": [
                    {"type": "TEMPLATE", "key": "eventName", "value": evento},
                    {
                        "type": "TEMPLATE",
                        "key": "measurementIdOverride",
                        "value": "{{GA4 - ID de métricas}}",
                    },
                ],
                "firingTriggerId": [id_acionador],
                "tagFiringOption": "ONCE_PER_EVENT",
            }
        )

    ids_leads = [str(11 + i) for i in range(len(slugs))]

    # Pixel da Meta como HTML personalizado: 100%% importável, sem depender de
    # baixar template da galeria na importação. Sem o <noscript><img> oficial,
    # pela mesma razão do GTM: dispararia sem checar consentimento.
    base_pixel = (
        "<script>\n"
        "!function(f,b,e,v,n,t,s)\n"
        "{if(f.fbq)return;n=f.fbq=function(){n.callMethod?\n"
        "n.callMethod.apply(n,arguments):n.queue.push(arguments)};\n"
        "if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';\n"
        "n.queue=[];t=b.createElement(e);t.async=!0;\n"
        "t.src=v;s=b.getElementsByTagName(e)[0];\n"
        "s.parentNode.insertBefore(t,s)}(window,document,'script',\n"
        "'https://connect.facebook.net/en_US/fbevents.js');\n"
        "fbq('init', '{{Meta - Pixel ID}}');\n"
        "fbq('track', 'PageView');\n"
        "</script>"
    )
    tags.append(
        {
            "tagId": "200",
            "name": "00 - [Meta] Pixel - Código base",
            "type": "html",
            "parameter": [
                {"type": "TEMPLATE", "key": "html", "value": base_pixel},
                {"type": "BOOLEAN", "key": "supportDocumentWrite", "value": "false"},
            ],
            "firingTriggerId": ["10"],
            "tagFiringOption": "ONCE_PER_EVENT",
        }
    )
    lead_pixel = (
        "<script>\n"
        "if (window.fbq) {\n"
        "  fbq('track', 'Lead', {content_name: '{{Click - utm_content}}'});\n"
        "}\n"
        "</script>"
    )
    tags.append(
        {
            "tagId": "201",
            "name": "01 - [Meta] Lead - Botão WPP (todos os acionadores)",
            "type": "html",
            "parameter": [
                {"type": "TEMPLATE", "key": "html", "value": lead_pixel},
                {"type": "BOOLEAN", "key": "supportDocumentWrite", "value": "false"},
            ],
            "firingTriggerId": ids_leads,
            "tagFiringOption": "ONCE_PER_EVENT",
        }
    )

    contêiner = {
        "exportFormatVersion": 2,
        "exportTime": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
        "containerVersion": {
            "path": "accounts/0/containers/0/versions/0",
            "accountId": "0",
            "containerId": "0",
            "containerVersionId": "0",
            "container": {
                "path": "accounts/0/containers/0",
                "accountId": "0",
                "containerId": "0",
                "name": "Mentalize Joias - Web",
                "publicId": "GTM-0000000",
                "usageContext": ["WEB"],
            },
            "builtInVariable": [
                {"type": "PAGE_URL", "name": "Page URL"},
                {"type": "PAGE_PATH", "name": "Page Path"},
                {"type": "CLICK_URL", "name": "Click URL"},
                {"type": "CLICK_TEXT", "name": "Click Text"},
            ],
            "variable": variaveis,
            "trigger": acionadores,
            "tag": tags,
        },
    }

    DESTINO.write_text(
        json.dumps(contêiner, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"{DESTINO.relative_to(RAIZ)}")
    print(f"  {len(slugs)} slugs → {len(acionadores)} acionadores, {len(tags)} tags, "
          f"{len(variaveis)} variáveis")


if __name__ == "__main__":
    main()
