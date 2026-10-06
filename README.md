# Grau de risco NR-4 por CNAE: vigente × proposta de novo Anexo I (2026)

Base aberta com as **1332 subclasses CNAE 2.3**, o **grau de risco vigente** (Anexo I da NR-4, por classe) e o **grau proposto** na consulta pública do novo Anexo I da NR-4 (reaberta pela Portaria MTE nº 203, de 01/06/2026, por subclasse).

Consulta interativa, página por CNAE e calculadora de dispensa de PGR/PCMSO: **https://grau-de-risco.pages.dev**

## Números
- 442 subclasses **sobem** de grau e 361 **descem**.
- 115 passam de GR 1–2 para GR 3–4. Nelas, a ME/EPP perde a possibilidade de dispensa de PGR e PCMSO prevista na NR-1 (itens 1.8.4 e 1.8.6).

| CNAE | Atividade | GR vigente | GR proposto |
|---|---|---|---|
| 1421-5/00 | Fabricação de meias | 2 | 3 |
| 1529-7/00 | Fabricação de artefatos de couro não especificados anteriormente | 2 | 3 |
| 1731-1/00 | Fabricação de embalagens de papel | 2 | 4 |
| 1732-0/00 | Fabricação de embalagens de cartolina e papel-cartão | 2 | 4 |
| 1733-8/00 | Fabricação de chapas e de embalagens de papelão ondulado | 2 | 4 |
| 1741-9/01 | Fabricação de formulários contínuos | 2 | 3 |
| 1741-9/02 | Fabricação de produtos de papel, cartolina, papel-cartão e papelão ond | 2 | 3 |
| 1742-7/01 | Fabricação de fraldas descartáveis | 2 | 4 |
| 1742-7/02 | Fabricação de absorventes higiênicos | 2 | 4 |
| 1742-7/99 | Fabricação de produtos de papel para uso doméstico e higiênico-sanitár | 2 | 4 |
| 1749-4/00 | Fabricação de produtos de pastas celulósicas, papel, cartolina, papel- | 2 | 4 |
| 2063-1/00 | Fabricação de cosméticos, produtos de perfumaria e de higiene pessoal | 2 | 3 |

Lista completa: https://grau-de-risco.pages.dev/mudancas/

## Arquivos
- `dados/cnae-grau-de-risco.csv` (UTF-8 com BOM, abre direto no Excel)
- `dados/cnae-grau-de-risco.json`
- `build_data.py`: script que gera a base a partir das fontes públicas

Campos: `subclasse, codigo, descricao, classe, divisao, secao, gr_vigente, gr_proposto, mudanca`.

## Fontes
- IBGE/CONCLA, API CNAE: https://servicodados.ibge.gov.br/api/v2/cnae/subclasses
- NR-4 (MTE): https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/normas-regulamentadora/normas-regulamentadoras-vigentes/norma-regulamentadora-no-4-nr-4
- Consulta pública do novo Anexo I: https://brasilparticipativo.presidencia.gov.br/processes/AnexoI-NR4

## Aviso
A proposta **não está em vigor** e pode mudar. Dados informativos; não substituem o texto publicado no DOU nem a análise de profissional habilitado. Encontrou um erro? Abra uma issue.

## Licença
Dados: CC BY 4.0. Cite "SSTE · SST Empresarial, grau-de-risco.pages.dev". Código: MIT.
