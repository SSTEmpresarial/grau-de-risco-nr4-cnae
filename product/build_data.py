"""Build product/data/cnae.json: CNAE 2.3 subclasses joined with NR-4 Annex I risk grades.

Sources (all official, archived under compliance/sources/, consulted 2026-10-06):
- IBGE CONCLA API: servicodados.ibge.gov.br/api/v2/cnae/subclasses
- Current NR-4 Annex I (grade per CNAE class): Portaria MTP nº 2.318/2022, gov.br PDF
- Proposed new NR-4 Annex I (grade per subclass): "texto participativo" on Brasil Participativo,
  consultation reopened by Aviso de Consulta Pública, DOU 13/05/2026 Seção 3 (rectified DOU 01/06/2026).
  The proposal is NOT in force.
"""
import json
import os
import re
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "compliance", "sources")
CONSULTED = "2026-10-06"  # date the official sources below were downloaded and checked
OUT = os.path.join(HERE, "data", "cnae.json")

SMALL_WORDS = {"de", "da", "do", "das", "dos", "e", "em", "para", "com", "a", "o", "as", "os", "por", "na", "no", "nas", "nos", "ou", "à", "às"}


def sentence_case(s):
    words = s.lower().split()
    out = []
    for i, w in enumerate(words):
        out.append(w if (i and w in SMALL_WORDS) else (w[:1].upper() + w[1:] if i == 0 else w))
    return " ".join(out)


def fmt_sub(sc):
    return f"{sc[:4]}-{sc[4]}/{sc[5:]}"


def fmt_class(c):
    return f"{c[:2]}.{c[2:4]}-{c[4]}"


def current_grades():
    """Official text: Portaria MTP nº 2.318/2022 (new NR-04), Anexo I, downloaded from gov.br."""
    t = open(os.path.join(SRC, "portaria_2318.txt"), encoding="utf-8").read()
    t = t[t.find("ANEXO I RELAÇÃO DA CLASSIFICAÇÃO"):t.find("ANEXO II DIMENSIONAMENTO")]
    rows = re.findall(r"(\d{2}\.\d{2}-\d)\s+([^0-9]{3,200}?)\s+([1-4])\b", t)
    return {c.replace(".", "").replace("-", ""): int(g) for c, _, g in rows}


CORRECTIONS = []  # codes in the official consultation text that do not exist in IBGE, resolved by exact description


def norm(s):
    return re.sub(r"\s+", " ", s.lower()).strip()


def proposed_grades(ibge_desc):
    s = open(os.path.join(SRC, "consulta_anexoI_nr04_texto_participativo_2026-10-06.txt"), encoding="utf-8").read()
    seg = s[s.find("Subclasse CNAE Descri"):]
    rows = re.findall(r"(\d{1,4}) (\d{5,7}) (.+?) ?([1-4]) (\d+)(?= \d{1,4} \d{5,7} | \d{1,4} [A-ZÁ])", seg)
    by_desc = {norm(d): k for k, d in ibge_desc.items()}
    out = {}
    for _, sc, desc, gr, _ in rows:
        code = sc.zfill(7)
        if code not in ibge_desc:
            fixed = by_desc.get(norm(desc))
            if not fixed:
                continue
            if code != fixed and (sc, fixed) not in [(c["as_published"], c["resolved_to"]) for c in CORRECTIONS]:
                CORRECTIONS.append({"as_published": sc, "resolved_to": fixed, "description": desc.strip(), "method": "exact description match with IBGE"})
            code = fixed
        out.setdefault(code, (int(gr), desc.strip()))
    return out


def main():
    subs = json.load(open(os.path.join(SRC, "ibge_cnae_subclasses_2026-10-06.json"), encoding="utf-8"))
    cur = current_grades()
    prop = proposed_grades({x["id"]: x["descricao"] for x in subs})
    items = []
    for x in subs:
        sc = x["id"]
        cl = x["classe"]
        dv = cl["grupo"]["divisao"]
        se = dv["secao"]
        p = prop.get(sc)
        items.append({
            "id": sc,
            "code": fmt_sub(sc),
            "desc": p[1] if p else sentence_case(x["descricao"]),
            "class": fmt_class(cl["id"]),
            "class_desc": sentence_case(cl["descricao"]),
            "division": dv["id"],
            "division_desc": sentence_case(dv["descricao"]),
            "section": se["id"],
            "section_desc": sentence_case(se["descricao"]),
            "gr_current": cur.get(cl["id"]),
            "gr_proposed": p[0] if p else None,
            "atividades": list(x.get("atividades") or [])[:12],
        })
    meta = {
        "built": date.today().isoformat(),
        "n_subclasses": len(items),
        "n_with_current": sum(1 for i in items if i["gr_current"]),
        "n_with_proposed": sum(1 for i in items if i["gr_proposed"]),
        "consulted": CONSULTED,
        "corrections": CORRECTIONS,
        "status": {
            "vigente": "NR-04 Anexo I aprovado pela Portaria MTP nº 2.318, de 3/8/2022 (por classe CNAE)",
            "proposta": "Proposta de novo Anexo I em consulta pública: Aviso de Consulta Pública do MTE, DOU de 13/05/2026, Seção 3 (retificado no DOU de 01/06/2026), prazo de 45 dias; após a consulta: análise pela SIT, GTT tripartite e CTPP. Nenhum ato final publicado até a data de consulta.",
        },
        "sources": {
            "cnae": "https://servicodados.ibge.gov.br/api/v2/cnae/subclasses",
            "nr4_current": "https://www.gov.br/trabalho-e-emprego/pt-br/assuntos/inspecao-do-trabalho/seguranca-e-saude-no-trabalho/sst-portarias/2022/portaria-mtp-no-2-318-nova-nr-04.pdf",
            "nr4_page": "https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/normas-regulamentadora/normas-regulamentadoras-vigentes/norma-regulamentadora-no-4-nr-4",
            "nr4_proposed": "https://brasilparticipativo.presidencia.gov.br/processes/AnexoI-NR4",
            "nr1": "https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/normas-regulamentadora/normas-regulamentadoras-vigentes/nr-01-atualizada-2025-i-3.pdf",
        },
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump({"meta": meta, "items": items}, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print(json.dumps(meta, indent=1))


if __name__ == "__main__":
    main()
