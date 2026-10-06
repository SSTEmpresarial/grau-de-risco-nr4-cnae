"""Build product/data/cnae.json: CNAE 2.3 subclasses joined with NR-4 Annex I risk grades.

Sources (all public, cached under spikes/data/):
- IBGE CONCLA API: servicodados.ibge.gov.br/api/v2/cnae/subclasses
- Current NR-4 Annex I (grade per CNAE class), text mirror of the official annex
- Proposed new NR-4 Annex I (grade per subclass), Brasil Participativo consultation
  reopened by Portaria MTE 203 (2026-06-01)
"""
import json
import os
import re
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "..", "spikes", "data")
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
    h = open(os.path.join(RAW, "guiatrab_nr4.htm"), "rb").read().decode("latin-1")
    t = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h))
    rows = re.findall(r"(\d{2}\.\d{2}-\d)\s+([^0-9]{3,200}?)\s+([1-4])\b", t)
    return {c.replace(".", "").replace("-", ""): int(g) for c, _, g in rows}


def proposed_grades():
    s = open(os.path.join(RAW, "bp_f.txt"), encoding="utf-8").read()
    seg = s[s.find("Subclasse CNAE Descri"):]
    rows = re.findall(r"(\d{1,4}) (\d{6,7}) (.+?) ?([1-4]) (\d+)(?= \d{1,4} \d{6,7} | \d{1,4} [A-ZÁ])", seg)
    out = {}
    for _, sc, desc, gr, _ in rows:
        out.setdefault(sc.zfill(7), (int(gr), desc.strip()))
    return out


def main():
    subs = json.load(open(os.path.join(RAW, "ibge_subclasses.json"), encoding="utf-8"))
    cur = current_grades()
    prop = proposed_grades()
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
        "sources": {
            "cnae": "https://servicodados.ibge.gov.br/api/v2/cnae/subclasses",
            "nr4_current": "https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/normas-regulamentadora/normas-regulamentadoras-vigentes/norma-regulamentadora-no-4-nr-4",
            "nr4_proposed": "https://brasilparticipativo.presidencia.gov.br/processes/AnexoI-NR4",
            "nr1": "https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/normas-regulamentadora/normas-regulamentadoras-vigentes/nr-1",
        },
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump({"meta": meta, "items": items}, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print(json.dumps(meta, indent=1))


if __name__ == "__main__":
    main()
