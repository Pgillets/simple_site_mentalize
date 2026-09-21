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
  - variável constante "GA4 - ID de métricas" (trocar o placeholder G-SUBSTITUA)
  - um acionador "[Lead] Botão WPP - ..." por slug (Apenas links,
    Click URL contém wa.me + Click - utm_content contém <slug>)
  - tag "00 - [GT] GA4" (Tag do Google, acionador Initialization)
  - uma tag "02 - [GA4] Evento - ... - clickwpp_<slug>" por acionador

O que fica manual no painel (documentado no README):
  - tags 01 de conversão do Google Ads (dependem das conversões criadas no Ads)
  - Pixel da Meta (template da galeria do GTM)
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
            "parameter": [{"type": "TEMPLATE", "key": "value", "value": "G-SUBSTITUA"}],
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
