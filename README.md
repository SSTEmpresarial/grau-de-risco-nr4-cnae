# Grau de risco NR-4 por CNAE: vigente × proposta de novo Anexo I (consulta pública 2026)

Base aberta com as **1332 subclasses CNAE 2.3**, separando:

- **Grau VIGENTE**: Anexo I da NR-4 aprovado pela **Portaria MTP nº 2.318/2022**, definido por classe CNAE (cada subclasse herda o grau da classe). É o que vale hoje.
- **Grau PROPOSTO (não vigente)**: proposta de novo Anexo I em **consulta pública**, reaberta pelo Aviso de Consulta Pública do MTE (DOU de 13/05/2026, Seção 3; retificado no DOU de 01/06/2026), definido por subclasse.

> **Situação verificada em 06/10/2026:** nenhum ato final do novo Anexo I foi publicado. Após a consulta, a proposta segue para análise da SIT, de grupo de trabalho tripartite e da CTPP. Os graus propostos podem mudar e **não criam obrigação**. Se aprovada, a atualização deve indicar prazo de adequação (Portaria MTP nº 2.318/2022, art. 3º, § 2º).

Consulta interativa, página por CNAE e verificação informativa das dispensas de PGR/PCMSO (NR-1, item 1.8): **https://grau-de-risco.pages.dev**

## Números (reproduzíveis: `python compliance/claims.py`)
Comparando a proposta com o grau vigente:
- 442 subclasses teriam grau **maior**, 362 grau **menor** e 528 ficariam iguais.
- 115 passariam de GR 1–2 para GR 3–4. **Caso a proposta seja aprovada**, as ME/EPP dessas atividades poderão deixar de se enquadrar nas dispensas de PGR e PCMSO da NR-1 (itens 1.8.4 e 1.8.6, que só alcançam GR 1 e 2 e exigem outras condições).
- 215 passariam de GR 3–4 para GR 1–2.

| CNAE | Atividade | GR vigente | GR proposto (não vigente) |
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

## Verificação da leitura do texto oficial
- O grau vigente das 673 classes confere com o Anexo I da Portaria MTP nº 2.318/2022 (PDF oficial).
- O texto da consulta traz a tabela duas vezes (Anexo e Apêndice de metodologia); as cópias são idênticas (`copies_differ: 0`), e a numeração de linhas é contínua.
- Correção documentada: no texto da consulta, a subclasse 0810-0/99 aparece com o código "10099"; ela foi identificada pela descrição idêntica à do IBGE.

## Arquivos
- `dados/cnae-grau-de-risco.csv` (UTF-8 com BOM) e `dados/cnae-grau-de-risco.json`. Campos: `subclasse, codigo, descricao, classe, divisao, secao, gr_vigente, gr_proposto_consulta_2026, diferenca, status_proposta`.
- `product/build_data.py`: gera a base a partir das fontes arquivadas.
- `compliance/claims.py` e `compliance/claims.json`: números, método, hashes SHA-256 das fontes.
- `compliance/sources/`: cópias das fontes oficiais consultadas em 06/10/2026.

## Fontes
- Portaria MTP nº 2.318/2022 (NR-4): https://www.gov.br/trabalho-e-emprego/pt-br/assuntos/inspecao-do-trabalho/seguranca-e-saude-no-trabalho/sst-portarias/2022/portaria-mtp-no-2-318-nova-nr-04.pdf
- Consulta pública do novo Anexo I: https://brasilparticipativo.presidencia.gov.br/processes/AnexoI-NR4
- NR-1 consolidada (gov.br, 2025): https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/normas-regulamentadora/normas-regulamentadoras-vigentes/nr-01-atualizada-2025-i-3.pdf
- IBGE/CONCLA, API CNAE: https://servicodados.ibge.gov.br/api/v2/cnae/subclasses

## Licenças e aviso
- Normas, portarias e demais atos oficiais não são protegidos por direito autoral (Lei nº 9.610/1998, art. 8º, IV); as cópias em `compliance/sources/` são reproduzidas para verificação, com as fontes citadas. Textos editoriais do portal gov.br (CC BY-ND 3.0) não são reproduzidos.
- A base compilada: **CC BY 4.0** (cite "SSTE · SST Empresarial, grau-de-risco.pages.dev"). Código: MIT.
- Dados informativos: não substituem o texto publicado no DOU, o levantamento de perigos no estabelecimento nem a análise de profissional competente. Encontrou um erro? Abra uma issue.
